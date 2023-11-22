import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import React, {useState, useRef, useEffect} from 'react';
import axios from 'axios';
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
import Documentation from './Documentation'; // Adjust the path as necessary
import TopRow from './TopRow';

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
  const [sumRotation, setSumRotation] = useState(0); // New state for rotation
  const [rotation, setRotation] = useState(0); // New state for rotation
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState(''); // State to store the image URL
  const transformWrapperRef = useRef(null); // Ref to access TransformWrapper
  const [bounds, setBounds] = useState({ boundX: 0, boundY: 0 });
  const [basePairAnnotation, setBasePairAnnotation] = useState('dssr');
  const [loopBulging, setLoopBulging] = useState('1');
  const [additionalFile, setAdditionalFile] = useState(null);
  const [timeString, setTimeString] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showDocumentation, setShowDocumentation] = useState(false);
  const url = 'http://localhost/rnaview/run-rnaview/';

  const toggleDocumentation = () => {
    setShowDocumentation(!showDocumentation);
  };

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
  
  function handleAdditionalFileChange(event) {
    setAdditionalFile(event.target.files[0]);
  }  

  function handleSubmit(event) {
    event.preventDefault();
    setIsLoading(true); // Start loading
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    // Check if additional file is required and selected
    if (basePairAnnotation === 'rnaview' && !additionalFile) {
      alert('Please select an output file from RNAView!');
      return;
  }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('fileName', file.name);
    formData.append('basePairAnnotation', basePairAnnotation);
    formData.append('loopBulging', loopBulging);


    // Append additional file if it's required and provided
    if (basePairAnnotation === 'rnaview' && additionalFile) {
      formData.append('additionalFile', additionalFile);
      formData.append('additionalFileName', additionalFile.name);
    }


    axios.post(url, formData, {
      headers: {
        'content-type': 'multipart/form-data',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      withCredentials: true,
    }).then(response => {
      // Set the image URL in the state
      setSumRotation(0);
      setImageUrl(response.data.image_url);
      setTimeString(response.data.time_string);
    }).catch(error => {
      console.error('Error uploading file:', error);
    }).finally(() => {
      setIsLoading(false); // Stop loading
    });
  }

  // Automatically load example structure
  const loadExampleData = () => {
    setIsLoading(true); // Start loading
    fetch('/testsite/3zp8-assembly1.cif')
      .then(response => response.blob())
      .then(blob => {
        // Create a File object from the blob
        const file = new File([blob], "3zp8-assembly1.cif"); // Adjust filename as needed
        
        // Programmatically set the file to your state and initiate upload
        setFile(file);
          // Check if additional file is required and selected
        if (basePairAnnotation === 'rnaview') {
          alert('Unable to use RNAView output for the example!');
          setIsLoading(false);
          return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('fileName', file.name);
        formData.append('basePairAnnotation', basePairAnnotation);
        formData.append('loopBulging', loopBulging);
        
        axios.post(url, formData, {
          headers: {
            'content-type': 'multipart/form-data',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          withCredentials: true,
        }).then(response => {
          // Set the image URL in the state
          setSumRotation(0);
          setImageUrl(response.data.image_url);
          setTimeString(response.data.time_string);
        }).catch(error => {
          console.error('Error uploading file:', error);
        }).finally(() => {
          setIsLoading(false); // Stop loading
        });
      })
      .catch(error => console.error('Error loading example data:', error))
  };


 // Send timeString and rotation via axios get request to run_regen_labels
 function testDjango(event) {
  setIsLoading(true); // Start loading
  // Define the URL for the GET request
  const url = `http://localhost/rnaview/test-get/`;

  // Set up the query parameters
  const params = {
    timeString: timeString,  // Assuming timeString is stored in state
    rotation: parseInt(rotation) + parseInt(sumRotation)       // Assuming rotation is stored in state
  };

  // Send the GET request with the query parameters
  return axios.get(url, { params })
    .then(response => {
      // Handle the response
      // console.log('Labels regenerated:', response.data);
      alert("SUCCESS!")
      return true;
      // You might want to update some state here based on the response
    })
    .catch(error => {
      console.error('Error regenerating labels:', error);
      throw error;
    })
    .finally(() => {
      setIsLoading(false); // Stop loading
    });
}




  // Send timeString and rotation via axios get request to run_regen_labels
  function handleRegenLabels(event) {
    setIsLoading(true); // Start loading
    // Define the URL for the GET request
    const url = `http://localhost/rnaview/run-regen_labels`;
  
    // do something to sum rotation here!
    // say I rotated 30 degrees already

    // Set up the query parameters
    const params = {
      timeString: timeString,  // Assuming timeString is stored in state
      rotation: parseInt(rotation) + parseInt(sumRotation)       // Assuming rotation is stored in state
    };
    // Send the GET request with the query parameters
    return axios.get(url, { params })
      .then(response => {
        // Handle the response
        // console.log('Labels regenerated:', response.data);
        setSumRotation(parseInt(rotation)+parseInt(sumRotation))
        setRotation(0)
        setImageUrl(response.data.image_url)
        return response.data.image_url;
        // You might want to update some state here based on the response
      })
      .catch(error => {
        console.error('Error regenerating labels:', error);
        throw error;
      })
      .finally(() => {
        setIsLoading(false); // Stop loading
      });
  }
  const downloadImage = (url) => {
    fetch(url)
      .then(response => response.blob())
      .then(blob => {
        const localUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = localUrl;
        link.download = 'processed-image.svg'; // Or dynamically set filename
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(localUrl); // Clean up the URL
      })
      .catch(error => {
        console.error('Error downloading the image:', error);
      });
  };
  
  const handleDownloadAndRegenerate = () => {
    if (rotation !== 0) {
      // If rotation is not 0, regenerate labels and then download
      // handleRegenLabels().then(newImageUrl => {
      //   downloadImage(newImageUrl);
      // });
      downloadRotatedSVG();
    } else {
      // If rotation is 0, directly download the current image
      downloadImage(imageUrl);
    }
  };


  const rotateAndDownloadSVG = (svgText, rotationDegrees) => {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(svgText, "image/svg+xml");
  
    const svgElement = xmlDoc.documentElement;
    const firstGElement = xmlDoc.querySelector('g');
    
    if (firstGElement) {
      // Apply rotation
      const rotationTransform = `rotate(${rotationDegrees})`;
      firstGElement.setAttribute('transform', rotationTransform);
  
      // Calculate new viewBox (rough approximation)
      const originalWidth = parseFloat(svgElement.getAttribute("width"));
      const originalHeight = parseFloat(svgElement.getAttribute("height"));
      const maxDim = Math.max(originalWidth, originalHeight);
      const newViewBox = `0 0 ${maxDim * 1} ${maxDim * 1}`;
      svgElement.setAttribute('viewBox', newViewBox);
    }
  
    // Serialize the modified SVG back to a string
    const serializer = new XMLSerializer();
    const rotatedSVGText = serializer.serializeToString(xmlDoc);
  
  
    // Convert the SVG string to a blob
    const blob = new Blob([rotatedSVGText], {type: "image/svg+xml"});
  
    // Create a download link for the blob
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'rotated-image.svg';  // Setting the download filename
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  };

  const downloadRotatedSVG = () => {
    fetch(imageUrl)
      .then(response => response.text())
      .then(svgText => {
        rotateAndDownloadSVG(svgText, rotation);
      })
      .catch(error => {
        console.error('Error fetching the SVG:', error);
      });
  };

  // const downloadImage = () => {
  //   fetch(imageUrl)
  //     .then(response => response.blob())
  //     .then(blob => {
  //       const rotationDegrees = rotation;
  //       const localUrl = window.URL.createObjectURL(blob);
  //       const image = new Image();
  //       image.src = localUrl;
  //       console.log(rotationDegrees);
  //       image.onload = () => {
  //         console.log("Hi!");
  //         const canvas = document.createElement('canvas');
  //         const ctx = canvas.getContext('2d');
  
  //         // Set canvas size to image size
  //         canvas.width = image.width;
  //         canvas.height = image.height;
  //         console.log(image.width);
  //         console.log(image.height);

  //         // Apply rotation
  //         ctx.translate(canvas.width / 2, canvas.height / 2);
  //         ctx.rotate(rotationDegrees * Math.PI / 180);  // Convert degrees to radians
  //         ctx.drawImage(image, -image.width / 2, -image.height / 2);
  
  //         // Convert canvas to image for download
  //         canvas.toBlob(blob => {
  //           const rotatedUrl = window.URL.createObjectURL(blob);
  //           const link = document.createElement('a');
  //           link.href = rotatedUrl;
  //           link.download = 'rotated-image.png'; // Or dynamically set filename
  //           document.body.appendChild(link);
  //           link.click();
  //           document.body.removeChild(link);
  //           window.URL.revokeObjectURL(localUrl);
  //           window.URL.revokeObjectURL(rotatedUrl);
  //         }, 'image/png', 1); // '1' for maximum quality
  //       };
  //     })
  //     .catch(error => {
  //       console.error('Error rotating and downloading the image:', error);
  //     });
  // };
  


  const transformOptions = {
    initialScale: 1,
    minScale: 0.1,
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
      <TopRow/>
      <form onSubmit={handleSubmit} className="upload-form">
        <a href="/testsite/3zp8-assembly1.cif" download className="download-link">
          Download Example Data
        </a>
        <button type="button" onClick={loadExampleData}>Load Example Data</button>
        <button type="button" onClick={toggleDocumentation}>
          {showDocumentation ? "Hide Documentation" : "Show Documentation"}
        </button>
        <input type="file" onChange={handleChange} required />
  
        <label>Base Pair Annotation:</label>
        <select 
          className="options-dropdown"
          value={basePairAnnotation}
          onChange={(e) => setBasePairAnnotation(e.target.value)}
        >
          <option value="dssr">DSSR</option>
          <option value="rnaview">RNAView</option>
          <option value="saenger">Saenger</option>
          <option value="dssrLw">Leontis-Westhof</option>
        </select>
        {basePairAnnotation === 'rnaview' && (
          <>
            <label class="pad-label" htmlFor="additional-file">Additional File for RNAView:</label>
            <input 
              type="file" 
              onChange={handleAdditionalFileChange} 
              id="additional-file" 
              required 
            />
          </>
        )}
  
        <label>Loop Bulging:</label>
        <select 
          className="options-dropdown"
          value={loopBulging}
          onChange={(e) => setLoopBulging(e.target.value)}
        >
          <option value="1">Conditional</option>
          <option value="0">Always</option>
        </select>
  
        <button type="submit">Upload</button>
      </form>
        {isLoading && (
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      )}
       {showDocumentation && <Documentation />}
      {!showDocumentation && !isLoading && imageUrl && (
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
            <button onClick={handleRegenLabels}>Regenerate Labels</button>
            <button type="button" onClick={handleDownloadAndRegenerate}>Download</button>
          </div>
          <TransformWrapper 
            ref={transformWrapperRef} 
            options={{ ...transformOptions}}
            defaultPositionX={bounds.boundX}
            defaultPositionY={bounds.boundY}
            >
            <TransformComponent
              wrapperStyle={{ height: '80vh', width: '80vw' }}>
              <img 
                src={imageUrl} 
                alt="RNA Landscape Image" 
                className="img-responsive" 
                style={{ transform: `rotate(${rotation}deg)` }}
                onLoad={onImageLoad}
              />
            </TransformComponent>
          </TransformWrapper>
          </div>
          <img 
                src="/testsite/legend.png" 
                alt="Legend"
                className="img-legend"
                />
        </div>
      )}
      <footer className="app-footer">
      <p>RNAScape is maintained by The Rohs Lab @ University of Southern California. It is free to access and use by anyone.</p>
    </footer>
    </div>
  );
}

export default App;
