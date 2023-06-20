import React, { useState } from 'react';
import { Button, Form, Alert } from 'react-bootstrap';
import MapFrame from './MapFrame';

const GetStatus = ({status,setStatus,number,useCurrentLocation ,currentLocation,point,setPoint}) => {
  const [email, setEmail] = useState('');
  const [meetingPoint, setMeetingPoint] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();

    const url = `http://localhost:5000/?email=${encodeURIComponent(email)}`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        // Handle the server's response
        if (data.status === null) {
          setStatus('WAIT');
        } else if (data.status === 'OFFERED') {
          setStatus('OFFERED');
          setMeetingPoint([data.meeting_point[0], data.meeting_point[1]]);
        } else if (data.status === 'CONFIRM') {
          setStatus('CONFIRM');
        } else if (data.status === 'READY' && status !== 'WAIT') {
          console.log(status);
          setStatus('READY');
          setMeetingPoint([data.meeting_point[0], data.meeting_point[1]]);
        } else if (data.status === 'READY' && status === 'WAIT') {
          console.log(status);
          setStatus('READY_IN_AREA');
          setMeetingPoint([data.meeting_point[0], data.meeting_point[1]]);
        } else if (data.status === 'ARE_REJECTED') {
          setStatus('ARE_REJECTED');
          setMeetingPoint({});
        }else if (data.status === 'NOT_REGISTERED') {
          setStatus('NOT_REGISTERED');
          setMeetingPoint({});
          setPoint('');
        }
      console.log(data);
      })
      .catch((error) => {
        // Handle any errors
        console.error(error);
      });
  };

  const handleChange = (e) => {
    setEmail(e.target.value);
  };

  const handleConfirm = () => {
    const requestBody = {
      email: email,
      meeting_point: meetingPoint,
    };

    fetch('http://localhost:5000/confirm', {
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
        setStatus('WAIT_TO_OTHER_PEOPLE_CONFIRMATION');
      })
      .catch((error) => {
        // Handle any errors
        console.error(error);
      });
  };

 const handleReject = () => {
    const requestBody = {
      email: email,
      meeting_point: meetingPoint,
    };
    console.log("point: ",point)
    console.log(meetingPoint)
    fetch('http://localhost:5000/reject', {
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
        setStatus('NOT_REGISTERED');
        setMeetingPoint({})
        setPoint('')
        alert('reject successfully!')
      })
      .catch((error) => {
        // Handle any errors
        console.error(error);
      });
  };

 const handleRejectArea = () => {
      const requestBody = {
      point: useCurrentLocation ? currentLocation : point,
      email: email,
      number: number.toString()
    };
    console.log("point: ",requestBody.point," number: ",requestBody.number," email: ",requestBody.email)
    fetch('http://localhost:5000/rejectArea', {
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
      })
      .catch((error) => {
        // Handle any errors
        console.error(error);
      });
  };

  return (
    <div className="GetStatus">
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formEmail">
          <Form.Control
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={handleChange}
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Check
        </Button>
      </Form>

      {status === 'WAIT' && (
        <Alert variant="info">
          Not found minyan yet
        </Alert>
      )}

      {status === 'CONFIRM' && (
        <Alert variant="info">
          Your confirmation was received, wait for the other people
        </Alert>
      )}

      {status === 'WAIT_TO_OTHER_PEOPLE_CONFIRMATION' && (
        <Alert variant="info">
          Waiting for other people's confirmation
        </Alert>
      )}
      {status === 'ARE_REJECTED' && (
        <Alert variant="info">
          one of the minian preys are decided to reject. the system search again for minian
        </Alert>
      )}
      {status === 'NOT_REGISTERED' && (
        <Alert variant="info">
          please register
        </Alert>
      )}

      {status === 'OFFERED' && (
        <div>
          <Alert variant="success">
            Found minyan in your area, the meeting point is {meetingPoint}
          <MapFrame point={meetingPoint} />
          </Alert>
          <Button variant="primary" onClick={handleConfirm}>
            Confirm
          </Button>
          <Button variant="primary" onClick={handleReject}>
            Reject
          </Button>
        </div>
      )}
      {status === 'READY_IN_AREA' && (
        <div>
          <Alert variant="success">
            minyan exist in your area, the meeting point is {meetingPoint}
          <MapFrame point={meetingPoint} />
          </Alert>
          if the meeting point not suitable for you:
          <Button variant="primary" onClick={handleRejectArea}>
            Reject And search again
          </Button>
        </div>
      )}

      {status === 'READY' && (
        <div>
          <Alert variant="success">
            The minyan is in progress, the meeting point is {meetingPoint}
          </Alert>
          <MapFrame point={meetingPoint} />
          <Alert variant="success">
            Please go there!
          </Alert>
        </div>
      )}
    </div>
  );
};

export default GetStatus;

