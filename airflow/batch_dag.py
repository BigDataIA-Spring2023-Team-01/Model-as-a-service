import os
import boto3
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import requests
import io
from io import BytesIO

import json
# Set up AWS credentials
aws_access_key_id = Variable.get('AWS_ACCESS_KEY')
aws_secret_access_key = Variable.get('AWS_SECRET_KEY')
token = Variable.get('OPENAI_SECRET_KEY')
BATCH_RAW_MP3 = Variable.get('batchrawmp3')
PROCESSED_TRANSCRIPT_BUCKET = Variable.get('processedTranscriptBucket')
CHAT_GPT_RESULTS = 'chatgptresults'
start_prompt = 'The following is a transcript of a zoom recording and you are a bot which will use the following transcript as context and answer questions relating to that meeting.'
prompts = [
    "Please provide a brief summary of the meeting.",
    "What was the main topic of discussion during the meeting?",
    "What were some of the key points discussed during the meeting?",
    "Can you describe any action items or next steps that were discussed during the meeting?",
    "What were the opinions or thoughts of each team member on the topic of discussion?",
]

# Set up AWS clients
s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key)

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
    print(response.text)
    answer = response.json()["choices"][0]["message"]["content"].strip()

    return answer

# Define function for Task 1
def read_all_files_from_s3():


    url = "https://api.openai.com/v1/audio/transcriptions"
    response = s3_client.list_objects_v2(Bucket=BATCH_RAW_MP3)
    all_transcripts = {}
    for file in response['Contents']:
        filename = file['Key']
        file_obj = s3_client.get_object(Bucket=BATCH_RAW_MP3, Key=filename)
        file_data = file_obj['Body'].read() 

        payload={'model': 'whisper-1','response_format':'text'}
        files = {'file': (filename, file_data)}
        headers = { 'Authorization': 'Bearer ' + token}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
    
        transcript = response.text
        all_transcripts[filename] = transcript

    return all_transcripts


# Define function for Task 2
def write_to_s3(ti):

    all_transcripts = ti.xcom_pull(task_ids=['read_all_files_from_s3'])
    print(all_transcripts)
    for filename,transcript in all_transcripts[0].items():

        key = filename.split('.')[0]
        s3_client.put_object(Body=transcript.encode(), Bucket=PROCESSED_TRANSCRIPT_BUCKET, Key=key)

    return 'Success'

# Define function for Task 3
def call_chatgpt(ti):
    all_transcripts = ti.xcom_pull(task_ids=['read_all_files_from_s3'])   
    for filename,transcript in all_transcripts[0].items():

        
        key = filename.split('.')[0]

        results = {}
        for question in prompts:
            answer = ask_question(question, transcript)
            results[question] = answer

        # Store the results in JSON format in S3 bucket
        data = json.dumps(results)
        s3_client.put_object(Key=key, Body=data,Bucket=CHAT_GPT_RESULTS)

    return 'Success'

# Define function for Task 4

def clean_ups3(ti):
    all_transcripts = ti.xcom_pull(task_ids=['read_all_files_from_s3'])
    
    for filename in all_transcripts[0]:
        
        response = s3_client.delete_object(Bucket=BATCH_RAW_MP3, Key=filename)
        if response['ResponseMetadata']['HTTPStatusCode'] == 204:
            print(f'The object with key {filename}  was deleted from bucket "{BATCH_RAW_MP3}"')
        else:
            print(f'There was an error deleting the object with key {filename}  from bucket "{BATCH_RAW_MP3}"')
    
    return "Completed cleanup"



default_args = {
    'start_date': datetime(2023, 3, 27),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'batch_mp3_bucket': 'batchrawmp3'
}

# Define the DAG
dag = DAG('batch_dag', description='Batch DAG for processing audio files from batch s3 bucket with Whisper.ai and ChatGPT',
          schedule_interval=None, default_args=default_args,catchup=False)

# Define the tasks
task1 = PythonOperator(task_id='read_all_files_from_s3', python_callable=read_all_files_from_s3, dag=dag)
task2 = PythonOperator(task_id='write_to_s3', python_callable=write_to_s3, dag=dag)
task3 = PythonOperator(task_id='call_chatgpt', python_callable=call_chatgpt, dag=dag)
task4 = PythonOperator(task_id='clean_ups3', python_callable=clean_ups3, dag=dag)

# Define the task dependencies
task1 >> task2 >> task3 >> task4
