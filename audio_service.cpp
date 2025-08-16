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
        bool uploadS3(string fileName){
            string filePath = outputDirectory + "/" + fileName;
            string s3Path = "s3://" + outputDirectory + "/" + fileName;
            string command = "aws s3 cp" + filePath + " " + s3Path;
            printf("Uploading audio to S3: %s\n", s3Path.c_str());

            int result = system(command.c_str());
            if (result == 0){
                printf("Uploaded audio to S3: %s\n", s3Path.c_str());
            }
            else {
                printf("Failed to upload audio to S3: %s\n", s3Path.c_str());
                return false;
            }
            return true;
        }
        string processAudio(vector <char> audioData){
            time_t now = time(0);
            char timestamp[20];
            sprintf(timestamp, "%ld", now);
            string fileName = "audio_" + string(timestamp) + ".wav";
            if (!saveAudio(audioData, fileName)){
                return "Error: Failed to save audio file";
            }
            if (!uploadS3(fileName)){
                return "Error: Failed to upload audio to S3";
            }
            return "Sucess, audio uploaded to S3";
        }



