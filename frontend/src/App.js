import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import React, {useState, useRef} from 'react';
import axios from 'axios';
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";



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
  const [rotation, setRotation] = useState(0); // New state for rotation
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState(''); // State to store the image URL
  const transformWrapperRef = useRef(null); // Ref to access TransformWrapper

  function handleChange(event) {
    setFile(event.target.files[0]);
  }
  
  function handleSubmit(event) {
    event.preventDefault();
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const url = 'http://localhost:8001/rnaview/run-rnaview/';
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

  const transformOptions = {
    initialScale: 1000,
    minScale: 0.5,
    maxScale: 2,
    // centerOnInit: true
  }

  const onImageLoad = () => {
    centerImage();
  };

  const centerImage = () => {
    if (transformWrapperRef.current) {
      transformWrapperRef.current.centerView();
    }
  };

  const resetTransform = () => {
    if (transformWrapperRef.current) {
      transformWrapperRef.current.resetTransform();
    }
  };

  const zoomIn = () => {
    if (transformWrapperRef.current) {
      transformWrapperRef.current.zoomIn();
    }
  };

  const zoomOut = () => {
    if (transformWrapperRef.current) {
      transformWrapperRef.current.zoomOut();
    }
  };

  const handleRotationChange = (event) => {
    setRotation(event.target.value);
  };


  return (
    <div className="App">
    <form onSubmit={handleSubmit} className="upload-form">
      <h1>RNA CIF File Upload</h1>
      <input type="file" onChange={handleChange} />
      <button type="submit">Upload</button>
    </form>
      {imageUrl && (
        <div className="image-container">
          <div className="controls">
            <button onClick={zoomIn}>Zoom In</button>
            <button onClick={zoomOut}>Zoom Out</button>
            <button onClick={centerImage}>Center</button>
            <button onClick={resetTransform}>Reset</button>
            <label>Rotate Image:</label>
            <input 
              type="range" 
              min="0" 
              max="360" 
              value={rotation} 
              onChange={handleRotationChange}
            />
          </div>
          <TransformWrapper 
            ref={transformWrapperRef} 
            options={transformOptions}>
            <TransformComponent
              wrapperStyle={{ height: '100vh', width: '100vw' }}>
              <img 
                src={imageUrl} 
                alt="Uploaded" 
                className="img-responsive" 
                style={{ transform: `rotate(${rotation}deg)` }}
                onLoad={onImageLoad}
              />
            </TransformComponent>
          </TransformWrapper>
        </div>
      )}
    </div>
  );
}

export default App;