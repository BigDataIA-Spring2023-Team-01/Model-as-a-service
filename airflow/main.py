import boto3
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
# import os
# from dotenv import load_dotenv
# load_dotenv()

AWS_ACCESS_KEY_ID = Variable.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = Variable.get('AWS_SECRET_KEY')

# S3 buckets
RAW_MP3_BUCKET = Variable.get('raws3Bucket')
PROCESSED_TRANSCRIPT_BUCKET = Variable.get('processedTranscriptBucket')
CHAT_GPT_DEFAULT_BUCKET = 'chatgptdefault'

# Whisper API client
token = Variable.get('OPENAI_SECRET_KEY')

# Boto3 S3 client
s3_client = boto3.client('s3',
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# DAG settings
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('whisper_chatgpt_dag', default_args=default_args, schedule_interval=None)

def whisper(file):
    url = "https://api.openai.com/v1/audio/transcriptions"

    payload={'model': 'whisper-1'}
    files={
      'file': file

    }
    headers = {
      'Authorization': 'Bearer ' + token
    }


    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.text
def get_transcript_from_whisper(audio_file_key):
    audio_file = s3_client.get_object(Bucket=RAW_MP3_BUCKET, Key=audio_file_key)['Body'].read()
    
    transcript = whisper(audio_file)
    
    return transcript

def my_chatgpt_function(transcript, default_questions=True):
    questions = ['What is the Project about?','How many team members are there?','How long will the project take?']
    test = 'jakhsdjhas3hdjkahsdkjahkdshakhdkjhakd'
    return test


def run_chatgpt_default(context):
    transcript_file_key = context['task_instance'].xcom_pull(task_ids='transcribe_audio')
    transcript = s3_client.get_object(Bucket=PROCESSED_TRANSCRIPT_BUCKET, Key=transcript_file_key)['Body'].read()
    

    chatgpt_results = my_chatgpt_function(transcript, default_questions=True)
    
    chatgpt_results_key = f'{transcript_file_key}-chatgpt-default.txt'
    s3_client.put_object(Bucket=CHAT_GPT_DEFAULT_BUCKET, Key=chatgpt_results_key, Body=chatgpt_results)
    
    return chatgpt_results_key

#  tasks
transcribe_audio_task = PythonOperator(
    task_id='transcribe_audio',
    python_callable=get_transcript_from_whisper,
    op_kwargs={'audio_file_key': 'test'},
    dag=dag
)

run_chatgpt_default_task = PythonOperator(
    task_id='run_chatgpt_default',
    python_callable=run_chatgpt_default,
    provide_context=True,
    dag=dag
)

transcribe_audio_task >> run_chatgpt_default_task
