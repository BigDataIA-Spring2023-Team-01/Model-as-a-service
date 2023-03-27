import sys
import requests
import os
from dotenv import load_dotenv
import boto3
import io


load_dotenv()
#---------------------------------------------------------------------------------------------------------------
#                            Connection Declarations
#---------------------------------------------------------------------------------------------------------------
#
s3 = boto3.client('s3',region_name='us-east-1',
                            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                            aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))

raws3Bucket = os.environ.get('raws3Bucket')

#---------------------------------------------------------------------------------------------------------------
#                            Variable Declarations
#---------------------------------------------------------------------------------------------------------------
#
filepath = 'data/Missed class summaryt.mp3'
s3_object = s3.get_object(Bucket=raws3Bucket, Key='Recording.mp3')
audio_data = s3_object['Body']
file_key = 'Recording.mp3'
#---------------------------------------------------------------------------------------------------------------
#                            Calling API
#---------------------------------------------------------------------------------------------------------------
#

def whisper(filepath):
    token = os.environ.get('OPENAI_SECRET_KEY')
    url = "https://api.openai.com/v1/audio/transcriptions"

    payload={'model': 'whisper-1'}
    # files={
    #   ('file',(io.BytesIO(result),'audio/mpeg'))
    #   # 'file': open('data/Recording.mp3','rb'),
    #   # 'file1': open('data/Missed class summaryt.mp3','rb')

    # }
    files = {'file': (file_key, audio_data)}

    headers = {
      'Authorization': 'Bearer ' + token
    }


    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)


whisper(filepath)
# s3.upload_file(r'data/Missed class summaryt.mp3', raws3Bucket,'rawfile')