#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <cstdio>
#include <httplib.h>

using namespace std;

class AudioService {
    private:
        string outputDirectory;
    public:
        AudioService(const string &directoryName){
            outputDirectory = directoryName;
            string command = "mkdir -p " + outputDirectory;
            system(command.c_str());
        }
        bool saveAudio(vector <char> audioData, string fileName){
            string filePath = outputDirectory + "/" + fileName;
            ofstream file(filePath.c_str(), ios::binary);
            if (!file.is_open()){
                cerr << "Failed to create file: " << filePath << endl;
                return false;
            }
            for (int i = 0; i < audioData.size(); ++i){
                file << audioData[i];
            }
            file.close();
            printf("Audio saved to %s\n", filePath.c_str());
            return true;
        }