// Created by Shane Drydahl
// Updated by Tucker Shaw on 11/4/2023
#include <string>
#include <vector>
#include <iostream>
#include <filesystem>
#include <fstream>
#include <cmath>
#include <cctype>
#include <iomanip>
using namespace std;
namespace fs = filesystem;

/**
 * @brief Struct containing user info
 * userMatchID is the ID of the user in user_scans being matched with processed
 * matchAvg is the average from the current match
 */
struct userMatch
{
    string userMatchID;
    float matchAvg;
};

/**
 * @brief Struct contains all users info
 * userID is the userID of the user being processed
 * allMatches contains each user in user_scans that the user has matched with
 * size is the current # of matches for the processed user
 */
struct user
{
    string userID;
    vector<userMatch> allMatches;
    int size; // Stores the # of matches user currently has
};

vector<user> allUserMatches; // Global vector for all user matches in process_scans

/**
 * @brief targetFolder will return the path to the current video directory
 * S -> Standard
 * T -> Trad
 * M -> Male
 * F -> Female
 * 
 * @param vid 
 * @return string 
 */
string targetFolder(char vid) {
    string path0 = "standard";
    string path1 = "trad";
    string path2 = "male";
    string path3 = "female";

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
 * @brief Checks allMatches vector for the current processed user in case their match already exists 
 *        If it finds an existing match it will update the average and return true (false if not)
 * 
 * @param compUser 
 * @param it1 
 * @param avg
 * @return bool
 */
bool find_matchUser_ID(string compUser, float avg, vector<user>::iterator it1)
{
    vector<userMatch>::iterator it2;
    bool flag = false;

    for(it2 = it1->allMatches.begin(); it2 != it1->allMatches.end() && !flag; it2++)
        {
            if(it2->userMatchID == compUser)
            {
                it2->matchAvg = (it2->matchAvg + avg) / 2;
                flag = true;
            }
        }

    return flag;
}

/**
 * @brief Checks allUserMatches vector for the current processed user in case they already exist
 * 
 * @param procUser 
 * @return vector<user>::iterator 
 */
vector<user>::iterator find_user_ID(string procUser)
{
    vector<user>::iterator it; // Create an iterator

    // Check all processed users for a match, return the iterator if match is found
    for(it = allUserMatches.begin(); it != allUserMatches.end(); it++)
        if(it->userID == procUser)
            return it;
    
    return it; // No match is found, returns the end of the vector
}

/**
 * @brief Displays all the matches that were processed
 * 
 */
void viewAllMatches()
{
    // std::cout << "Processed User ID | Compared User ID | Average" << endl; // Table header (DEBUG)

    ofstream fout;
    fout.open("output.txt");

    // Loop through all processed users and display their matched users and averages
    for(vector<user>::iterator it1 = allUserMatches.begin(); it1 != allUserMatches.end(); it1++)
    {
        for(vector<userMatch>::iterator it2 = it1->allMatches.begin(); it2 != it1->allMatches.end(); it2++)
        {
            fout << it1->userID << ' ' << it2->userMatchID << ' ' << it2->matchAvg << endl; // Display info
        }
    }
}

/**
 * @brief Stores each match into the allUserMatches vector (Will eventually be the database)
 * 
 * @param procUser 
 * @param compUser 
 * @param average 
 */
void storeMatches(string procUser, string compUser, float average){
    
    bool flag;

    // Store the match if needed in a vector
    vector<userMatch> currentMatch;
    currentMatch.push_back({compUser, average});

    vector<user>::iterator it = find_user_ID(procUser); // Check for user in set

    if(it != allUserMatches.end()) // User already in set
    {
        flag = find_matchUser_ID(compUser, average, it);
        
        if(!flag)
        {
            it->allMatches.push_back({compUser, average}); // Add match to it's set
            it->size++;
        }
    } 
    else // User not in set
        allUserMatches.push_back({procUser, currentMatch, 1}); // Add user and it's match to the set, also update the size
}

/**
 * @brief Comparison Algorithm: Processes the file in process_scans and user_scans to create the average
 * 
 * @param processFile 
 * @param compareFile 
 */
void processFile(fs::path processFile, fs::path compareFile) {
    string line1 = "";
    string line2 = "";

    fstream in1(processFile);
    fstream in2(compareFile);


    // Maths
    float O1_1;
    float O1_2;
    float O2_1;
    float O2_2;
    float T3_1;
    float T3_2;
    float T4_1;
    float T4_2;

    // Variables
    float O1;
    float O2;
    float T3;
    float T4;
    float sum;
    float sqroot;


    // Vector for holding row calculations and commas
    vector<float> rowSquares;
    vector<int> commas1;
    vector<int> commas2;


    int samples = 0;
    if(in1.is_open() && in2.is_open()) {
        while (getline(in1, line1) && getline(in2, line2)) {
            samples++;
            for (int i = 0; i < line1.length(); i++) {
                if (line1.at(i) == ',') {
                    commas1.push_back(i);
                }
            }
            for (int i = 0; i < line2.length(); i++) {
                if (line2.at(i) == ',' || line2.at(i) == '\n') {
                    commas2.push_back(i);
                }
            }

            commas1.push_back(line1.length() - 1);
            commas2.push_back(line2.length() - 1);

            O1_1 = stof(string(&line1[0], &line1[commas1.at(0)]));
            O1_2 = stof(string(&line2[0], &line2[commas2.at(0)]));

            O1 = powf((O1_1 - O1_2), 2);

            O2_1 = stof(string(&line1[commas1.at(0) + 1], &line1[commas1.at(1)]));
            O2_2 = stof(string(&line2[commas2.at(0) + 1], &line2[commas2.at(1)]));
            O2 = powf((O2_1 - O2_2), 2);

            T3_1 = stof(string(&line1[commas1.at(1) + 1], &line1[commas1.at(2)]));
            T3_2 = stof(string(&line2[commas2.at(1) + 1], &line2[commas2.at(2)]));
            T3 = powf((T3_1 - T3_2), 2);

            T4_1 = stof(string(&line1[commas1.at(2) + 1], &line1[commas1.at(3)]));
            T4_2 = stof(string(&line2[commas2.at(2) + 1], &line2[commas2.at(3)]));

            T4 = powf((T4_1 - T4_2), 2);

            sum = O1 + O2 + T3 + T4;
            sqroot = sqrt(sum);
            rowSquares.push_back(sqroot);
            sqroot = 0;


            commas1.clear();
            commas2.clear();
        }
    }


    float sqrSums = 0;
    for (float nums: rowSquares) {
        sqrSums += nums;
    }

    string tempName = processFile.filename().string();
    string processUser = tempName.substr(0, tempName.find_last_of('_'));

    string tempName2 = compareFile.filename().string();
    string compareUser = tempName2.substr(0, tempName2.find_last_of('_'));

    // cout << "Processed User ID: " << processUser << endl; // Debug
    // cout << "Compared User ID: " << compareUser << endl; // Debug

    storeMatches(processUser, compareUser, (sqrSums / (float) samples));

    // cout << "Samples: " << samples << endl; // Debug
    // cout << "AVERAGE = " << sqrSums / (float)samples << endl << endl; // Debug

}

int main() {
    // Get the current path for process_scans and user_scans
    fs::path procDir = fs::current_path();
    fs::path userScans = fs::current_path();

    // Declare variables
    char currProcFile;
    string currFileName;

    // Set process_scans directory name
    if (procDir.filename() != "process_scans") {
        procDir /= "process_scans";
    }

    // Set user_scans directory name
    if (userScans.filename() != "user_scans") {
        userScans /= "user_scans";
    }

    // cout << "Process: " << procDir << endl; // Debug
    // cout << "UserScan: " << userScans << endl; // Debug

    // Loop through each type of directory in process_scans (S, T, M, F) to find files needed for processing
    for (const auto &type: fs::directory_iterator(procDir)) {
        currFileName = type.path().string();
        currProcFile = toupper(currFileName.at(currFileName.rfind('\\') + 1));

        // cout << "File Path:" << currFileName << endl;   // Debug
        // cout << "File Types:" << currProcFile << endl;  // Debug

        userScans /= targetFolder(currProcFile);
        // cout << "  =====================" + userScans.string() + "===================" << endl;  // Debug

        procDir /= targetFolder(currProcFile);
        // cout << "  =====================" + procDir.string() + "===================" << endl;  // Debug

        // Loop through each file in process_scans directories and user_scans directories and run the algo
        for(const auto &entry_1: fs::directory_iterator(type))
        {
            for (const auto &entry_2: fs::directory_iterator(userScans)) {
                processFile(entry_1, entry_2);
            }
        }

        // Reset each path variable
        while (userScans.filename() != "user_scans") {
            userScans = userScans.parent_path();
        }
        while (procDir.filename() != "process_scans") {
            procDir = procDir.parent_path();
        }
    }

    viewAllMatches(); // Display all the matches in a table

    return 0;
}
