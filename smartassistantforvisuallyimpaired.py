import cv2
import pyttsx3
import threading
from ultralytics import YOLO

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 300)  # Speech rate

# Load YOLOv8 model
model = YOLO('yolov8s.pt')

# Start video capture with a video file
# cap = cv2.VideoCapture(r"C:\Users\gaura\Downloads\videoplayback.mp4")
cap = cv2.VideoCapture(0)

# Check if the video file opened successfully
if not cap.isOpened():
    print("Error: Couldn't open the video file.")
    exit()

# Frame dimensions
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Camera properties
focal_length = 500  
real_world_height = 1.7 

# Step length (in meters) for the distance-to-steps conversion
step_length = 0.8  # Average human step length in meters

# 3x3 Grid dimensions
grid_rows = 2  # Two rows
grid_cols = 3  # Three columns
cell_width = frame_width // grid_cols
cell_height = frame_height // 4

# Store previous distances and positions
previous_data = {}

# Function to draw grid
def draw_grid(frame):
    for i in range(1, grid_cols):
        cv2.line(frame, (i * cell_width, 0), (i * cell_width, frame_height), (255, 255, 255), 2)

# Function to check which grid cell an object belongs to
def get_grid_cell(xmin, ymin, xmax, ymax):
    center_x = (xmin + xmax) // 2
    center_y = (ymin + ymax) // 2
    grid_x = center_x // cell_width
    grid_y = center_y // cell_height
    return grid_y, grid_x, center_x, center_y

# Function to estimate distance based on object height in the image
def estimate_distance(object_height_in_image):
    if object_height_in_image == 0:
        return 0
    distance = (real_world_height * focal_length) / object_height_in_image
    return distance

# Function to check if an object is approaching based on distance and position change
def is_approaching(previous_distance, current_distance, previous_center, current_center, distance_threshold=8, position_threshold=6):
    distance_diff = previous_distance - current_distance
    position_diff = ((previous_center[0] - current_center[0]) ** 2 + (previous_center[1] - current_center[1]) ** 2) ** 0.5
    return distance_diff > distance_threshold and position_diff > position_threshold

# Function to announce text through voice output asynchronously
def speak_async(text):
    threading.Thread(target=speak, args=(text,)).start()

# Synchronous speak function for the thread
def speak(text):
    engine.say(text)
    engine.runAndWait()

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video.")
        break

    # Perform object detection
    results = model(frame)
    draw_grid(frame)
    
    current_data = {}

    for result in results[0].boxes:
        xmin, ymin, xmax, ymax = result.xyxy[0].tolist()
        class_id = int(result.cls[0])
        class_name = results[0].names[class_id]
        confidence = result.conf[0].item()

        if confidence > 0.6:
            grid_y, grid_x, center_x, center_y = get_grid_cell(xmin, ymin, xmax, ymax)
            object_height_in_image = ymax - ymin
            distance = estimate_distance(object_height_in_image)

            # Convert distance to steps
            steps = distance // step_length  # Calculate steps
            steps=int(steps)
            # Determine direction
            direction = 'left' if grid_x == 0 else 'center' if grid_x == 1 else 'right'

            # Unique key for each object in a grid cell
            obj_key = (grid_y, grid_x, class_id)  

            # Check if the object is approaching based on distance and position
            is_approaching_flag = False
            if obj_key in previous_data:
                previous_distance, previous_center = previous_data[obj_key]
                is_approaching_flag = is_approaching(previous_distance, distance, previous_center, (center_x, center_y))

            # Voice output if object is within 2 meters
            if distance <= 2 and obj_key not in previous_data: 
                speak_async(f"{class_name} detected {steps} steps away on the {direction}.")
            
            # Voice output if object is approaching
            if is_approaching_flag and distance <= 8:
                speak_async(f"{class_name} approaching from the {direction}.")

            # Update current data
            current_data[obj_key] = (distance, (center_x, center_y))

            # Draw bounding box around the detected object
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
            
            # Display class name, grid position, steps, and "Approaching" if applicable
            approach_text = " (Approaching)" if is_approaching_flag else ""
            cv2.putText(frame, f'{class_name} in Grid[{grid_y}, {grid_x}]{approach_text}', 
                        (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f'Steps: {steps:.2f}', 
                        (int(xmin), int(ymin) - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Update previous data with current data
    previous_data = current_data

    cv2.imshow('YOLOv8 Object Detection with Grid and Steps', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
