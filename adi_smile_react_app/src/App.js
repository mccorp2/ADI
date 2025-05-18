import {FacialStream} from './Stream';
import './App.css';

function App() {
  /* Barebones app to display camera data. This video and data are
  published by a flask server defined in adi_backend.
   */
  return (
    <div>
      <div className="App">
        <FacialStream />
      </div>
    </div>
  );
}

export default App;
