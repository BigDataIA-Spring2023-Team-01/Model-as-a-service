#
import requests
from dotenv import load_dotenv
import os
import json
token = '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'

def test_api():
    
    url = "https://api.openai.com/v1/audio/transcriptions"

    payload={'model': 'whisper-1','response_format':'json'}

    files = {'file': ('Recording.txt', '../data/download.jpeg')}
    headers = {
      'Authorization': 'Bearer ' + token
    }


    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    response_json = response.json()
    print(response_json)
    assert response.status_code == 400


def test_chatgpt_api():
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": f'Bearer {token}'}
  

    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
          {
            "role": "system",
            "content": "I am shamin i am a student at northestern university"
          },
          {
            "role": "user",
            "content": "Question:where does shamin study?"
          },
          {
            "role": "user",
            "content": "Answer?"
          }
        ],
        "max_tokens": 700,
        "n": 1
    })

    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        assert True
    else:
        print(f"API error ({response.status_code}): {response.json()['error']}")
        assert False

