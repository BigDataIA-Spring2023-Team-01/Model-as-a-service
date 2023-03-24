from openapi import uploadTos3
import streamlit as st
import pandas as pd
from io import StringIO
import os
from dotenv import load_dotenv
import boto3

load_dotenv()
raws3Bucket = os.environ.get('raws3Bucket')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    uploadTos3(uploaded_file,raws3Bucket,'samplemp3')

    

    