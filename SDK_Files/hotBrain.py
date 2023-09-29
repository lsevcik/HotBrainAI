from scanner import Scanner
from cmn_types import *
import concurrent.futures
from time import sleep
import ctypes
import sys
import cv2

# Event handler for scan finding a headband, prints sensor info
def sensor_found(scanner, sensors):
    for index in range(len(sensors)):
        print('Sensor found: %s' % sensors[index])

# Event handler for headband state changing, prints the state
def on_sensor_state_changed(sensor, state):
    print('Sensor {0} is {1}'.format(sensor.name, state))

# Event handler for signal data being recieved
def on_signal_data_received(sensor, data):
    print(data)

# Event handler for resist data being recieved
# def on_resist_data_received(sensor, data):
#     print(data)

# Event handler for electrode state being changed
def on_electrodes_state_changed(sensor, data):
    print(data)

# Event handler for device connection
def device_connection(sensor_info):
    return scanner.create_sensor(sensor_info)

# Creates a simple message box window
# Warns the user that the video is about to start
def displayMsg():
    ctypes.windll.user32.MessageBoxW(0, "Ready to Proceed?", "Alert", 1)

# Function to play a video for testing the headband
def playVideo():
    # Define variables
    videoName = "Videos\HotBrain_Test_Video.mp4" # Name of the video file
    windowName = "TEST VIDEO" # Name of the video window
    
    # Create a fullscreen window for playing a video
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cap = cv2.VideoCapture(videoName)  # Start capture
    
    # Check if the video exists, exit if not
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # Loop for video playback
    while(cap.isOpened()):
        success, frame = cap.read() # Start reading the frames

        # Frames are still being received
        if success:
            cv2.imshow(windowName, frame) # Continue showing frames
        
            quitButton = cv2.waitKey(25) & 0xFF == ord('q') # Get user input for q button (QUIT)

            if quitButton: # If q is pressed, video ends
                break
        else: # Frames no longer being received, exit window
            break

    cap.release() # Release the capture
    cv2.destroyAllWindows() # Remove the window

try:
    scanner = Scanner([SensorFamily.SensorLEBrainBitBlack, SensorFamily.SensorLEBrainBit,
                    SensorFamily.SensorLECallibri]) # Check for headband sensors

    scanner.sensorsChanged = sensor_found # Call event handler for sensor found
    
    # Search for the headband (up to 5 seconds)
    scanner.start()
    print("Starting search for 5 sec...")
    sleep(5)
    scanner.stop()

    # Loop while the device is connected and run all features
    sensorsInfo = scanner.sensors()
    for i in range(len(sensorsInfo)):
        current_sensor_info = sensorsInfo[i]
        print(sensorsInfo[i])

        # Start thread pool and connect device
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(device_connection, current_sensor_info)
            sensor = future.result()
            print("Device connected")

        sensor.sensorStateChanged = on_sensor_state_changed # Call event handler for state change (connected)

        sensFamily = sensor.sens_family

        # Print all sensor info
        print(sensFamily)
        print(sensor.features)
        print(sensor.commands)
        print(sensor.parameters)
        print(sensor.name)
        print(sensor.state)
        print(sensor.address)
        print(sensor.serial_number)
        print(sensor.batt_power)
        print(sensor.sampling_frequency)
        print(sensor.gain)
        print(sensor.data_offset)
        print(sensor.version)

        # Start the signal data feature
        if sensor.is_supported_feature(SensorFeature.FeatureSignal):
            sensor.signalDataReceived = on_signal_data_received

        # if sensor.is_supported_feature(SensorFeature.FeatureResist):
        #     sensor.resistDataReceived = on_resist_data_received

        # Take signal data output and store into a CSV file
        with open('output.csv', 'w', newline='') as dataFile:
            if sensor.is_supported_command(SensorCommand.CommandStartSignal):
                sensor.exec_command(SensorCommand.CommandStartSignal) #this line prints the data

                displayMsg() # Get the user ready with a message
                sys.stdout = dataFile  # Redirect stdout to the file
                playVideo()
                sys.stdout = sys.__stdout__ # Stop redirect

                sensor.exec_command(SensorCommand.CommandStopSignal)

        # if sensor.is_supported_command(SensorCommand.CommandStartResist):
        #     sensor.exec_command(SensorCommand.CommandStartResist)
        #     print("Start resist")
        #     sleep(5)
        #     sensor.exec_command(SensorCommand.CommandStopResist)
        #     print("Stop resist")

        sensor.disconnect()
        print("Disconnect from sensor")
        del sensor # Garbage collection for sensor

    del scanner # Garbage collection for scanner

# Print any errors
except Exception as err:
    print(err)
