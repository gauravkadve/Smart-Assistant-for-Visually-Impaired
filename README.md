# Smart-Assistant-for-Visually-Impaired
This repository contains files on the project- "Smart Assistant for Visually Impaired" 

## 1. Introduction
Self-navigating and understanding the environment is a significant challenge for people who are visually impaired. According to the World Health Organization, more than 2 
billion people are affected by some form of visual impairment. 
For these people, the quest for independent navigation is 
sometimes associated with challenges and risk factors. 
Current assistive tools, including white canes and guide dogs, 
have limitations in providing instantaneous environmental 
information. This research is to develop a solution that enables 
real-time object identification, distance measurement, and 
auditory alerts in providing the user with the necessary 
information required in safe navigation. The YOLOv8 object 
detection framework will be used because of its exemplary 
accuracy and effectiveness.

## 2. System Architecture
The proposed system enhances the navigation of visually impaired individuals by providing instant information about their surroundings. The system is comprised of three main components:

1. **Object Detection Module**: Identifies objects in the surroundings.
2. **Distance Estimation Mechanism**: Measures the distance to detected objects.
3. **Audio Feedback System**: Supplies context-sensitive information through audio feedback.

These components work synergistically to identify objects, measure distances, and provide audio guidance. The methodology for each component is detailed below.

---

## A. YOLO Object Detection Model

### Overview
The YOLO (You Only Look Once) framework is highly valued for its balance of speed and accuracy in real-time object detection. Key features include:

- **Pre-trained on COCO Dataset**: Detects 80 distinct object categories.
- **Anchor-free Approach**: Streamlines training and inference.
- **Decoupled Heads**: Separates classification and localization tasks.
- **Neck Layers**: Facilitates feature fusion across scales for accurate detection.

### Real-Time Processing
YOLO excels in applications requiring timely responses, such as:

- Live-stream analysis
- Drone navigation
- Industrial automation

### Customizability
YOLO supports fine-tuning with custom datasets, enabling:

- Focus on specific object categories
- Adaptation to specific environmental conditions

### Output
Detection results include:

- **Class Labels**: Identifies object categories.
- **Bounding Boxes**: Provides object locations.
- **Confidence Scores**: Indicates detection accuracy.

---

## B. Distance Estimation Technique

### Pinhole Camera Model
The system estimates distance using the equation:

\[ D = \frac{H \times f}{h} \]

Where:
- **D**: Estimated distance
- **H**: Real-world height of the object
- **f**: Focal length of the camera lens
- **h**: Object height in the frame

### Distance Conversion to Steps
To improve usability for visually impaired individuals, the distance is converted into steps:

\[ \text{Steps} = \frac{D}{S} \]

Where **S** is the individual's step length.

---

## C. Voice Feedback System

### Real-Time Text-to-Speech
The system uses a text-to-speech engine to announce:

- Detected object class
- Distance to the object
- Object position (e.g., left, center, right)

### Features
- **Adjustable Speech Rate**: Ensures clarity for diverse user needs.
- **Threading**: Reduces overhead by processing voice feedback separately.

---

## D. Grid Mapping

### Technique
The frame is divided into three parts for precise spatial mapping:

- Left
- Center
- Right

### Benefits
- Provides clear directional cues.
- Enhances navigation by offering real-time guidance on object positions.

---

## E. Thresholds

### 1. Confidence Threshold
Filters out objects detected with low confidence to reduce false identifications.

### 2. Approaching Threshold
Handles motion by comparing the difference between previous and current distances to reduce false alarms.

### 3. Proximity Threshold
Avoids announcing objects that are far away unless within a predefined threshold:
- Higher threshold for approaching objects.

### 4. Position Threshold
Reduces false alarms by analyzing changes in object positions.

---
