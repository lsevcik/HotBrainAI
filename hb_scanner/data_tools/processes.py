import subprocess, os

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
