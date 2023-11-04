// Created by Shane Drydahl on 10/6/2023.
// Updated by Tucker Shaw 11/4/2023
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <fstream>
#include <random>
#include <filesystem>
#include <cstdlib>
using namespace std;
namespace fs = filesystem;

/**
 * @brief Generates a random number for user ID creation
 * 
 * @param LOW 
 * @param HIGH 
 * @return int 
 */
int generateRandom(int LOW, int HIGH) {
    random_device dev;
    mt19937 rng(dev());
    uniform_int_distribution<int> dist6(LOW, HIGH);

    return dist6(rng);
}

/**
 * @brief Generates a random double for data creation
 * 
 * @param LOW 
 * @param HIGH 
 * @return long double 
 */
long double generateRandomDouble(float LOW, float HIGH) {
    random_device rd;
    mt19937_64 gen(rd());

    uniform_real_distribution<float> dis(LOW, HIGH);

    return dis(gen);
}

/**
 * @brief Generate a random 10 digit number, empty spaces filled with 0's
 * 
 * @return string
 */
string generateUserID_Number() {
   stringstream userID;
   userID << setw(10) << setfill('0') << ((int) generateRandom(0, 99999) % (999999 - 0 + 1));
   return userID.str();
}

/**
 * @brief Generates a random phone number for the user ID
 * 
 * @return string 
 */
string generateUserID_Phone() {
    string id;
    for (int i = 0; i < 10; i++) {
        if (i == 0 || i == 3) {
            id += to_string((int) generateRandom(2, 9));
        } else {
            id += to_string((int) generateRandom(0, 9));
        }
    }

    return id;
}

/**
 * @brief Generates random video types for data creation
 * 
 * @return vector<char> 
 */
vector<char> generateVideos() {
    int number = (int) generateRandom(1, 7);
    switch (number) {
        case 1:
            return {'T'};
        case 2:
            return {'M'};
        case 3:
            return {'F'};
        case 4:
            return {'T', 'M'};
        case 5:
            return {'T', 'F'};
        case 6:
            return {'M', 'F'};
        default:
            return {'T', 'M', 'F'};
    }
}

/**
 * @brief Returns the path to the specified video directory
 * 
 * @param vid 
 * @return string 
 */
string targetFolder(char vid) {
    string path0 = "standard\\";
    string path1 = "trad\\";
    string path2 = "male\\";
    string path3 = "female\\";

    switch (vid) {
        case 'S':
            return path0;
        case 'T':
            return path1;
        case 'M':
            return path2;
        default:
            return path3;
    }
}

/**
 * @brief Generates the random data and places it in the specified directory
 * 
 * @param name 
 * @param currentSamples 
 */
void generateRandomData(fs::path name, int currentSamples)
{
    ofstream out(name); // Create the file in current path

    if (out.is_open()) // Check if the file was successfully created
    {
        // Generate the data for the file
        out << setprecision(32);
        for (int p = 1; p < currentSamples; p++) 
        {
            out << generateRandomDouble(-1.0, 1.0);
            out << "," << generateRandomDouble(-1.0, 1.0);
            out << "," << generateRandomDouble(-1.0, 1.0);
            out << "," << generateRandomDouble(-1.0, 1.0);
            out << "," << p+1 << endl;
        }  
    } else // Otherwise, exit the program
    {
        cout << "Unable to open file";
        exit(0);
    }

    out.close(); // Close the file
}

int main() {
    srand(time(0)); // Set random seed

    fs::path workDir = fs::current_path();
    fs::path procDir = fs::current_path();

    if (workDir.filename() != "user_scans") {
        workDir /= "user_scans";
    }

    if (procDir.filename() != "process_scans") {
        procDir /= "process_scans";
    }

    int numberOfFiles = 0;
    string userID;
    int directory; // For specifying which directory to fill

    int sampleRate = 250;       // 250 samples taken per second
    int standardLength = 60;    // Length of standard video is 60 seconds
    int supplementLength = 30;  // Length of supplement video is 30 seconds
    int currentSamples = 0;     // Number of samples for current file

    cout << "How Many User Scans to Generate: ";
    cin >> numberOfFiles;

    char currentVid;
    cout << setprecision(32) << endl;


    for (int k = 0; k < numberOfFiles; k++) {
        vector<char> userVideo = {'S'};
        vector<char> tempVids = generateVideos();
        userVideo.insert(userVideo.end(), tempVids.begin(), tempVids.end());
        userID = generateUserID_Number();

        for (char j: userVideo) {
            currentVid = j;

            if (currentVid == 'S')
                currentSamples = sampleRate * standardLength;
            else 
                currentSamples = sampleRate * supplementLength;

            directory = rand() % 2 + 1; // Generate a random directory number to fill

            // If 1, place video in user_scans
            if(directory == 1)
            {
                workDir /= targetFolder(j) + userID + "_" + currentVid + ".csv";
                generateRandomData(workDir, currentSamples);
            }
            else // otherwise, place the video in process_scans
            {
                procDir /= targetFolder(j) + userID + "_" + currentVid + ".csv";
                generateRandomData(procDir, currentSamples);
            }

            // Reset the path that needs to be reset
            if(directory == 1)
            {
                while(workDir.filename() != "user_scans")
                    workDir = workDir.parent_path();
            } else
            {
                while(procDir.filename() != "process_scans")
                    procDir = procDir.parent_path();
            }
        }
    }
    return 0;
}


