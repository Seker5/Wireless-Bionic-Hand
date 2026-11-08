# Wireless Bionic Hand

## Project Overview

Wireless Bionic Hand is a wireless robotic hand project developed using STM32 microcontroller technology and computer vision.

The system uses a computer camera to detect human hand movements in real time. Hand movements are processed using Python, OpenCV, and MediaPipe. The detected movements are then transmitted wirelessly via Bluetooth to an STM32F401RE microcontroller, which controls five servo motors to operate the robotic fingers.

## Hardware Components

- STM32F401RE Microcontroller
- 5 Servo Motors
- Bluetooth Communication Module
- Rechargeable Battery System
- Custom-designed Robotic Hand Structure

## Software and Technologies

- Python
- OpenCV
- MediaPipe
- STM32CubeMX
- Embedded C
- Bluetooth Serial Communication

## System Architecture

1. A computer camera captures the user's hand movements.
2. MediaPipe detects hand landmarks and finger positions.
3. Python processes the detected hand movements.
4. Control commands are transmitted wirelessly via Bluetooth.
5. The STM32F401RE receives and processes the commands.
6. Five servo motors control the robotic fingers.

## Installation and Requirements

### Python Requirements

- Python 3
- OpenCV
- MediaPipe
- PySerial

Install the required Python libraries:

```bash
pip install opencv-python mediapipe pyserial
```

## Running the Python Application

Navigate to the directory containing the Python source code and execute:

```bash
python biyonik_kol.py
```

Make sure that a camera is connected to the computer.

The Bluetooth serial port and camera settings must be configured according to the hardware setup.

## STM32 Firmware

The embedded firmware is developed for the STM32F401RE microcontroller.

The STM32 firmware source files are included in this repository.

The firmware can be compiled and uploaded to the microcontroller using a compatible STM32 development environment.

## Project Features

- Real-time hand movement detection
- Wireless Bluetooth communication
- Five servo motor-controlled fingers
- Camera-based hand tracking
- Rechargeable and standalone robotic hand

## Project Status

The prototype has been developed and successfully tested.

## Developer

**Abdurrahim Şeker**

Mechatronics Engineering Student
