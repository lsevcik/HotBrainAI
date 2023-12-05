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
import turtle
import configparser

# Read config file for server communication
config = configparser.ConfigParser()
config.read(r'config.cfg')

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
        print(data[i].O1, data[i].O2, data[i].T3, data[i].T4)

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
def playVideo(videoURL, type):
    windowName = str(type) # Name of the video window (video type)
    
    # Create a fullscreen window for playing a video
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cap = cv2.VideoCapture(videoURL)  # Start capture
    
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
def createOutputCSV(inputFile, type):
    outputFile = inputFile.strip(".txt") + ".csv"
    with open(inputFile) as fdin, open(outputFile, 'w', newline='') as fdout:
        wr = csv.DictWriter(fdout, fieldnames=['O1', 'O2', 'T3', 'T4'],
                            extrasaction='ignore')  # Create header and ignore unwanted fields

        row = {} # Initialize empty dictionary for the row

        # Read the data file line by line and parse data for csv file
        while True:
            data = fdin.readline() # Get the next line
            
            if not data: # End of file
                break
            
            data = data.split(' ') # Split up 01, 02, T3, T4

            # Add sample # and electrode data to row values
            o1 = data[0]
            o2 = data[1]
            t3 = data[2]
            t4 = data[3].strip('\n') # Strip very last data point's new line character

            # Create a row
            row = {wr.fieldnames[0]: o1, wr.fieldnames[1]: o2, wr.fieldnames[2]: t3, wr.fieldnames[3]: t4}

            if len(row) != 0: # Check if a row has been parsed then add to the csv file
                wr.writerow(row)

    shutil.move(f'{outputFile}', f'process_scans/{type.lower()}') # Moves the newly created CSV file to processing folder

    os.remove(inputFile) # Delete temporary text file

    return outputFile # Return the name of the output file
 
# Attempts to get the video urls from the server
def getVideoUrl():
    url = config.get('WEB_URL', 'URL') + config.get('WEB_URL', 'Video')
    token = turtle.simpledialog.askstring("Get Token", "Please enter your token")
    response = requests.get(url, headers={'Authorization':f'Bearer {token}'})

    # print(response) # DEBUG
    return response.json(), token

# Attempts to send a datafile to the server
def sendFileToServer(fileName, token):
    dataFile = open(fileName, "rb") # Open the dataFile as a binary file

    url = config.get('WEB_URL', 'URL') + config.get('WEB_URL', 'Results')

    requests.post(url, data=dataFile, headers={'Authorization': f'Bearer {token}'})
    
    # print(response) # DEBUG

# Checks directories for matching names
# Need standard, trad, female, male inside user_scans and process_scans
def checkDirs():
    # Check if user_scans exists
    if not os.path.isdir('user_scans'):
        os.makedirs('user_scans')

    # Check if process_scans exists
    if not os.path.isdir('process_scans'):
        os.makedirs('process_scans')

    dirList = ['standard', 'trad', 'female', 'male'] # List of directories needed

    # Check user_scans and process_scans for matching directory names
    for dir in dirList:
        if not os.path.isdir(f'user_scans\\{dir}'):
            os.makedirs(f'user_scans\\{dir}')
        if not os.path.isdir(f'process_scans\\{dir}'):
            os.makedirs(f'process_scans\\{dir}')

# Runs the GenerateScans executable from data_tools (For Testing purposes)
def generateScanData():
    checkDirs()
    subprocess.call(args='start', executable='data_tools/generate_build/GenerateScans.exe') # Run the algorithm

# Runs the ClearScans executable from data_tools (For testing purposes)
def clearScanData():
    checkDirs()
    subprocess.call(args='start', executable='data_tools/clear_build/ClearScans.exe') # Run the algorithm

# Runs the compareMatch executable from data_tools (Used for creating match table)
def compareMatches():
    checkDirs()
    subprocess.call(args='start', executable='data_tools/compare_build/compareMatch.exe') # Run the algorithm

# Moves all data files from process_scans directory to user_scans directory
def moveProcessedFiles(files):
    for file in files:
        shutil.move(f"process_scans/{file[1].lower()}/{file[0]}", f'user_scans/{file[1].lower()}')

# Creates the data file from compareMatch output for sending to the server
def createMatchesFile(token):
    # Create input and output file names
    inputFile = f"{token}.txt"
    os.rename("output.txt", inputFile)
    outputFile = inputFile.strip(".txt") + ".csv"

    # Read the input file and convert to csv
    with open(inputFile) as fdin, open(outputFile, 'w', newline='') as fdout:
        wr = csv.DictWriter(fdout, fieldnames=['user1', 'user2', 'score'],
                            extrasaction='ignore')  # Create header and ignore unwanted fields

        row = {} # Initialize empty dictionary for the row

        # Read the data file line by line and parse data for csv file
        while True:
            data = fdin.readline() # Get the next line

            if not data:
                break

            data = data.split(' ') # Split up user1, user2, score

            # Add user1, user2, and score info
            user1 = data[0]
            user2 = data[1]
            score = data[2].strip('\n') # Strip very last data point's new line character

            # Create a row
            row = {wr.fieldnames[0]: user1, wr.fieldnames[1]: user2, wr.fieldnames[2]: score}

            if len(row) != 0: # Check if a row has been parsed then add to the csv file
                wr.writerow(row)

    os.remove(inputFile) # Remove the inputFile

    return outputFile # Return the name of the new CSV file

# TESTING:
# files = [("5_S.csv", "Standard"), ("5_M.csv", "Male")]
# token = "5"
# compareMatches() # Run the match algorithm
# dataFile = createMatchesFile(token) # Convert the dataFile to csv
# sendFileToServer(dataFile, token)
# moveProcessedFiles(files) # Move all files from process_scans to user_scans

# Get user information until there are no more users (exit program)
while(True):
    try:
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

            # START TO USER INTERACTION - PLAY VIDEO(S), CREATE DATA FILE(S)
            videoURLs, token = getVideoUrl() # Get the URLs for each video based on user preference
            files = [] # Stores all process file names and their types

            # Loop through each video and play for the user
            for video in videoURLs['videos']:

                # Start the signal data feature
                if sensor.is_supported_feature(SensorFeature.FeatureSignal):
                    sensor.signalDataReceived = on_signal_data_received

                videoURL = config.get('VIDEO_URL', 'URL') # Add the path
                videoURL += video # Get the video type
                type = videoURL.split('/')[5].split('.')[0] # Get the video type
                fileName = f"{token}_{type[0]}.txt" # Create the file name based on USER_ID and VIDEO_TYPE

                # Creates a temporary text file for parsing the data
                with open(fileName, 'w', newline='') as dataFile:
                    if sensor.is_supported_command(SensorCommand.CommandStartSignal):
                        sensor.exec_command(SensorCommand.CommandStartSignal) #this line prints the data
                        
                        displayMsg() # Get the user ready with a message
                        sys.stdout = dataFile  # Redirect stdout to the file
                        playVideo(videoURL, type) # Play the customer's video
                        sys.stdout = sys.__stdout__ # Stop redirect

                        sensor.exec_command(SensorCommand.CommandStopSignal)

                outputFile = createOutputCSV(fileName, type) # Create the CSV file from output text
                files.append((outputFile, type)) # Add the current file name and its type to the list

            # END TO USER INTERACTION: RUN ALGO, CREATE FINAL DATA FILE, SEND TO SERVER, MOVE PROCESSED FILES
            compareMatches() # Run the match algorithm
            dataFile = createMatchesFile(token) # Convert the dataFile to csv
            sendFileToServer(dataFile) # Attempt to send the file to the server
            moveProcessedFiles(files) # Move all files from process_scans to user_scans

            sensor.disconnect()
            print("Disconnect from sensor")
            del sensor # Garbage collection for sensor

        del scanner # Garbage collection for scanner

    # Print any errors
    except Exception as err:
        print(err)
