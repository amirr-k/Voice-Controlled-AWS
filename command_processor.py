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
        transcriptionData = json.loads(response['Body'].read())

        #Extract transcript
        transcript = transcriptionData['results']['transcripts'][0]['transcript'].lower()

        #Parsing commands
        if 'start' in transcript and 'server' in transcript:
            result = startServer()
        elif 'stop' in transcript and 'server' in transcript:
            result = stopServer()
        else:
            result = f"Command not recognized: {transcript}"
        
        return {
            'statusCode': 200,
            'body': json.dumps({'command': transcript, 'result': result})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def startServer():
    #Start EC2 instance
    instanceId = "IF THIS IF FAILING YOU FORGOT TO REPLACE ME!"
    try:
        ec2.start_instances(InstanceIds=[instanceId])
        return "Server started"
    except Exception as e:
        return f"Error starting server: {str(e)}"

def stopServer():
    #Stop EC2 instance
    instanceId = "IF THIS IF FAILING YOU FORGOT TO REPLACE ME!"
    try:
        ec2.stop_instances(InstanceIds=[instanceId])
        return "Server stopped"
    except Exception as e:
        return f"Error stopping server: {str(e)}"
