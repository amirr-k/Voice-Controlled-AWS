import json
import boto3
import requests
import base64

def lambda_handler(event, context):
    #Get audio from API Gateway
    try:
        if event.get("isBase64Encoded"):
            #Convert to binary
            audioData = base64.b64decode(event["body"])
        else:
            audioData = event["body"]
            #Already in binary format
    
    #Send audio to C++ service
    #Need to make this dynamic later
        cppServiceUrl = "http://localhost:8080/process"

        response = requests.post(cppServiceUrl, files = {"audio": ("record.wav", audioData, "audio/wav")})

        return {'statusCode': 200,'headers': {'Access-Control-Allow-Origin': '*','Content-Type': 'application/json'},
            'body': json.dumps({'message': response.text,'status': 'success'})}

        
    except Exception as e:
        return {'statusCode': 500,'body': json.dumps({'error': str(e)})}