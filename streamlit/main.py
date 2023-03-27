import streamlit as st
import pandas as pd
from io import StringIO
import os
import boto3
import sys
import io

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------



st.header("Model As A Service")

audio_file = st.file_uploader("Attach an audio file", type = 'mp3', on_change = None)

st.button("Upload Button")
# if audio_file:
#     st.write(audio_file.name)

# st.set_option('deprecation.showfileUploaderEncoding', False)
def upload_to_s3(file, bucket_name):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).put_object(Key=file.name, Body=file)
# def upload_to_s3(file, bucket_name, key):
#     s3.upload_fileobj(file, bucket_name, key)

# # Create S3 client
# s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# # if uploaded_file is not None:
    

# #     # Read uploaded file as bytes
# #     file_bytes = uploaded_file.read()

# #     # Create BytesIO object from file bytes
# #     audio_file = [io.BytesIO(file_bytes)]

# #     # Set name attribute of BytesIO object
# #     # audio_file[0].name = f"{file_name}.mp3"

# #     # Upload file to S3
# #     bucket_name = "rawmp3"
# #     key = f"{file_name}.mp3"
# #     upload_to_s3(audio_file[0], bucket_name, key)

# #     # Display success message to user
# #     st.success(f"{file_name}.mp3 was uploaded to S3!")

# Check if a file was uploaded
if audio_file is not None:
    # Extract file name from uploaded file
    # file_name = st.text_input("Enter filename for ")
    # Upload the file to S3 bucket
    upload_to_s3(audio_file, BUCKET_NAME)
    # Rename the file with .mp3 extension
    os.rename(file_name, file_name + ".mp3")
    st.write("File uploaded successfully!")
else:
    st.write("Please upload an MP3 file.")


st.markdown("-------")


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