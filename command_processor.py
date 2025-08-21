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
        
        #Only process transcription results (not audio files)
        if not key.endswith('.json'):
            return {'statusCode': 200, 'body': 'Not a transcription file'}