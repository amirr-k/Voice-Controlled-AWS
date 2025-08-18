import json
import boto3
import requests
import base64

def lambda_handler(event, context):
    #Get audio from API Gateway
    try:
        if event.get("isBase64Encoded"):
            #Convert to binary
            audio_data = base64.b64decode(event["body"])
        else:
            body = event["body"]
            #Already in binary format
    
    #Send audio to C++ service
    #Need to make this dynamic later
    cppServiceUrl = "http://localhost:8080/process"

    response = response.post(cppServiceUrl, files = {"audio": ("record.wav", body, "audio/wav")})

    
