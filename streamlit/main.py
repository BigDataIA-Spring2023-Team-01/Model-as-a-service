# importing libraries 
import streamlit as st
import pandas as pd
from io import StringIO
import os
import boto3
import sys
import io
import requests
import json
from dotenv import load_dotenv
import base64

#------------------------------------------------------------------------------------------------------------------------------------
# loading environment variables 
load_dotenv()
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')
token = os.environ.get("OPENAI_SECRET_KEY")

#------------------------------------------------------------------------------------------------------------------------------------
# defining s3 clients 
s3client = boto3.client('s3',region_name='us-east-1',
                        aws_access_key_id = AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

#------------------------------------------------------------------------------------------------------------------------------------
# defining various s3 buckets 
USER_BUCKET_NAME = os.environ.get("raws3Bucket") # bucket in which audio files goes
PROCESSED_BUCKET = s3.Bucket('processedtranscript') # bucket with the audio transcript in it 
GPTRESULTS_BUCKET = 'chatgptresults' # bucket with generic question in it

#------------------------------------------------------------------------------------------------------------------------------------
# streamlit page 
#Title
st.header("Recording Summariser 🔊📝")

# setting up the background image 
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background(r"C:\Users\user\OneDrive\Desktop\DAMG_7245\Model-as-a-service\streamlit\download.jpeg")
#File Uploader
audio_file = st.file_uploader("Attach an audio file", type = 'mp3')

# Triggering the adhoc dag
def triggerDAG(filename:str):
    url = os.environ.get("AIRFLOW_URL")
    auth = ("team01", "team01af")
    headers = {"Content-Type": "application/json"}
    data = {"conf": {"filename": filename}}

    response = requests.post(url, headers=headers, json=data, auth=auth)

    return response.status_code

# Check if a file was uploaded or not 
if audio_file is not None:
    
    if st.button("Upload Button"):
        s3client.upload_fileobj(audio_file, USER_BUCKET_NAME, audio_file.name)
        st.success("File uploaded successfully!", icon="✅")
        status = triggerDAG(audio_file.name)
        if status == 200:
            st.write("AdHoc DAG Triggered")
    else:
        st.write("Please upload an MP3 file.")

# Processed audio file 
st.markdown("-------")

# Selecting audio files for context
file_names = [obj.key for obj in PROCESSED_BUCKET.objects.all()]
selected_file = st.selectbox('Select a file', file_names)
file_name = selected_file

if selected_file:
   bucket = s3.Bucket(GPTRESULTS_BUCKET)
#    file_name = selected_file
try:
        obj = s3.Object(GPTRESULTS_BUCKET, file_name)
        contents = obj.get()['Body'].read().decode('utf-8')
        data = json.loads(contents)
        for key, value in data.items():
            st.markdown(f"<p style='font-weight: bold;'>{key}: </p><p>{value}</p>", unsafe_allow_html=True)
        #st.write(data)
except:
    st.error("Failed to read file from S3 bucket.")
    st.text_area('Generic Transcript Questionnaire',
                 '''
    1. What was the meeting about? 
    2. How many people participated?
    3. What was the conclusion of the discussion''', on_change = None)
   
#------------------------------------------------------------------------------------------------------------------------------------
# Defining Various Funtions 
#------------------------------------------------------------------------------------------------------------------------------------
# asking question using whisper api 

def ask_question(question, context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    openai_api_endpoint = "https://api.openai.com/v1/chat/completions"

    payload = json.dumps({
"model": "gpt-3.5-turbo",
"messages": [
    {
    "role": "system",
    "content": context
    },
    {
    "role": "user",
    "content": f"Question:{question}"
    },
    {
    "role": "user",
    "content": "Answer?"
    }
],
"max_tokens": 700,
"n": 1
})
    
    response = requests.post(openai_api_endpoint, headers=headers, data=payload)
    print("here")
    print(response.text)
    answer = response.json()["choices"][0]["message"]["content"].strip()
    return answer

   
bucket_name = 'processedtranscript'
file_url = 'https://s3.console.aws.amazon.com/s3/object/{}?region=us-east-1&prefix={}'.format(bucket_name,file_name)

s3_object = s3client.get_object(Bucket=bucket_name, Key=file_name)
file_content = s3_object['Body'].read().decode('utf-8')

#-----------------------------------------------------------------------------
#Streamlit Page Continue
# asking questions using whisper api 
question = st.text_input("Ask a question")
if st.button("Ask Button"):
    answer = ask_question(file_content, question)
    st.text_area('Answer to question asked:', value = answer)

