
# api.py
from flask import Flask, flash, request, jsonify, redirect, url_for, Response, render_template
from flask_cors import CORS, cross_origin
from transcribe import transcribe
from translate import translate_text
from database import firebase

from werkzeug.utils import secure_filename
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
        flash("no file part")
        return redirect(request.url)

    uploaded_file = request.files['videoFile']

    if uploaded_file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['videoUploads'], filename)
        flash(f"File path: {file_path}")
        uploaded_file.save(file_path)

    return jsonify({'filePath': url_for('download_file', name=filename)})

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
    className = request.files["className"]
    data["language"] = request.files["selectedLanguage"]
    title = request.files["lectureTitle"]
    
    firestore_client.create_lecture(className, title, data)
    return 'database update complete'

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
