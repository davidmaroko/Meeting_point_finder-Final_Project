import logo from './logo.svg';
import './App.css';
// import UserInput from "./components/UserInput";
// import GetStatus from "./components/GetStatus";
import 'mapbox-gl/dist/mapbox-gl.css';

// function App() {
//   return (
//     <div className="App">
//      <UserInput/>
//      <GetStatus/>
//
//     </div>
//   );
// }
//
// export default App;
import React, {useState} from 'react';
import './App.css';
import UserInput from './components/UserInput';
import GetStatus from './components/GetStatus';
import 'mapbox-gl/dist/mapbox-gl.css';

function App() {
  const [point, setPoint] = useState('');
  const [number, setNumber] = useState(1);
  const [useCurrentLocation, setUseCurrentLocation] = useState(false);
  const [currentLocation, setCurrentLocation] = useState(null);
  const [status, setStatus] = useState('NOT_REGISTERED');

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1 className="App-title">Minyan Finder</h1>
      </header>
      <div className="App-content">
        <UserInput setStatus={setStatus}
                   number={number}
                   setNumber={setNumber}
                   useCurrentLocation={useCurrentLocation}
                   setUseCurrentLocation={setUseCurrentLocation}
                   currentLocation={currentLocation}
                   setCurrentLocation={setCurrentLocation}
                   point={point} setPoint={setPoint} />
        <GetStatus status={status}
                   setStatus={setStatus}
                   number={number}
                   useCurrentLocation={useCurrentLocation}
                   currentLocation={currentLocation}
                   point={point} setPoint={setPoint} />
      </div>
      <footer className="App-footer">
        &copy; {new Date().getFullYear()} Minyan Finder.
      </footer>
    </div>
  );
}

export default App;