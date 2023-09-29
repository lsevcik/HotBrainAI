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

const int MAX_MATCHES = 10; // For checking if user has more than 10 matches already

struct userMatch
{
    string userMatchID;
    float matchAvg;
};

struct user
{
    string userID;
    vector<userMatch> allMatches;
    int size; // Stores the # of matches user currently has
};

vector<user> allUserMatches; // Global vector for user matches

string targetFolder(char vid) {
    string path0 = "standard/";
    string path1 = "trad/";
    string path2 = "male/";
    string path3 = "female/";

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

// Checks allUserMatches vector for the current processed user in case they already exist
vector<user>::iterator find_user_ID(string procUser)
{
    vector<user>::iterator it;

    for(it = allUserMatches.begin(); it != allUserMatches.end(); it++)
        if(it->userID == procUser)
            return it;
    
    return it;
}

// Displays all the matches that were processed
void viewAllMatches()
{
    std::cout << "Processed User ID | Compared User ID | Average" << endl;

    for(vector<user>::iterator it1 = allUserMatches.begin(); it1 != allUserMatches.end(); it1++)
    {
        for(vector<userMatch>::iterator it2 = it1->allMatches.begin(); it2 != it1->allMatches.end(); it2++)
        {
            std::cout << setw(14) << it1->userID << setw(18) << it2->userMatchID << setw(14) << it2->matchAvg << endl;
        }
    }
}

// Stores each match into the allUserMatches vector (Will eventually be the database)
void storeMatches(string procUser, string compUser, float average){
    // Store the match if needed
    vector<userMatch> currentMatch;
    currentMatch.push_back({compUser, average});

    vector<user>::iterator it = find_user_ID(procUser); // Check for user in set

    if(it != allUserMatches.end()) // User already in set
    {
        it->allMatches.push_back({compUser, average}); // Add match to it's set
        it->size++;
    } 
    else // User not in set
        allUserMatches.push_back({procUser, currentMatch, 1}); // Add user and it's match to the set, also update the size

    // std::cout << "MatchAvg:  " << current[0].matchAvg << endl;
    // std::cout << procUser << " | " << compUser << " | average: " << average << endl;
}


void processFile(fs::path processFile, fs::path compareFile) {
//    cout << "Process File:" << processFile.string() << endl;
//    cout << "Compare File:" << compareFile.string() << endl;
//    string inPath =
//    string path =

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


//    // Vector for holding row calculations
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
                if (line2.at(i) == ',') {
                    commas2.push_back(i);
                }
            }
//            for(int ns : commas1){
//                cout << ns << ", ";
//            }
//            cout << endl;

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
//            cout << "ROW: " << sqroot << "  ||  "  << sum << endl;
            rowSquares.push_back(sqroot);
            sqroot = 0;


            commas1.clear();
            commas2.clear();
        }
    }


    float sqrSums = 0;
    for (float nums: rowSquares) {
//        cout << nums << endl;
        sqrSums += nums;
    }

    string tempName = processFile.filename().string();
    string processUser = tempName.substr(0, tempName.find_last_of('_'));

    string tempName2 = compareFile.filename().string();
    string compareUser = tempName2.substr(0, tempName2.find_last_of('_'));

    cout << "Processed User ID: " << processUser << endl;
    cout << "Compared User ID: " << compareUser << endl;

    storeMatches(processUser, compareUser, (sqrSums / (float) samples));

//    cout << "Samples: " << samples << endl;
    cout << "AVERAGE = " << sqrSums / (float)samples << endl << endl;

}


int main() {
    fs::path procDir = fs::current_path();
    fs::path userScans = fs::current_path();

    char currProcFile;
    string currFileName;

    if (procDir.filename() != "process_scans") {
        procDir /= "process_scans";
    }

    if (userScans.filename() != "user_scans") {
        userScans /= "user_scans";
    }

    cout << "Process: " << procDir << endl;
    cout << "UserScan: " << userScans << endl;

    for (const auto &type: fs::directory_iterator(procDir)) {
        currFileName = type.path().string();
        currProcFile = toupper(currFileName.at(currFileName.rfind('/') + 1));
        cout << "===================================================================================================="
             << endl;

        cout << "File Path:" << currFileName << endl;   // Debug
        cout << "File Types:" << currProcFile << endl;  // Debug



        userScans /= targetFolder(currProcFile);
        cout << "  =====================" + userScans.string() + "===================" << endl;  // Debug

        procDir /= targetFolder(currProcFile);
        cout << "  =====================" + procDir.string() + "===================" << endl;  // Debug

        for(const auto &entry_1: fs::directory_iterator(type))
        {
            for (const auto &entry_2: fs::directory_iterator(userScans)) {
                // cout << entry_1.path() << endl;
                // cout << entry_1 << ' ' << entry << endl;
                processFile(entry_1, entry_2);
            }
        }

        while (userScans.filename() != "user_scans") {
            userScans = userScans.parent_path();
        }
        while (procDir.filename() != "process_scans") {
            procDir = procDir.parent_path();
        }
        cout << endl << endl;
    }

    viewAllMatches();

    return 0;
}