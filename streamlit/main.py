
# from openapi import uploadTos3

import streamlit as st
import pandas as pd
from io import StringIO
import os
# from dotenv import load_dotenv
# from dotenv import load_dotenv
import boto3
import sys

# @ -24,6 +27,7 @@ processedTranscriptBucket = os.environ.get('processedTranscriptBucket')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# load_dotenv()


# @ -37,7 +41,46 @@ if uploaded_file is not None:

#     st.success('File Upload Successful')
    # uploadTos3(uploaded_file,raws3Bucket,'samplemp3')
# load_dotenv()
# raws3Bucket = os.environ.get('raws3Bucket')

# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:

#     uploadTos3(uploaded_file,raws3Bucket,'samplemp3')
st.header("Model As A Service")
# col1, col2 = st.beta_columns(2)


# with col1:
# col3, col4 = st.columns(2)
# with col3:
st.file_uploader("Attach an audio file", type = 'mp3', accept_multiple_files = True, on_change = None)

# with col4:
st.button("Upload Button")


st.markdown("-------")

# with col2:
options = ['Processed Audio List', 'Recording_2', 'Recording_3']
selected_option = st.selectbox("Select Processed Audio from the list", options)

if options:
    st.text_area('Generic Transcript Questionnaire',
                 '''
        1. What was the meeting about? 
        2. How many people participated?
        3. What was the conclusion of the discussion''', on_change = None)
    

    st.text_input('Enter a question to answer related to the meeting', on_change = None)

    st.button("Ask Button")