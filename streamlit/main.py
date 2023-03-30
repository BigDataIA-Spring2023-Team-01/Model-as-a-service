import streamlit as st
import pandas as pd
from io import StringIO
import os
import boto3
import sys
import io
import requests
import json
# from airflow import batch_dag
from dotenv import load_dotenv
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

load_dotenv()
USER_BUCKET_NAME = os.environ.get("raws3Bucket")

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')

token = os.environ.get("OPENAI_SECRET_KEY")


s3client = boto3.client('s3',region_name='us-east-1',
                        aws_access_key_id = AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

st.header("Recording Summariser 🔊📝")

audio_file = st.file_uploader("Attach an audio file", type = 'mp3')

def triggerDAG(filename:str):
    url = os.environ.get("AIRFLOW_URL")
    auth = ("team01", "team01af")
    headers = {"Content-Type": "application/json"}
    data = {"conf": {"filename": filename}}

    response = requests.post(url, headers=headers, json=data, auth=auth)

    return response.status_code

# Check if a file was uploaded
if audio_file is not None:
    
    if st.button("Upload Button"):
        s3client.upload_fileobj(audio_file, USER_BUCKET_NAME, audio_file.name)
        st.success("File uploaded successfully!", icon="✅")
        status = triggerDAG(audio_file.name)
        if status == 200:
            st.write("AdHoc DAG Triggered")

    else:
        st.write("Please upload an MP3 file.")
 
    
st.markdown("-------")

s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
buckets3 = s3.Bucket('processedtranscript')
file_names = [obj.key for obj in buckets3.objects.all()]
selected_file = st.selectbox('Select a file', file_names)


if selected_file:
    s3 = boto3.resource('s3',aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    bucket_name_ = 'chatgptresults'
    bucket = s3.Bucket(bucket_name_)

    file_name = selected_file
    
    try:
        obj = s3.Object(bucket_name_, file_name)
        contents = obj.get()['Body'].read().decode('utf-8')
        data = json.loads(contents)
        for key, value in data.items():
            st.markdown(f"<p style='font-weight: bold;'>{key}: </p><p>{value}</p>", unsafe_allow_html=True)
        #st.write(data)
    except:
        st.error("Failed to read file from S3 bucket.")
   
    


    


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



question = st.text_input("Ask a question")
if st.button("Ask Button"):
    answer = ask_question(file_content, question)
    st.text_area('Answer to question asked:', value = answer)
