
# api.py
from flask import Flask, flash, request, jsonify, redirect, url_for, Response
from flask_cors import CORS, cross_origin
from transcribe import transcribe
from translate import translate_text
from werkzeug.utils import secure_filename
import os
import sys

app = Flask(__name__)
CORS(app, origins='*')
app.config['videoUploads'] = 'videos'
os.makedirs(app.config['videoUploads'], exist_ok=True)

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    if 'videoFile' not in request.files:
        return jsonify({'error': 'No file part'})

    uploaded_file = request.files['videoFile']

    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.root_path, app.config['videoUploads'], filename)
        print(f"File path: {file_path}", file=sys.stdout)
        uploaded_file.save(file_path)

    return jsonify({'filePath': file_path})

# route should match what your frontend calls it
# POST should also have OPTIONS 
@app.route('/transcribe', methods=['POST'])
@cross_origin()
def transcribe_endpoint():
    data = request.get_json()
    video_file = data.get('videoFile')
    result = transcribe("videos/" + video_file)
    return jsonify({'transcription': result})

@app.route('/translate', methods=['POST'])
@cross_origin()
def translate_endpoint():
    data = request.get_json()
    text = data.get('text')
    target = data.get('target', 'en')
    result = translate_text(target, text)
    return jsonify({'translation': result})

if __name__ == '__main__':
    app.run(port=5000)
