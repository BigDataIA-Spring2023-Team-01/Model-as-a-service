import os
import boto3
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime
import requests
import io
from io import BytesIO

import json
# Set up AWS credentials
aws_access_key_id = Variable.get('AWS_ACCESS_KEY')
aws_secret_access_key = Variable.get('AWS_SECRET_KEY')
token = Variable.get('OPENAI_SECRET_KEY')
RAW_MP3_BUCKET = Variable.get('raws3Bucket')
PROCESSED_TRANSCRIPT_BUCKET = Variable.get('processedTranscriptBucket')
CHAT_GPT_RESULTS = 'chatgptresults'
user_input = {
        "filename": "Recording.mp3"
        }

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
def read_from_s3(**kwargs):
    filename = kwargs['dag_run'].conf['filename']
    s3_object = s3_client.get_object(Bucket=RAW_MP3_BUCKET, Key=filename)
    audio_data = s3_object['Body']


    url = "https://api.openai.com/v1/audio/transcriptions"

    payload={'model': 'whisper-1'}
    files = {'file': (filename, audio_data)}

    headers = {
      'Authorization': 'Bearer ' + token
    }


    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    transcript = response.text

    return transcript


# Define function for Task 2
def write_to_s3(transcript,**kwargs):
    fileToWrite = kwargs['dag_run'].conf['filename']
    result = fileToWrite.split('.')[0]
    s3_client.put_object(Body=transcript.encode(), Bucket=PROCESSED_TRANSCRIPT_BUCKET, Key=result)

# Define function for Task 3
def call_chatgpt(transcript,**kwargs):
    fileToWrite = kwargs['dag_run'].conf['filename']
    result = fileToWrite.split('.')[0]

    results = {}
    for question in prompts:
        answer = ask_question(question, transcript)
        results[question] = answer

    # Store the results in JSON format in S3 bucket
    data = json.dumps(results)
    s3_client.put_object(Key=result, Body=data,Bucket=CHAT_GPT_RESULTS)

    return results

# Define function for Task 4

def clean_ups3(**kwargs):
    filename = kwargs['dag_run'].conf['filename']
    response = s3_client.delete_object(Bucket=RAW_MP3_BUCKET, Key=filename)
    if response['ResponseMetadata']['HTTPStatusCode'] == 204:
        print(f'The object with key {filename}  was deleted from bucket "{RAW_MP3_BUCKET}"')
    else:
        print(f'There was an error deleting the object with key {filename}  from bucket "{RAW_MP3_BUCKET}"')
    return "Completed cleanup"



# Define the DAG
dag = DAG('adhoc_dag', description='Example DAG for processing audio file with Whisper.ai and ChatGPT',
          schedule_interval=None, start_date=datetime(2023, 3, 24),params = user_input,catchup=False)

# Define the tasks
task1 = PythonOperator(task_id='read_from_s3', python_callable=read_from_s3, dag=dag)
# task2 = PythonOperator(task_id='send_to_whisper', python_callable=whisper, dag=dag, op_kwargs={'audio_data': "{{ ti.xcom_pull(task_ids='read_from_s3') }}"})
task2 = PythonOperator(task_id='write_to_s3', python_callable=write_to_s3, dag=dag, op_kwargs={'transcript': "{{ ti.xcom_pull(task_ids='read_from_s3') }}"})
task3 = PythonOperator(task_id='call_chatgpt', python_callable=call_chatgpt, dag=dag, op_kwargs={'transcript': "{{ ti.xcom_pull(task_ids='read_from_s3') }}"})
task4 = PythonOperator(task_id='clean_ups3', python_callable=clean_ups3, dag=dag, op_kwargs={'transcript': "{{ ti.xcom_pull(task_ids='read_from_s3') }}"})

# Define the task dependencies
task1 >> task2 >> task3 >> task4
