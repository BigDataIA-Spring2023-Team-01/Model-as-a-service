import sys
import os
import boto3
import requests
from dotenv import load_dotenv
import json
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
KEY = 'Recording.mp3'

def whisper():
    token = os.environ.get('OPENAI_SECRET_KEY')
    url = "https://api.openai.com/v1/audio/transcriptions"

    payload={'model': 'whisper-1'}
    # files={
    #   ('file',(io.BytesIO(result),'audio/mpeg'))
    #   # 'file': open('data/Recording.mp3','rb'),
    #   # 'file1': open('data/Missed class summaryt.mp3','rb')

    # }
    filepath = f'data/sound_recordings/{KEY}'
    files = {'file': r'filepath'}

    headers = {
      'Authorization': 'Bearer ' + token
    }


    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)

# s3.download_file(
#     Bucket=raws3Bucket,
#     Key=KEY,
#     Filename=f'data/sound_recordings/{KEY}'
# )

response = s3.list_objects_v2(Bucket=raws3Bucket)
print(response['Contents'])