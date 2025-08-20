import json
import boto3
import base64
from datetime import datetime

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    #Get audio from API Gateway
    try:
        # Get audio from API Gateway
        if event.get("isBase64Encoded"):
            #Convert to binary
            audioData = base64.b64decode(event["body"])
        else:
            audioData = event["body"]
            #Already in binary format
    
        timestamp = int(datetime.now().timestamp())
        filename = f"audio_{timestamp}.wav"

        s3_client.put_object(
            Bucket='voice-recordings-bucket-amirkiadi-2025',
            Key=filename,
            Body=audioData,
            ContentType='audio/wav'
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': f'Audio uploaded successfully: {filename}',
                'status': 'success'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }