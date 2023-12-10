#include <string>
#include <iostream>
#include <filesystem>
#include <fstream>
#include <cmath>
#include <chrono>
#include <mutex>
#include <condition_variable>
#include <vector>
#include <future>
#include <thread>

using namespace std;
namespace fs = filesystem;

int numFiles = 0;  // DEBUG

const auto processor_count = std::thread::hardware_concurrency();  // Get number of cores for current CPU

// Used to ensure synchronization between processing threads
class Semaphore {
public:
    explicit Semaphore(int count) : count_(count) {}

    inline void notify() {
        std::unique_lock<std::mutex> lock(mtx_);
        count_++;
        cv_.notify_one();
    }

    inline void wait() {
        std::unique_lock<std::mutex> lock(mtx_);
        while(count_ == 0) {
            cv_.wait(lock);
        }
        count_--;
    }

private:
    std::mutex mtx_;
    std::condition_variable cv_;
    int count_;
};

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
bool find_matchUser_ID(const string& compUser, float avg, vector<user>::iterator it1)
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
vector<user>::iterator find_user_ID(const string& procUser)
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
//     std::cout << "Processed User ID | Compared User ID | Average" << endl; // Table header (DEBUG)

    ofstream fout;
    fout.open("output.txt");

    // Loop through all processed users and display their matched users and averages
    for(auto &iter : allUserMatches)
    {
        for(auto it2 = iter.allMatches.begin(); it2 != iter.allMatches.end(); it2++)
        {
            fout << iter.userID << ' ' << it2->userMatchID << ' ' << it2->matchAvg << endl; // Display info
        }
    }
    fout.close();
}

/**
 * @brief Stores each match into the allUserMatches vector (Will eventually be the database)
 *
 * @param procUser
 * @param compUser
 * @param average
 */
void storeMatches(const string& procUser, const string& compUser, float average){
    bool flag;
//    cout << procUser << " | " << compUser << " | AVERAGE: " << average << "\n";  // DEBUG

    // Store the match if needed in a vector
    vector<userMatch> currentMatch;
    currentMatch.push_back({compUser, average});

    auto it = find_user_ID(procUser); // Check for user in set

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


double parseDoubleFromString(const string& str, int start, int length) {
    double result = 0.0;
    bool negative = false;
    bool decimalFound = false;
    double fractionFactor = 1.0;
    vector<double> num;

    for (int i = start; i < start + length; ++i) {
        char c = str[i];
        if (c == '-') {
            negative = true;
        } else if (c == '.') {
            decimalFound = true;
        } else if (c >= '0' && c <= '9') {
            if (decimalFound) {
                fractionFactor *= 0.1;
                result += (c - '0') * fractionFactor;
            } else {
                result = result * 10.0 + (c - '0');
            }
        }
    }
    return negative ? -result : result;
}

double calcRow(const string& L1, const string& L2, const vector<int>& com1, const vector<int>& com2) {
    double sum = 0.0;
    double LM1, LM2;
    for (int i = 0; i < 4; i++) {
        int start1 = com1[i] + ((i == 0) ? 0 : 1);
        int length1 = com1[i + 1] - start1;
        LM1 = parseDoubleFromString(L1, start1, length1);

        int start2 = com2[i] + ((i == 0) ? 0 : 1);
        int length2 = com2[i + 1] - start2;
        LM2 = parseDoubleFromString(L2, start2, length2);

        double diff = LM1 - LM2;
        sum += diff * diff;  // Directly squaring the difference
    }
    return sum;
}

/**
 * @brief Comparison Algorithm: Processes the file in process_scans and user_scans to create the average
 *
 * @param processFile
 * @param compareFile
 */
static void processFile(const fs::path& processFile, const fs::path& compareFile) {
    string line1;
    string line2;

    fstream in1(processFile);
    fstream in2(compareFile);

    double sum;
    double sqroot;

    // Vector for holding row calculations
    vector<double> rowSquares;
    vector<int> commas1;
    vector<int> commas2;

    int samples = 0;
    if (in1.is_open() && in2.is_open()) {
        while (getline(in1, line1) && getline(in2, line2)) {
            samples++;

            commas1.push_back(0);
            commas2.push_back(0);
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
            sum = calcRow(line1, line2, commas1, commas2);

            sqroot = sqrt(sum);
            rowSquares.push_back(sqroot);
            sqroot = 0;

            commas1.clear();
            commas2.clear();
        }
    }
    in1.close();
    in2.close();

    double sqrSums = 0;
    for (double nums: rowSquares) {
        sqrSums += nums;
    }

    string tempName = processFile.filename().string();
    string processUser = tempName.substr(0, tempName.find_last_of('_'));

    string tempName2 = compareFile.filename().string();
    string compareUser = tempName2.substr(0, tempName2.find_last_of('_'));

    storeMatches(processUser, compareUser, float(sqrSums / samples));
}

void proc(const fs::path& P1, const fs::path& P2, vector<future<void>>& futures, Semaphore& sem) {
    for (const auto& entry: fs::directory_iterator(P1)) {
        for (const auto &entry_2: fs::directory_iterator(P2)) {
            sem.wait(); // Wait for available slot
            futures.push_back(std::async(std::launch::async, [&sem](const fs::path& file1, const fs::path& file2) {
                processFile(file1, file2);
                sem.notify(); // Release slot
                numFiles++;   // DEBUG
            }, entry, entry_2));
        }
    }
}

int main() {
    // Timers to test efficiency
//    typedef std::chrono::high_resolution_clock Time;              // DEBUG
//    typedef std::chrono::milliseconds ms;                         // DEBUG
//    typedef std::chrono::duration<float> fsec;                    // DEBUG
//    auto t0 = Time::now();                                        // DEBUG

    fs::path procDir = fs::current_path();
    fs::path userScans = fs::current_path();
    fs::path userScans_Default = fs::current_path();

//    string curPa[] = {"trad", "standard", "male", "female"};
//    char currProcFile;
    string currFileName;

    if (procDir.filename() != "process_scans") {
        procDir /= "process_scans";
    }

    if (userScans.filename() != "user_scans") {
        userScans /= "user_scans";
        userScans_Default /= "user_scans";
    }

    Semaphore sem(static_cast<int>(processor_count)); // Based on the number of cores available
    vector<future<void>> futures;

    for (const auto &entry_1: fs::directory_iterator(procDir)) {
        fs::path currentCategory = entry_1.path().filename();
        fs::path userScansTemp = userScans / currentCategory;
        proc(entry_1, userScansTemp, futures, sem);
    }

    // Wait for all async tasks to complete
    for (auto &f : futures) {
        f.get();
    }

    viewAllMatches(); // Display all the matches in a table

//    cout << "NUM OF FILES: " << numFiles << endl;                               // DEBUG
//    cout << "NUMBER OF THREADS AVAIL: " << processor_count << endl;             // DEBUG
//    auto t1 = Time::now();                                                      // DEBUG
//    fsec fs = t1 - t0;                                                          // DEBUG
//    std::cout << fs.count() << "s\n";                                           // DEBUG
    return 0;
}