# Voice-Controlled AWS Manager

A voice-driven interface for managing AWS resources. This project enables users to record speech in the browser, upload it to a backend pipeline for transcription, and trigger AWS actions such as starting or stopping EC2 instances.

## Project Structure

```
voice-aws-manager/
├── frontend/                  # Browser-based recorder
│   ├── recorder.js            # Handles audio recording & upload
│   ├── recorder.css           # UI styles for recording/processing states
│   └── assets/                # Icons and static assets
├── backend/
│   ├── lambda_function.py     # AWS Lambda entrypoint
│   ├── transcribe_processor.py# Handles AWS Transcribe job results
│   ├── command_processor.py   # Parses transcript into AWS API calls
│   └── Dockerfile             # Container config (alternative deployment option)
├── audio_service.cpp          # Prototype for native audio service (unused in final impl.)
└── README.md
```

## Prerequisites

- Node.js 18+
- Python 3.10+
- AWS account with:
  - Amazon Transcribe
  - AWS Lambda
  - Amazon EC2
- Browser supporting the MediaRecorder API (tested in Chrome & Safari)

## Environment

Backend requires AWS credentials (IAM role or keys) with permissions for Transcribe and EC2.  
Frontend expects an API Gateway endpoint exposed for `/upload-audio`.

Example `.env` for frontend:

```
REACT_APP_API_URL=https://your-api-gateway-url.amazonaws.com/test
```

## Install & Run

### Frontend

```bash
cd frontend
npm install
npm start
```

The app runs at: http://localhost:3000

### Backend

Deploy Lambda functions with their Python dependencies.  

## Features

- Voice Recording – Browser-based recorder using MediaRecorder API with recording/processing states.
- AWS Transcribe Integration – Audio uploaded to Amazon S3, which triggers an Amazon Transcribe job
- Command Parsing – Natural language parsed into AWS API calls (start, stop EC2).
- Secure Uploads – Audio sent securely via API Gateway.

## Example Flow

1. User clicks microphone, recording starts  
2. Audio blob uploaded to API Gateway endpoint 
3. API Gateway endpoint invokes `lambda_function.py`
4. `lambda_function.py` places audio in Amazon S3
5. MP4 Files uploaded to S3 trigger Amazon Transcribe
6. Amazon Transcribe returns parsed audio in the form of .json to S3
7. .json files trigger `command_processor.py` lambda function 
8. `command_processor.py` parses text (e.g., “start EC2 instance”)

## Alternative Architecture: C++ + Dockerfile

An earlier design explored using C++ (`audio_service.cpp`) with Dockerized deployment:

### Pros
- Low-level audio handling and codec control.
- Containerization ensures reproducibility and simplified Lambda packaging.

### Cons (why it wasn’t chosen)
- Added complexity: bridging C++ with AWS Lambda/Transcribe required extra bindings.
- Slower iteration: Python (boto3) + JavaScript enabled faster prototyping compared to C++.
- Limited browser integration: MediaRecorder API already provides cross-platform audio capture without needing C++.

### Final Choice

Python + React offered the best balance between development speed, maintainability, and AWS integration.  
C++ remains in the repo as a prototype reference but was not needed for production.
 
