# api.py
from flask import Flask, request, jsonify
from transcribe import transcribe
from translate import translate_text

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_endpoint():
    data = request.get_json()
    video_file = data.get('video_file')
    result = transcribe(video_file)
    return jsonify({'transcription': result})

@app.route('/translate', methods=['POST'])
def translate_endpoint():
    data = request.get_json()
    text = data.get('text')
    target = data.get('target', 'en')
    result = translate_text(target, text)
    return jsonify({'translation': result})

if __name__ == '__main__':
    app.run(port=5000)
