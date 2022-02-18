# 4WD Rover ESP32 Desktop client 
 Desktop python GUI application for controlling a 4WD Rover powered by an ESP-32  microcontroller.
 Goal: The aim of this project was the remote control of a rover device powered by an ESP-32 microcontroller with a dedicated desktop application.
 The rover was equipped with 2 HCSR04 ultrasonic sensors, 2 infrared sensors, a battery slot and of course 4 dc motors and can be piloted in two different ways: 
 1) Manually
 The user via the python application can control the device by clicking buttons on the screen.
 2) "Automatically"
 The rover will move forwards until an obstacle is detected and then it will decide the best route to avoid the obstacle. An obstacle is detected with a combo of HCSR04 sensors and    infrared sensors.
 Of course the device can be stopped at any time with the desktop application. 
 All data obtained from the sensors (presence of an obstacle and its distance) will be shown in the desktop application in real time.
 Both the ESP-32 microcontroller and the device running the python application must be connected on the same wifi network in order to control the rover.
 This was a "beta" version of a project "iOS application for controlling a 4WD Rover powered by an ESP-32" 
 
# Technical Information
- The python code for the microcontroller was developed under Zerynth studio, consequently it will not run properly under any other environment, you will have to register your microcontroller under zerynth studio and then run the code.
- The desktop GUI application was developed with Python 3.8
