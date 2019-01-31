#include <fstream>
#include <iostream>
#include <string>
#include <cctype>

int main() {
    std::ifstream fout("user_out");
    std::ifstream fans("answer");

    std::string s1, s2;
    std::getline(fout, s1);
    std::getline(fans, s2);

    bool ok = true;

    if (s1.length() != s2.length()) {
        std::cerr << "Output length differs." << std::endl;
        ok = false;
    } else {
        for (size_t i = 0; i < s1.length(); i++) {
            if (tolower(s1[i]) != tolower(s2[i])) {
                std::cerr << "The " << i + 1 << "-th character differs. Expected '" << s2[i] << "'; got '" << s1[i] << "'." << std::endl;
                ok = false;
            }
        }
    }
    if (ok) {
        std::cerr << "OK!" << std::endl;
    }
    std::cout << (ok ? 100 : 0) << std::endl;
}
