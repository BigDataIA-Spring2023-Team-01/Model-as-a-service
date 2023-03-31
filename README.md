# Model-as-a-service
A model-as-a-service project 


Streamlit Link - https://bigdataia-spring2023-team-01-model-as-a-se-streamlitmain-mxcf4d.streamlit.app/

Airflow Link - http://35.237.121.118:8080/home

Documentation Link - https://codelabs-preview.appspot.com/?file_id=19xyGJumh98_N7z0qhKBeTg10asxw79QeTDVa_zSGbFs/edit#0

The objective of this project is to develop a user-friendly and interactive Streamlit application that allows users to upload audio of their choice and ask questions related to the content of the audio. The application will utilize advanced audio processing techniques to extract meaningful information from the audio, which will be used to generate relevant questions for the user to select from or to provide a platform for users to input their own custom questions.
Users will have the flexibility to choose from various audio and upload them to the application with ease. Once the audio is uploaded, the application will automatically process it to extract relevant information and provide with some generic questions.
The application will provide an intuitive user interface, allowing users to easily navigate and ask questions related to the audio content. Additionally, the application will have the functionality to store previous audios, making it easy for users to retrieve and access them at a later time.
Overall, this Streamlit application will offer a unique and efficient platform for users to explore audio content and ask questions that are relevant and meaningful to them.

# Steps to run the code
1. Open terminal
2. Browse the location where you want to clone the repository
3. Write the following command and press enter 
````
  git clone https://github.com/BigDataIA-Spring2023-Team-01/Model-as-a-service.git
 ````
 4. Create a virtual environment using the following command
 ````
  python -m venv <Virtual_environment_name>
 ````
 5. Activate the virtual environment and download the requirements.txt using
 ````
  pip install -r /path/to/requirements.txt
 ````
 6. Run the Streamlit application.(cd to the root of the project /Model-as-a-service)
 ````
  streamlit run streamlit/main.py
 ````
# Reference 
./airflow

This folder cotains the adhocg dag and bacth dag files 

./data 

This folder contains the audio recordings and the images used in the project

./openapi

This folder contains the files integrating the whisper API with airflow dags

./streamlit 

This folder contains the streamlit application files
# Declaration 
Contribution 
 
1. Anandita Deb : 25%
2. Cheril Yogi :25%
3. Shamin Chokshi :25%
4. Thejas Bharadwaj :25%
 
WE ATTEST THAT WE HAVEN'T USED ANY OTHER STUDENT'S WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.
