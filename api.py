
# api.py
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS, cross_origin
from transcribe import transcribe
from translate import translate_text
from database import firebase

import os
import sys

app = Flask(__name__)

CORS(app, origins='*')
app.config['videoUploads'] = 'videos/'
os.makedirs(app.config['videoUploads'], exist_ok=True)

"""
@app.route('/')
def main():
    return render_template('src/home.html')
"""

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    if 'videoFile' not in request.files:
        return redirect(request.url)

    uploaded_file = request.files.get('videoFile')

    if uploaded_file.filename == '':
        return redirect(request.url)
    
    if uploaded_file:
        file_path = os.path.join(app.config['videoUploads'], uploaded_file.filename)
        uploaded_file.save(file_path)

    return jsonify({'filePath': file_path})

# route should match what your frontend calls it
# POST should also have OPTIONS 
@app.route('/transcribe', methods=['POST', 'OPTIONS'])
@cross_origin()
def transcribe_endpoint():
    data = request.get_json()
    video_file = data.get('videoFile')
    result = transcribe("videos/" + video_file)
    return jsonify({'transcription': result})

@app.route('/translate', methods=['POST', 'OPTIONS'])
@cross_origin()
def translate_endpoint():
    data = request.get_json()
    text = data.get('text')
    target = data.get('target', 'en')
    result = translate_text(target, text)
    return jsonify({'translation': result})

@app.route('/create_lecture', methods=['POST', 'OPTIONS'])
@cross_origin()
def create_lecture_endpoint():
    firestore_client = firebase.Firebase()
    data = request.get_json()
    className = data["className"]
    title = data["lectureTitle"]
    data = {"original transcript": data["transcript"]}
    firestore_client.create_lecture(className, title, data)
    return 'created lecture'

@app.route('/update_lecture', methods=['POST', 'OPTIONS'])
@cross_origin()
def update_lecture_endpoint():
    firestore_client = firebase.Firebase()
    data = request.get_json()
    className = data["className"]
    title = data["lectureTitle"]
    data = {data["selectedLanguage"]: data["translation"]}
    firestore_client.create_lecture(className, title, data)
    return 'updated lecture'

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
