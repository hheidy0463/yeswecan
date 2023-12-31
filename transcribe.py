from os import path
import time
import sys

# regex
import re

# video-editing library
from moviepy.editor import *

# speech-to-text library
import requests

# transcribe audio file    
def transcribe(file):
    if file[-3:] == "mp4": 
        print("mp4 detected")
        mp3 = file[:-3] + "mp3"
        f = open(mp3, "w+")
        convert_mp3(file, mp3)
    elif file[-3:] == "mp3":
        print("mp3 detected")
    else:
        print("invalid file format")
        return

    # upload local file
    headers = {
        "authorization": "aa22022ab90d4f619444d01386317bcc",
    }
    response1 = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(mp3))  
    f.close()
    json1 = response1.json()
    url = json1.get("upload_url")

    audio_url = {"audio_url": url}

    # submit for transcription
    endpoint1 = "https://api.assemblyai.com/v2/transcript"
    response2 = requests.post(endpoint1, json=audio_url, headers=headers)
    id = response2.json().get("id")
    
    # check status of transcription
    endpoint2 = "https://api.assemblyai.com/v2/transcript/" + id
    response3 = requests.get(endpoint2, headers=headers)
    status = response3.json().get("status")

    while status != "completed":
        time.sleep(20)
        response3 = requests.get(endpoint2, headers=headers)
        json3 = response3.json()
        status = response3.json().get("status")
    
    transcript = json3.get("text")
    
    return transcript

# extracts audio from mp4 and puts it into an mp3 file
def convert_mp3(mp4, mp3):
    vid = VideoFileClip(mp4)

    aud = vid.audio
    aud.write_audiofile(mp3)

    vid.close()
    aud.close()

# reading file with AssemblyAI
def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

if __name__ == '__main__':
    print(transcribe("/Users/danieltsan/Downloads/databases.mp4"))
    
