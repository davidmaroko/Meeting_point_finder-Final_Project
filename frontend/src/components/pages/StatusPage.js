import React, {useState} from 'react';
import Navbar from "../parts/Navbar";
import FooterComponent from "../parts/FooterComponent";
import CheckStatus from "../CheckStatus";
import GetStatus from "../segments/GetStatus";
import MapFrame from "../segments/MapFrame";

const StatusPage = ({status,setStatus,number,useCurrentLocation ,currentLocation,point,setPoint,meetingPoint,setMeetingPoint}) => {
  const printData = () => {
    console.log("++++++++++++++++++++++++++++++++++++");
    console.log("meetingPoint: ", meetingPoint);
    console.log("status: ", status);
    console.log("++++++++++++++++++++++++++++++++++++");
  }
  printData();
  return (
      <>
        <Navbar/>
        <div className="container my-5">
          <div className="row">
            <div className="col-md-5">
              <GetStatus
                 status={status}
                 setStatus={setStatus}
                 number={number}
                 useCurrentLocation={useCurrentLocation}
                 currentLocation={currentLocation}
                 point={point} setPoint={setPoint}
                 meetingPoint={meetingPoint} setMeetingPoint={setMeetingPoint} />
            </div>
            <div className="col-md-7">
              <div className="bg-black"
                   style={{
                      height: '70vh',
                      position: 'relative',
                    }}>
                {(status === 'OFFERED' || status === 'READY_IN_AREA' ||  status === 'READY') && (
                  <MapFrame point={meetingPoint} />
                )}

              </div>
            </div>
          </div>
        </div>
        <FooterComponent/>
      </>
  );
};

export default StatusPage;
