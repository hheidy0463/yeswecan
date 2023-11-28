import React, { useState } from 'react';
import axios from 'axios';
import Dropzone from 'react-dropzone';

const App = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [transcript, setTranscript] = useState('');

  const handleFileDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    setVideoFile(file);
  };

  const handleUpload = async () => {
    // Implement video upload logic using a server and API
    // For simplicity, we'll assume a successful upload and get back a transcript
    try {
      const videoFile = document.getElementById('fileInput').files[0];

      const transcribeResponse = await axios.post('API_ENDPOINT', { videoFile });
      const transcription = transcribeResponse.data.transcription;

      const tranlateRepsonse = await axios.post('API_ENDPOINT', { target: selectedLanguage, text: transcription})
      const translation = tranlateRepsonse.data.translation;

      setTranscript(translation);
      
    } catch (error) {
      console.error('Error uploading video:', error);
    }
  };

  return (
    <div>
      <h1>Video Translation App</h1>
      <div>
        <h2>Upload Video</h2>
        <Dropzone onDrop={handleFileDrop}>
          {({ getRootProps, getInputProps }) => (
            <div {...getRootProps()} style={dropzoneStyles}>
              <input {...getInputProps()} />
              <p>Drag and drop a video file here, or click to select one</p>
            </div>
          )}
        </Dropzone>
        {videoFile && (
          <div>
            <p>Selected Video: {videoFile.name}</p>
            <button onClick={handleUpload}>Upload</button>
          </div>
        )}
      </div>
      <div>
        <h2>Choose Translation</h2>
        <label>
          Select Language:
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
          >
            <option value="en">English</option>
            <option value="fr">French</option>
            <option value="es">Spanish</option>
            <option value="zh">Mandarin</option>
            <option value="ar">Arabic</option>
            <option value="de">German</option>
            <option value="ru">Russian</option>
            <option value="ja">Japanese</option>
            <option value="pt">Portuguese</option>
            <option value="hi">Hindi</option>
          </select>
        </label>
      </div>
      <div>
        <h2>Translated Transcript</h2>
        <p>{transcript}</p>
      </div>
    </div>
  );
};

const dropzoneStyles = {
  border: '2px dashed #cccccc',
  borderRadius: '4px',
  padding: '20px',
  textAlign: 'center',
  cursor: 'pointer',
};

export default App;
