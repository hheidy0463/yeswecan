
# api.py
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin
from transcribe import transcribe
from translate import translate_text
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app, origins='*')
app.config['videoUploads'] = 'uploads'
os.makedirs(app.config['videoUploads'], exist_ok=True)

@app.route('/', methods=['POST'])
@cross_origin()
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    uploaded_file = request.files['videoFile']

    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['videoUploads'], filename)
        uploaded_file.save(file_path)

    return redirect(url_for('index'))

@app.route('/', methods=['POST'])
@cross_origin()
def transcribe_endpoint():
    data = request.get_json()
    video_file = data.get('videoFile')
    result = transcribe(video_file)
    return jsonify({'transcription': result})

@app.route('/', methods=['POST'])
@cross_origin()
def translate_endpoint():
    data = request.get_json()
    text = data.get('text')
    target = data.get('target', 'en')
    result = translate_text(target, text)
    return jsonify({'translation': result})

if __name__ == '__main__':
    app.run(port=5000)
