import requests
import os
from dotenv import load_dotenv
import boto3

load_dotenv()
#---------------------------------------------------------------------------------------------------------------
#                            Connection Declarations
#---------------------------------------------------------------------------------------------------------------
#
s3 = boto3.client('s3',region_name='us-east-1',
                            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                            aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))

raws3Bucket = os.environ.get('raws3Bucket')
processedTranscriptBucket = os.environ.get('processedTranscriptBucket')
filepath = r'data/Missed class summaryt.mp3'
files={
      ('file',('Missed class summaryt.mp3',open(filepath,'rb'),'audio/mpeg'))
      # 'file': open('data/Recording.mp3','rb'),
      # 'file1': open('data/Missed class summaryt.mp3','rb')

    }
#---------------------------------------------------------------------------------------------------------------
#                            Function Declarations
#---------------------------------------------------------------------------------------------------------------
#

def uploadTos3(filepath,bucket,key):
    s3.upload_file(filepath, bucket,key)

uploadTos3(filepath,raws3Bucket,'samplemp3')

