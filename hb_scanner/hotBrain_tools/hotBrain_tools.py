import ctypes, cv2, csv, os, shutil, requests
from tkinter import messagebox

# Creates a simple message box window
# Warns the user that the video is about to start
def displayMsg(type):
    messagebox.showwarning(f"{type}", "Ready to proceed?") # Display warning before video is shown

# Function to play a video for testing the headband
def playVideo(videoURL, type):
    windowName = type # Name of the video window (video type)
    
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
def getVideoUrl(HB_GUI, config):
    url = config.get('WEB_URL', 'URL') + config.get('WEB_URL', 'Video')
    token = HB_GUI.createTokenPopUp() # Create pop up window and get user input
    response = requests.get(url, headers={'Authorization':f'Bearer {token}'})
    return response.json(), token

# Attempts to send a datafile to the server
def sendFileToServer(config, fileName, token):
    dataFile = open(fileName, "rb") # Open the dataFile as a binary file
    url = config.get('WEB_URL', 'URL') + config.get('WEB_URL', 'Results')
    requests.post(url, data=dataFile, headers={'Authorization': f'Bearer {token}'})

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
