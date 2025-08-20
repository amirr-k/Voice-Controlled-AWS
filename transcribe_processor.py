import json
import boto3
import urllib.parse

transcribe = boto3.client('transcribe')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Get bucket and key from S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

        # Start transcription job
        jobName = f"transcribe-{key.replace('/', '-').replace('.', '-')}"
        jobURI = f"s3://{bucket}/{key}"
        
        transcribe.start_transcription_job(
            TranscriptionJobName=jobName,
            Media={'MediaFileUri': jobURI},
            MediaFormat='wav',
            LanguageCode='en-US',
            OutputBucketName=bucket
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Transcription job started')
        }

    except Exception as e:
        print(f"Error: {e}")
        raise e