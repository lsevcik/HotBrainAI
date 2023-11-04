// Created by Shane Drydahl
// Updated by Tucker Shaw on 11/4/2023
#include <string>
#include <filesystem>
using namespace std;
namespace fs = filesystem;

/**
 * @brief Returns the path to the specified video directory
 * 
 * @param num 
 * @return string 
 */
string targetFolder(int num) {
    string path0 = "standard";
    string path1 = "trad";
    string path2 = "male";
    string path3 = "female";

    switch (num) {
        case 0:
            return path0;
        case 1:
            return path1;
        case 2:
            return path2;
        default:
            return path3;
    }
}

int main() {
    // Get the current path for process_scans and user_scans
    fs::path workDir = fs::current_path();
    fs::path procDir = fs::current_path();

    // Set the path for user_scans
    if (workDir.filename() != "user_scans") {
        workDir /= "user_scans";
    }

    // Set the path for process_scans
    if(procDir.filename() != "process_scans") {
        procDir /= "process_scans";
    }

    // Loop through each directory and remove the files
    for (int i = 0; i < 4; i++) {
        workDir /= targetFolder(i);
        procDir /= targetFolder(i);

        for (const auto &entry: fs::directory_iterator(workDir)) {
            remove(entry.path());
        }
        workDir = workDir.parent_path();

        for (const auto &entry: fs::directory_iterator(procDir)) {
            remove(entry.path());
        }
        procDir = procDir.parent_path();
    }
    return 0;
}