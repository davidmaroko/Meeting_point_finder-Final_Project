import React, {useState} from 'react';
import Navbar from "../parts/Navbar";
import FormComponent from "../segments/FormComponent";
import UserInput from "../UserInput";
import GetStatus from "../segments/GetStatus";
import FooterComponent from "../parts/FooterComponent";

const HomePage = ({status, setStatus,number,setNumber,currentLocation,setCurrentLocation,useCurrentLocation,setUseCurrentLocation,point,setPoint}) => {
  return (
    <>
      <header className="App-header">
        <Navbar/>
        <FormComponent
                   setStatus={setStatus}
                   number={number}
                   setNumber={setNumber}
                   currentLocation={currentLocation}
                   setCurrentLocation={setCurrentLocation}
                   useCurrentLocation={useCurrentLocation}
                   setUseCurrentLocation={setUseCurrentLocation}
                   point={point} setPoint={setPoint} />
      </header>
      <div className="App-content">
        <UserInput
           setStatus={setStatus}
           number={number}
           setNumber={setNumber}
           currentLocation={currentLocation}
           setCurrentLocation={setCurrentLocation}
           useCurrentLocation={useCurrentLocation}
           setUseCurrentLocation={setUseCurrentLocation}
           point={point} setPoint={setPoint} />
        {/*<GetStatus status={status}*/}
        {/*           setStatus={setStatus}*/}
        {/*           number={number}*/}
        {/*           useCurrentLocation={useCurrentLocation}*/}
        {/*           currentLocation={currentLocation}*/}
        {/*           point={point} setPoint={setPoint} />*/}
      </div>
      <FooterComponent/>
    </>
  );
};

export default HomePage;
