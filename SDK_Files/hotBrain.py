from scanner import Scanner
from cmn_types import *
import concurrent.futures
from time import sleep
import ctypes
import sys
import cv2
import csv
import os

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

        # Creates a temporary text file for parsing the data
        with open('output.txt', 'w', newline='') as dataFile:
            if sensor.is_supported_command(SensorCommand.CommandStartSignal):
                sensor.exec_command(SensorCommand.CommandStartSignal) #this line prints the data

                displayMsg() # Get the user ready with a message
                sys.stdout = dataFile  # Redirect stdout to the file
                playVideo() # Play the customer's video
                sys.stdout = sys.__stdout__ # Stop redirect

                sensor.exec_command(SensorCommand.CommandStopSignal)

        # Opens the text file to parse the data and creates a csv file with the parsed data
        with open('output.txt') as fdin, open('output.csv', 'w', newline='') as fdout:
            wr = csv.DictWriter(fdout, fieldnames=['PackNum_1', 'O1_1', 'O2_1', 'T3_1', 'T4_1', '', 'PackNum_2', 'O1_2', 'O2_2', 'T3_2', 'T4_2'],
                                extrasaction='ignore')  # ignore unwanted fields
            
            row_1, row_2 = {}, {} # Initialize empty dictionaries
            wr.writeheader()    # write the header line

            # Read the data file line by line and parse data for csv file
            while True:
                data = fdin.readline() # Get the next line
                
                if not data: # End of file
                    break

                data = data.strip("[BrainBitSignalData(")
                
                count = 0 # Loop counter
                while count < 2: # Loops twice because of bimodal readings, parses fields for PackNo, O1, O2, T3, and T4
                    packNo, data = data.split('=', 1)[1].split(',', 1)[0], data.split('=', 1)[1].split(',', 1)[1]
                    data = data.strip(f"Marker={packNo}, ")
                    o1, data = data.split('=', 1)[1].split(',', 1)[0], data.split('=', 1)[1].split(',', 1)[1].strip()
                    o2, data = data.split('=', 1)[1].split(',', 1)[0], data.split('=', 1)[1].split(',', 1)[1].strip()  
                    t3, data = data.split('=', 1)[1].split(',', 1)[0], data.split('=', 1)[1].split(',', 1)[1].strip()
                    
                    if count == 0: # Checking for first set of data, allows proper parsing
                        t4, data = data.split('=', 1)[1].split(',', 1)[0].strip(')'), data.split('=', 1)[1].split(',', 1)[1].strip()
                        data = data.strip("), BrainBitSignalData(")
                        row_1 = {wr.fieldnames[0]: packNo, wr.fieldnames[1]: o1, wr.fieldnames[2]: o2, wr.fieldnames[3]: t3, wr.fieldnames[4]: t4} # First set of data for the row
                    else: # End of the second set of data
                        t4 = data.split('=', 1)[1].strip(')]')
                        row_2 = {wr.fieldnames[6]: packNo, wr.fieldnames[7]: o1, wr.fieldnames[8]: o2, wr.fieldnames[9]: t3, wr.fieldnames[10]: t4} # Second set of data for the row
                    
                    count += 1 # Update loop counter

                row_1.update(row_2) # Merge the dictionaries for the two sets of data

                if len(row_1) != 0: # Check if a row has been parsed then add to the csv file
                    wr.writerow(row_1)

        os.remove("output.txt") # Delete temporary text file

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
