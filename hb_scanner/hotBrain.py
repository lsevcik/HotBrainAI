from sdk_tools.scanner import Scanner
from cmn_types import *
import concurrent.futures
from time import sleep
import ctypes
import sys
import cv2
import csv
import os
import shutil
import subprocess
import requests
from turtle import textinput

# Event handler for scan finding a headband, prints sensor info
def sensor_found(scanner, sensors):
    for index in range(len(sensors)):
        print('Sensor found: %s' % sensors[index])

# Event handler for headband state changing, prints the state
def on_sensor_state_changed(sensor, state):
    print('Sensor {0} is {1}'.format(sensor.name, state))

# Event handler for signal data being recieved
def on_signal_data_received(sensor, data):
    for i in range(len(data)):
        print(data[i].PackNum, data[i].O1, data[i].O2, data[i].T3, data[i].T4)

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
# def playVideo(videoName):
    # Define variables
    videoName = "Videos\\HotBrain_Test_Video.mp4" # Name of the video file
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

# Opens the text file to parse the data and creates a csv file with the parsed data
def createOutputCSV():
# def createOutputCSV(dataFile):
    with open('output.txt') as fdin, open('output.csv', 'w', newline='') as fdout:
        wr = csv.DictWriter(fdout, fieldnames=['Sample', 'O1', 'O2', 'T3', 'T4'],
                            extrasaction='ignore')  # Create header and ignore unwanted fields
        wr.writeheader() # write the header line

        row = {} # Initialize empty dictionary for the row
        count = 1 # Loop counter

        # Read the data file line by line and parse data for csv file
        while True:
            data = fdin.readline() # Get the next line
            
            if not data: # End of file
                break
            
            data = data.split(' ') # Split up 01, 02, T3, T4

            # print("PackNum: ", data[0]) # For testing purposes

            # Add sample # and electrode data to row values
            Sample = count
            o1 = data[1]
            o2 = data[2]
            t3 = data[3]
            t4 = data[4].strip('\n') # Strip very last data point's new line character

            # Create a row
            row = {wr.fieldnames[0]: Sample, wr.fieldnames[1]: o1, wr.fieldnames[2]: o2, wr.fieldnames[3]: t3, wr.fieldnames[4]: t4}

            count += 1 # Update loop counter

            if len(row) != 0: # Check if a row has been parsed then add to the csv file
                wr.writerow(row)

    os.remove("output.txt") # Delete temporary text file

    shutil.move(f'{fdout.name}', f'Processing/{fdout.name}') # Moves the newly created CSV file to processing folder
 
# Attempts to get the video urls from the server
def getVideoUrl():
    url = "http://localhost:8080" # ToDo: Get the url where we receive video data from server
    token = textinput("Get Token", "Please enter your token")
    response = requests.get(url, headers={'Authorization':f'Bearer {token}'})

    print(response)

    # if videoUrl:
    #     return videoUrl

# # Attempts to send a datafile to the server
def sendFileToServer(fileName):
    dataFile = open(fileName, "rb") # Open the dataFile
    url = "http://localhost:8080/api/scanner" # ToDo: Get the url where we want to post the csv files
    submission = requests.post(url, files = {"form_field_name": dataFile}) # ToDo: Get the form_field_name from server
    
    print(submission)

    # if submission.ok: # Checks if the file was submitted 
    #     return True
    # else:
    #     return False

try:
    token = textinput("Get Token", "Please enter your token")
    # getVideoUrl()
    # sendFileToServer("output.csv")
    # Runs the generatescans and clearscans programs
    # os.chdir('Programs_From_Shane')
    # subprocess.call(args='start', executable='GenerateScans.exe')
    # os.chdir('user_scans')
    # subprocess.call(args='start', executable='ClearScans.exe')
    # os.chdir('..\..')

    scanner = Scanner([SensorFamily.SensorLEBrainBit]) # Check for headband sensors

    scanner.sensorsChanged = sensor_found # Call event handler for sensor found
    
    # Search for the headband
    scanner.start()
    print("Starting search...")
    while len(scanner.sensors()) == 0:
        sleep(1)
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

        # Start the signal data feature
        if sensor.is_supported_feature(SensorFeature.FeatureSignal):
            sensor.signalDataReceived = on_signal_data_received

        # if sensor.is_supported_feature(SensorFeature.FeatureResist):
        #     sensor.resistDataReceived = on_resist_data_received

        # videoName = getVideoUrl()

        # Creates a temporary text file for parsing the data
        with open('output.txt', 'w', newline='') as dataFile:
            if sensor.is_supported_command(SensorCommand.CommandStartSignal):
                sensor.exec_command(SensorCommand.CommandStartSignal) #this line prints the data
                
                displayMsg() # Get the user ready with a message
                sys.stdout = dataFile  # Redirect stdout to the file
                playVideo() # Play the customer's video
                sys.stdout = sys.__stdout__ # Stop redirect

                sensor.exec_command(SensorCommand.CommandStopSignal)

        createOutputCSV() # Create the CSV file from output text

        # sendFileToServer(dataFile)

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
