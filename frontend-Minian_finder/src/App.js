import './App.css';
import 'mapbox-gl/dist/mapbox-gl.css';

import {BrowserRouter, Route, Routes} from "react-router-dom";
import HomePage from "./components/pages/HomePage";
import AboutPage from "./components/pages/AboutPage";
import {Container} from "react-bootstrap";
import ContactPage from "./components/pages/ContactPage";
import StatusPage from "./components/pages/StatusPage";
import React, {useState} from "react";
import FormComponent from "./components/segments/FormComponent";
import GetStatus from "./components/segments/GetStatus";

function App() {
    const [point, setPoint] = useState('');
    const [number, setNumber] = useState('');
    const [useCurrentLocation, setUseCurrentLocation] = useState(false);
    const [currentLocation, setCurrentLocation] = useState(null);
    const [status, setStatus] = useState('NOT_REGISTERED');
    const [meetingPoint, setMeetingPoint] = useState([]);
  return (
    <BrowserRouter>
        {/*<div style={{ position: 'fixed', width: '100%', zIndex: 1 }}>*/}
        {/*    <MenuBar  />*/}
        {/*</div>*/}
        <Container fluid className="App px-0">
            <Routes>
                <Route path="/" element={<HomePage
                   status={status}
                   setStatus={setStatus}
                   number={number}
                   setNumber={setNumber}
                   useCurrentLocation={useCurrentLocation}
                   setUseCurrentLocation={setUseCurrentLocation}
                   currentLocation={currentLocation}
                   setCurrentLocation={setCurrentLocation}
                   point={point}
                   setPoint={setPoint}/>} />
                <Route path="/status" element={<StatusPage
                   status={status}
                   setStatus={setStatus}
                   number={number}
                   useCurrentLocation={useCurrentLocation}
                   currentLocation={currentLocation}
                   point={point} setPoint={setPoint}
                   meetingPoint={meetingPoint} setMeetingPoint={setMeetingPoint}/>} />
                <Route path="/about" element={<AboutPage/>} />
                <Route path="/contact" element={<ContactPage/>} />
                {/*<Route path="/status" element={<GetStatus*/}
                {/*   status={status}*/}
                {/*   setStatus={setStatus}*/}
                {/*   number={number}*/}
                {/*   useCurrentLocation={useCurrentLocation}*/}
                {/*   currentLocation={currentLocation}*/}
                {/*   point={point} setPoint={setPoint} />} />*/}
            </Routes>
        </Container>
    </BrowserRouter>
  );
}

export default App;