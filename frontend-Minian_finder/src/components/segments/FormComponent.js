import React, {useEffect, useState} from 'react';
import AutoCompletePlaces from "./AutoCompletePlaces";
import CheckStatus from "../CheckStatus";
import { useNavigate } from 'react-router-dom';

const FormComponent = ({setStatus,number,setNumber,currentLocation,setCurrentLocation,useCurrentLocation,setUseCurrentLocation,point,setPoint}) => {
  const [email, setEmail] = useState('');


  const handlePointChange = (e) => {
    setPoint(e.target.value);
  };

  const handleNumberChange = (e) => {
    setNumber(Number(e.target.value));
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleUseCurrentLocationChange = (e) => {
    setUseCurrentLocation(e.target.checked);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(`number: ${number}`);
    console.log(`email: ${email}`);
    console.log(`point: ${point}`);
    console.log(`currentLocation: ${currentLocation}`);
    console.log(`useCurrentLocation: ${useCurrentLocation}`);
   
    const requestBody = {
      point: useCurrentLocation ? currentLocation : point,
      number: number.toString(),
      email: email,
    };
    console.log(`point: ${requestBody.point}`);

    setUseCurrentLocation(false);
    fetch('http://localhost:5000/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response from the server
        console.log(data);
        alert(data.status);
        setStatus('WAIT');
      })
      .catch((error) => {
        // Handle any errors
        console.error(error);
      });

  };

  return (
      <div className={"form-container position-absolute top-50 start-50 translate-middle p-3 rounded-2"}>
        <h1 className={"text-white pb-4"}>Find a minyan near you now</h1>
        <form onSubmit={handleSubmit}>
          <div className="row mb-3">
            <div className="col-md-12">
              { <AutoCompletePlaces
                  setUseCurrentLocation={setUseCurrentLocation}
                  useCurrentLocation={useCurrentLocation}
                  setCurrentLocation={setCurrentLocation}
                  point={point}
                  setPoint={setPoint}/> }
              {/*  <input*/}
              {/*  type="text"*/}
              {/*  name="point"*/}
              {/*  min="1"*/}
              {/*  required*/}
              {/*  className="form-control"*/}
              {/*  placeholder="point"*/}
              {/*  value={point}*/}
              {/*  onChange={handlePointChange}/>*/}
            </div>
          </div>
          <div className="row mb-3">
            <div className="col-md-6">
              <input
                type="email"
                pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
                title="Please enter a valid email"
                required
                className="form-control"
                placeholder="Email"
                value={email}
                onChange={handleEmailChange}
              />
            </div>
            <div className="col-md-6">
              <input
                type="number"
                name="number"
                min="1"
                required
                className="form-control"
                placeholder="Number of People"
                value={number}
                onChange={handleNumberChange}
              />
            </div>
          </div>
          <div className="row">
            <div className=" col-12">
              <button type="submit" className="btn btn-primary form-control">Add your details</button>
            </div>
          </div>
        </form>
    </div>
  );
};

export default FormComponent;
