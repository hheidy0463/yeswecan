import React, { useState } from 'react';
import axios from 'axios';
import Dropzone from 'react-dropzone';

const App = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [transcript, setTranscript] = useState('');
  const [translation, setTranslation] = useState('');
  const [className, setClassName] = useState('');
  const [lectureTitle, setLectureTitle] = useState('');
  const [selectedLecture, setSelectedLecture] = useState('');

  const handleFileDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    setVideoFile(file);
  };

  const handleUpload = async () => {
    try { // dont' use withAuthentication, also use 127.0.0.1 instead of localhost
      const formData = new FormData();

      formData.append('videoFile', videoFile);
      formData.append('selectedLanguage', selectedLanguage);
      formData.append('className', className);
      formData.append('lectureTitle', lectureTitle);

      const uploadResponse = await axios.post('http://127.0.0.1:5000/upload', { videoFile : videoFile });
      const filepath = uploadResponse.data.filePath

      const transcribeResponse = await axios.post('http://127.0.0.1:5000/transcribe', { filepath : filepath});
      const transcription = transcribeResponse.data.transcription

      const dbResponse = await axios.post('http://127.0.0.1:5000/create_lecture', {className: className, lectureTitle: lectureTitle, transcript: transcription})
      
      setTranscript(transcription);

    } catch (error) {
      console.error('Error uploading video:', error);
    }
  };

  const handleTranslate = async () => {
    try { // dont' use withAuthentication, also use 127.0.0.1 instead of localhost
      const formData = new FormData();

      formData.append('videoFile', videoFile);
      formData.append('selectedLanguage', selectedLanguage);
      formData.append('className', className);
      formData.append('lectureTitle', lectureTitle);
      formData.append('transcript', transcript);

      const tranlateRepsonse = await axios.post('http://127.0.0.1:5000/translate', { target: selectedLanguage, text: transcript })
      const translation = tranlateRepsonse.data.translation;

      const dbResponse = await axios.post('http://127.0.0.1:5000/update_lecture', { className: className, lectureTitle: lectureTitle, selectedLanguage: selectedLanguage, translation: translation})
      
      setTranscript(translation);

    } catch (error) {
      console.error('Error uploading video:', error);
    }
  }

  const handleClassNameChange = (e) => {
    setClassName(e.target.value);
  };

  const handleLectureTitleChange = (e) => {
    setLectureTitle(e.target.value);
  };

  const handleLectureSelectChange = (e) => {
    setSelectedLecture(e.target.value);
  };

  const handleSelectedLanugageChange = (e) => {
    setSelectedLanguage(e.target.value);
  }

  // Dummy function for demonstration. Replace with actual data retrieval logic.
  const getStoredLectures = () => {
    return [

    ];
  };

  const inputStyles = {
    margin: '10px 0',
    padding: '10px',
    border: '1px solid #cccccc',
    borderRadius: '1px',
    width: '95%'
  };

  return (
    <div>
      <h1>Video Translation App</h1>

      <div>
        <h2>Class and Lecture Details</h2>
        <input
          type="text"
          placeholder="Class Name"
          value={className}
          onChange={handleClassNameChange}
          style={inputStyles}
        />
        <input
          type="text"
          placeholder="Lecture Title"
          value={lectureTitle}
          onChange={handleLectureTitleChange}
          style={inputStyles}
        />
        <h3>Select Previous Lecture</h3>
        <select
          value={selectedLecture}
          onChange={handleLectureSelectChange}
          style={inputStyles}
        >
          <option value="">Select a Stored Lecture</option>
          {getStoredLectures().map((lecture) => (
            <option key={lecture.id} value={lecture.id}>
              {lecture.title}
            </option>
          ))}
        </select>
      </div>

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
            onChange={handleSelectedLanugageChange}
            style={inputStyles}
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
        <div>
            <button onClick={handleTranslate}>Translate</button>
          </div>
      </div>
      <div>
        <h2>Translated Transcript</h2>
        <p>{translation}</p>
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
