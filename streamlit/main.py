import streamlit as st
import pandas as pd
from io import StringIO
import os
import boto3
import sys
import io
import requests

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


s3client = boto3.client('s3',region_name='us-east-1',
                        aws_access_key_id = AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

st.header("Model As A Service")

audio_file = st.file_uploader("Attach an audio file", type = 'mp3')


# Check if a file was uploaded
if audio_file is not None:
    
    if st.button("Upload Button"):
        s3client.upload_fileobj(audio_file, USER_BUCKET_NAME, audio_file.name)
        st.success("File uploaded successfully!", icon="✅")
    else:
        st.write("Please upload an MP3 file.")

def whisper_api(question, transcript_url):
    # Define the API endpoint and headers
    endpoint = "https://api.whisper.ai/v1/ask"
    headers = {"Authorization": "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"}

    # Define the request payload
    data = {
        "question": question,
        "audio_url": transcript_url
    }

    # Call the API
    response = requests.post(endpoint, headers=headers, json=data)

    # Return the response
    return response.json()["answer"]

def main():
    # Create a file uploader in Streamlit
    # uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])
    question = st.text_input("Ask a question")

    # If a file is uploaded by the user and a question is entered
    if audio_file is not None and question != "":

        # Get the URL of the uploaded file
        transcript_url = f"https://s3.amazonaws.com/processedtranscript/{audio_file.name}"

        # Call the Whisper API to generate a response to the question
        response = whisper_api(question, transcript_url)

        # Display the response to the user
        st.write(f"Question: {question}")
        st.write(f"Response: {response}")


if __name__ == "__main__":
    main()






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