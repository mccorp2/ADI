import React, { useState, useEffect } from "react";

function FetchImageData(isOn) {
    /* React function to grab image metadata from a local host.
    Args:
    - isOn: Boolean react hook defining if the video capture is active.

    Return:
    - metaData: expects json as text containing all smiles and their coordinates.
    */
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
    fetchMetaData(); // Fetch image metadata from localhost

    const intervalId = setInterval(() => {
      fetchMetaData(); // Referesh cycle in ms.
    }, 100);

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

    return (
      <p>
        {isOn ? metaData : '{}'}
      </p>
    );
}

function FacialStream() {
    /* React function to stream video from a python backend. Grabs jpegs as frames from
    a local host.

    Return:
    - Streamed image
    - Enable button
    - Smiles metadata
     */
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

  
  
  export {FacialStream, FetchImageData};