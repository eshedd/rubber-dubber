# 🎶 MIDI Music Generation with YOLOv8 Object Detection

## 📖 Overview
This project combines real-time object detection using **YOLOv8** with **MIDI music generation** to create dynamic musical experiences controlled by visual cues. The system captures video input from a camera, analyzes it for traffic lights, and generates MIDI music based on the detected state of the lights. The code is structured in a modular way, with classes for MIDI control, song composition, and YOLOv8 integration.

---

## ✨ Features
- **🎹 MIDI Control**: The `MidiPlayer` class handles MIDI output, allowing the program to send note on/off messages to a connected MIDI device or virtual port.
- **🎶 Song Structure**: The `Song` class defines the musical structure, including tempo, drum patterns, and chord progressions. It provides methods for playing standard bars, suspense bars, and drop beats.
- **🎼 Chord Generation**: The `ChordGenerator` class uses a Markov chain based on music theory principles to generate chord progressions. It supports major and minor keys and can translate chord progressions into MIDI note values.
- **🖼️ YOLOv8 Integration**: The `run_yolo_detection` function utilizes a pre-trained YOLOv8 model to detect red, green, or yellow traffic lights in real-time. The detected light influences the music generation. For instance, detecting a red light triggers a "suspense bar," while a green light trigger a "standard bar."

---

## 🚀 Usage
The `main` function initializes the `MidiPlayer`, loads the YOLOv8 model, and starts two threads:
- **🎥 Detection Thread**: Continuously captures video frames, performs object detection, and updates the `user_input` variable in the `MidiPlayer` based on the detected objects.
- **🎵 Music Generation Thread**: Generates and plays music based on the current value of `user_input`, switching between different song sections accordingly.

---

## 🎛️ Example
The code includes an example setup that uses a drum pattern, a chord progression in **B major**, and a drop note. The YOLOv8 model detects 'green' and 'red' traffic lights to switch between different musical sections.

---

## 📦 Dependencies
- `rtmidi`
- `ultralytics`
- `OpenCV` (cv2)
- `numpy`

---

## 🌟 Future Improvements
- 🔍 Expanding the YOLOv8 model to recognize a wider range of objects and mapping them to more diverse musical parameters.
- 🧠 Implementing more sophisticated music generation algorithms, such as using **recurrent neural networks (RNNs)**.
- 🖥️ Adding a graphical user interface (GUI) for easier control and visualization.
- 🎨 Integrating with other creative tools and platforms.

---

For training traffic detector: 
https://colab.research.google.com/drive/15cb-ZtznRvdVCfCISJhnyEJ_xYzT0GlF?authuser=1#scrollTo=VIdYdhQjT1pR
