import json
import boto3
import urllib.parse

transcribe = boto3.client('transcribe')
s3 = boto3.client('s3')