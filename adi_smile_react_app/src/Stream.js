import React, { useState, useEffect } from "react";

function FetchImageData(isOn) {
    const [metaData, setMetaData] = useState('{}');

    const fetchMetaData = async () => {
      try {
        const response = await fetch('http://localhost:8081/smiles');
        const data = await response.text();
        setMetaData(data);
      } catch (error) {
        setMetaData(error.message);
      }
    }

  useEffect(() => {
    fetchMetaData(); // Fetch text on component mount

    const intervalId = setInterval(() => {
      fetchMetaData(); // Fetch text every 5 seconds
    }, 100);

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

    return (
      <p>
        {isOn ? metaData : '{}'}
      </p>
    );
}

function Cam() {
    let initialState = false;
    let cameraSource = "http://localhost:8081/video_feed";
    const [isOn, setIsOn] = useState(initialState);
    const [streamSource, setStreamSource] = useState(initialState ? cameraSource : null);

    const handleToggle = () => {
      setIsOn(!isOn);
      setStreamSource(isOn ? null : cameraSource)
    };

    const metaData = FetchImageData(isOn);
  
    return (
    <div>
        <img
            className="Video-feed"
            src={streamSource}
            alt="Video"
        />
        <div>
          <button 
              onClick={handleToggle}
              aria-pressed={isOn}
              style={{
              backgroundColor: isOn ? 'green' : 'gray',
              }}
          >
          {isOn ? 'Face Detection: On' : 'Face Detection: Off'}
          </button>
          {metaData}
          
        </div>
    </div>
    );
  }

  
  
  export {Cam, FetchImageData};