import json
import boto3
import base64
from datetime import datetime

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        #Get audio from API Gateway
        if event.get("isBase64Encoded"):
            #Convert to binary
            body = base64.b64decode(event["body"])
        else:
            body = event["body"].encode() if isinstance(event["body"], str) else event["body"]
        
        #Extract actual audio from multipart form data
        contentType = event.get('headers', {}).get('content-type', '') or event.get('headers', {}).get('Content-Type', '')
        
        if 'multipart/form-data' in contentType:
            boundary = contentType.split('boundary=')[1].encode()
            parts = body.split(b'--' + boundary)
            
            audioData = None
            for part in parts:
                if b'name="audio"' in part:
                    headerEnd = part.find(b'\r\n\r\n')
                    if headerEnd != -1:
                        audioData = part[headerEnd + 4:]
                        if audioData.endswith(b'\r\n'):
                            audioData = audioData[:-2]
                        break
            
            if not audioData:
                audioData = body
        else:
            audioData = body
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
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
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