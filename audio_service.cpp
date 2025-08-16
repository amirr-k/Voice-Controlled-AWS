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
            return "Success, audio uploaded to S3";
        }
        AudioService* globalService = nullptr;
        void healthCheck(const httplib::Request& req, httplib::Response& res){
            res.set_content("C++ Audio Service running", "text/plain");
            printf("Health check requested\n");
        }
        void handleProcessAudio(const httplib::Request& req, httplib::Response& res){
            printf("Audio processing requested\n");
            auto file = req.get_file_value("audio");
            if (!file){
                res.status = 400;
                res.set_content("No audio file provided", "text/plain");
                printf("Error: No audio file provided\n");
                return;
            }
            printf("Received audio file: %s (%d bytes)\n", 
            file->filename.c_str(), (int)file->content.size());
            vector<char> audioData;
            for (int i = 0; i < file->content.size(); ++i){
                audioData.push_back(file->content[i]);
            }
            string result = globalService->processAudio(audioData);
            res.set_content(result, "text/plain");
            printf("Response: %s\n", result.c_str());
        }
        // Handles CORS
        // Notes to self:
        // Cross-Origin Resource Sharing (CORS)
        // Allows requests from different origins
        // Ie. if this service is running on a different domain than the frontend
        // Like localhost:3000 and localhost:8080
        // This allows the frontend to make requests to the backend
        httplib::Server::HandlerResponse handleCORS(const httplib::Request& req, httplib::Response& res) {
            res.set_header("Access-Control-Allow-Origin", "*");
            res.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
            res.set_header("Access-Control-Allow-Headers", "Content-Type");
            return httplib::Server::HandlerResponse::Unhandled;
        }


        

int main() {
    // Create audio service instance, can change directory name later
    AudioService service("./audiofiles");
    globalService = &service;
    // Create HTTP server
    httplib::Server server;

   
     
    

    return 0;
}



