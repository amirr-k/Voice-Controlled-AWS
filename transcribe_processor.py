import json
import boto3

transcribe = boto3.client('transcribe')

def lambda_handler(event, context):
    print("🚀 Lambda triggered by S3 event:", json.dumps(event))
    
    try:
        # extract bucket + key
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        print(f"Processing file s3://{bucket}/{key}")
        
        job_name = f"transcribe-{key.replace('.', '-')}"
        job_uri = f"s3://{bucket}/{key}"
        
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='mp4',  
            LanguageCode='en-US',
            OutputBucketName='voice-recordings-bucket-amirkiadi-2025'
        )
        
        print(f"Started Transcribe job: {job_name}")
        
    except Exception as e:
        print(f"Error in transcribe-processor: {str(e)}")
        raise