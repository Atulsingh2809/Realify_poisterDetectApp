import React, { useState } from 'react';
import axios from 'axios';
import './style.css';


function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [feedback, setFeedback] = useState([]);

  const handleFileChange = (e) => {
    setVideoFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", videoFile);

    const res = await axios.post("http://localhost:8000/analyze/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    setFeedback(res.data.result);
  };

  return (
    <div className="App">
      <h2>Posture Detection</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload & Analyze</button>
      <div>
        {feedback.map((item, idx) => <p key={idx}>{item}</p>)}
      </div>
    </div>
  );
}

export default App;