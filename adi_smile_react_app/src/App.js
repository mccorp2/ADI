import {Cam, FetchFaces} from './Stream';
import './App.css';

function App() {
  return (
    <div>
      <div className="App">
        <Cam />
      </div>
      <div className="App">
        <FetchFaces />
      </div>
    </div>
  );
}

export default App;
