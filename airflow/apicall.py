import requests
from airflow.models import Variable
import os
from dotenv import load_dotenv
load_dotenv()
url = os.environ.get("AIRFLOW_URL")

# Replace <USERNAME> and <PASSWORD> with your Airflow credentials if authentication is enabled
auth = ("team01", "team01af")
headers = {"Content-Type": "application/json"}
data = {"conf": {"filename": 'Recording.mp3'}}

response = requests.post(url, headers=headers, json=data, auth=auth)

print(response.text)