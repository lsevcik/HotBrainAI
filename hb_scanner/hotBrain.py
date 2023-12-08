from sdk_tools.scanner import Scanner
from cmn_types import *
import concurrent.futures
from time import sleep
from hotBrain_tools.hotBrain_tools import displayMsg, playVideo, createOutputCSV, getVideoUrl, sendFileToServer, moveProcessedFiles, createMatchesFile
from data_tools.processes import compareMatches
import sys, configparser

# Read config file for server communication
config = configparser.ConfigParser()
config.read(r'config.cfg')

# Event handler for scan finding a headband, prints sensor info
def sensor_found(sensors):
    for index in range(len(sensors)):
        print('Sensor found: %s' % sensors[index])

# Event handler for headband state changing, prints the state
def on_sensor_state_changed(sensor, state):
    print('Sensor {0} is {1}'.format(sensor.name, state))

# Event handler for signal data being recieved
def on_signal_data_received(data):
    for i in range(len(data)):
        print(data[i].O1, data[i].O2, data[i].T3, data[i].T4)

# Event handler for device connection
def device_connection(sensor_info):
    return Scanner.create_sensor(sensor_info)

# Main function that runs the backend process for HotBrain application
# Get user information until there are no more users (exit program)
def startUserProcess():
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

            while(True): # TODO: Change this to a looping system
                # START TO USER INTERACTION - PLAY VIDEO(S), CREATE DATA FILE(S)
                videoURLs, token = getVideoUrl(config) # Get the URLs for each video based on user preference
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
                sendFileToServer(config, dataFile, token) # Attempt to send the file to the server
                moveProcessedFiles(files) # Move all files from process_scans to user_scans

                # TODO: Needs to disconnect after all users finished (after while loop from above)
                # Disconnect the current sensor
                sensor.disconnect()
                print("Disconnect from sensor")
                del sensor # Garbage collection for sensor

        del scanner # Garbage collection for scanner

    # Print any errors
    except Exception as err:
        print(err)
        