import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import React, {useState, useRef, useEffect} from 'react';
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
  const [bounds, setBounds] = useState({ boundX: 0, boundY: 0 });

  const calculateBounds = () => {
    const footerHeight = document.querySelector('.app-footer').clientHeight;
    const windowHeight = window.innerHeight;
    const boundY = windowHeight - footerHeight;
  
    setBounds({ boundX: 0, boundY });
  };
  
  useEffect(() => {
    window.addEventListener('resize', calculateBounds);
    return () => {
      window.removeEventListener('resize', calculateBounds);
    };
  }, []);

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
    calculateBounds();
  };

  useEffect(() => {
    calculateBounds();
  }, [imageUrl]); // Recalculate bounds when the image URL changes
  

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
    <h1>RNAViewer</h1>
    <input type="file" onChange={handleChange} />
    <label>Base Pair Annotation:</label>
    <select className="bulging-dropdown">
        <option value="dssr">DSSR</option>
        <option value="rnaview">RNAView</option>
      </select>
      <label>Loop Bulging:</label>
    <select className="bulging-dropdown">
        <option value="1">Conditional</option>
        <option value="0">Always</option>
      </select>


      <button type="submit">Upload</button>

    </form>
      {imageUrl && (
        <div className="image-and-legend-container">
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
            options={{ ...transformOptions, limitToBounds: true }}
            defaultPositionX={bounds.boundX}
            defaultPositionY={bounds.boundY}
            >
            <TransformComponent
              wrapperStyle={{ height: '80vh', width: '80vw' }}>
              <img 
                src={imageUrl} 
                alt="RNAView Image" 
                className="img-responsive" 
                style={{ transform: `rotate(${rotation}deg)` }}
                onLoad={onImageLoad}
              />
            </TransformComponent>
          </TransformWrapper>
          </div>
          <img 
                src="/legend.png" 
                alt="Legend"
                className="img-legend"
                />
        </div>
      )}
      <footer className="app-footer">
      <p>RNAViewer: A USC x Rutgers collaboration. With gratitude, we recognize the efforts of the original RNAView paper found here.</p>
    </footer>
    </div>
  );
}

export default App;
