import json
import boto3
import urllib.parse

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        #Get transcription result from S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        
        #Only process transcription results 
        if not key.endswith('.json'):
            return {'statusCode': 200, 'body': 'Not a transcription file'}
        
        response = s3.get_object(Bucket=bucket, Key=key)
        transcription_data = json.loads(response['Body'].read())

        #Extract transcript
        transcript = transcription_data['results']['transcripts'][0]['transcript'].lower()

        #Parsing commands
        if 'start' in transcript and 'server' in transcript:
            result = start_server()
        elif 'stop' in transcript and 'server' in transcript:
            result = stop_server()
        else:
            result = f"Command not recognized: {transcript}"
        
        return {
            'statusCode': 200,
            'body': json.dumps({'command': transcript, 'result': result})
        }