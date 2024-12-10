import React, { useState, useEffect } from 'react';

const UserInput = ({setStatus,number,setNumber,currentLocation,setCurrentLocation,useCurrentLocation,setUseCurrentLocation,point,setPoint}) => {
  const [email, setEmail] = useState('');

  useEffect(() => {
    if (useCurrentLocation && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setCurrentLocation(`${latitude}, ${longitude}`);
        },
        (error) => {
          console.error(error);
          setCurrentLocation(null);
        }
      );
    }
  }, [useCurrentLocation]);

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
    const requestBody = {
      point: useCurrentLocation ? currentLocation : point,
      number: number.toString(),
      email: email,
    };
    console.log("requestBody: ",requestBody);
    console.log("point that send: ",point);
    console.log("point that send: ",useCurrentLocation ? currentLocation : point);
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
    <div className="UserInput">
      <h2>Enter Point</h2>
      <form onSubmit={handleSubmit}>
        <div className="Input-container">
          <label>השתמש במיקום הנוכחי שלך:</label>
          <input
            type="checkbox"
            checked={useCurrentLocation}
            onChange={handleUseCurrentLocationChange}
          />
        </div>
        {!useCurrentLocation && (
          <div className="Input-container">
            <label>נקודה:</label>
            <input
              type="text"
              name="point"
              placeholder="Enter point coordinates"
              value={point}
              onChange={handlePointChange}
            />
          </div>
        )}
        <div className="Input-container">
          <label>מספר המתפללים:</label>
          <input
            type="number"
            name="number"
            placeholder="Number"
            value={number}
            onChange={handleNumberChange}
          />
        </div>
        <div className="Input-container">
          <label>אימייל:</label>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={handleEmailChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default UserInput;
