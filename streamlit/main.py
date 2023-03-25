import streamlit as st
import pandas as pd
from io import StringIO
import os
from dotenv import load_dotenv
import boto3
import sys




#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#                               Temp



s3 = boto3.resource('s3',region_name='us-east-1',
                            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                            aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))

raws3Bucket = os.environ.get('raws3Bucket')
processedTranscriptBucket = os.environ.get('processedTranscriptBucket')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

load_dotenv()


st.title('Welcome to our Model-as-a-service Application')

uploaded_file = st.file_uploader("Choose a Audio file to process")
if uploaded_file is not None:


    s3.meta.client.upload_file(uploaded_file, raws3Bucket,uploaded_file.name)

    st.success('File Upload Successful')
    # uploadTos3(uploaded_file,raws3Bucket,'samplemp3')

    

    