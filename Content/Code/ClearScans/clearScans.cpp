#include <string>
#include <filesystem>

namespace fs = filesystem;

using namespace std;

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
    fs::path workDir = fs::current_path();

    if (workDir.filename() != "user_scans") {
        workDir /= "user_scans";
    }

    for (int i = 0; i < 4; i++) {
        workDir /= targetFolder(i);

        for (const auto &entry: fs::directory_iterator(workDir)) {
            remove(entry.path());
        }
        workDir = workDir.parent_path();
    }
    return 0;
}