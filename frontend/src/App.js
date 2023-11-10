import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import React, {useState} from 'react';
import axios from 'axios';

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function App() {
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState(''); // State to store the image URL

  function handleChange(event) {
    setFile(event.target.files[0]);
  }
  
  function handleSubmit(event) {
    event.preventDefault();
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const url = 'http://localhost:8000/rnaview/run-rnaview/';
    const formData = new FormData();
    formData.append('file', file);
    formData.append('fileName', file.name);

    axios.post(url, formData, {
      headers: {
        'content-type': 'multipart/form-data',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      withCredentials: true,
    }).then(response => {
      // Set the image URL in the state
      setImageUrl(response.data.image_url);
    }).catch(error => {
      console.error('Error uploading file:', error);
    });
  }

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <h1>RNA CIF File Upload</h1>
        <input type="file" onChange={handleChange}/>
        <button type="submit">Upload</button>
      </form>
      {imageUrl && (
        <div classname="image-container">
          <h2>Uploaded Image:</h2>
          <img src={imageUrl} alt="Uploaded" className="img-responsive" />
        </div>
      )}
    </div>
  );
}

export default App;