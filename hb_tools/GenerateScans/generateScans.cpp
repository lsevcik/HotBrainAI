//
// Created by shane on 10/6/2023.
//
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <random>

#include <filesystem>
using namespace std;

namespace fs = filesystem;


int generateRandom(int LOW, int HIGH) {
    random_device dev;
    mt19937 rng(dev());
    uniform_int_distribution<int> dist6(LOW, HIGH);

    return dist6(rng);
}

long double generateRandomDouble(float LOW, float HIGH) {
    random_device rd;
    mt19937_64 gen(rd());

    uniform_real_distribution<float> dis(LOW, HIGH);

    return dis(gen);
}


// Generate a random 10 digit number, empty spaces filled with 0's
//string generateUserID() {
//    stringstream userID;
//    userID << setw(10) << setfill('0') << ((int) generateRandom(0, 99999) % (999999 - 0 + 1));
//    return userID.str();
//}

// Generate random phone number for ID
string generateUserID() {
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

int main() {
    fs::path workDir = fs::current_path();

    if (workDir.filename() != "user_scans") {
        workDir /= "user_scans";
    }

    int numberOfFiles = 0;
    string userID;

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
//        vector<char> tempVids = {'T', 'M', 'F'};
        userVideo.insert(userVideo.end(), tempVids.begin(), tempVids.end());
        userID = generateUserID();

        for (char j: userVideo) {
            currentVid = j;
            workDir /= targetFolder(j) + userID + "_" + currentVid + ".csv";
            ofstream out(workDir);

            if (currentVid == 'S') {
                currentSamples = sampleRate * standardLength;
            } else {
                currentSamples = sampleRate * supplementLength;
            }

            if (out.is_open()) {
                out << setprecision(32);
                for (int p = 1; p < currentSamples; p++) {
                    out << generateRandomDouble(-1.0, 1.0);
                    out << "," << generateRandomDouble(-1.0, 1.0);
                    out << "," << generateRandomDouble(-1.0, 1.0);
                    out << "," << generateRandomDouble(-1.0, 1.0);
                    out << "," << p+1 << endl;
                }
            } else {
                cout << "Unable to open file";
                return -1;
            }

            while(workDir.filename() != "user_scans"){
                workDir = workDir.parent_path();
            }
            out.close();
        }
    }
    return 0;
}


