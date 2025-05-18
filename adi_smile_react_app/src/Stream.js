import React, { useState, useEffect } from "react";

function FetchFaces() {
    const [paragraph, setParagraph] = useState('No smiles found.');

    const fetchParagraph = async () => {
      try {
        const response = await fetch('http://localhost:8081/smiles');
        const data = await response.text();
        setParagraph(data);
      } catch (error) {
        setParagraph(error.message);
      }
    }

  useEffect(() => {
    fetchParagraph(); // Fetch text on component mount

    const intervalId = setInterval(() => {
      fetchParagraph(); // Fetch text every 5 seconds
    }, 100);

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

    return (
        <>
            <p>{paragraph}</p>
        </>
    );
}

function Cam() {
    let initialState = false;
    let cameraSource = "http://localhost:8081/video_feed";
    const [isOn, setIsOn] = useState(initialState);
    const [streamSource, setStreamSource] = useState(initialState ? cameraSource : null)

    const handleToggle = () => {
      setIsOn(!isOn);
      setStreamSource(isOn ? null : cameraSource)
    };
  
    return (
    <div>
        <img
            className="Video-feed"
            src={streamSource}
            alt="Video"
        />
        <button 
            onClick={handleToggle}
            aria-pressed={isOn}
            style={{
            backgroundColor: isOn ? 'green' : 'gray',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            cursor: 'pointer',
            }}
        >
        {isOn ? 'Face Detection: On' : 'Face Detection: Off'}
        </button>
    </div>
    );
  }

  
  
  export {Cam, FetchFaces};