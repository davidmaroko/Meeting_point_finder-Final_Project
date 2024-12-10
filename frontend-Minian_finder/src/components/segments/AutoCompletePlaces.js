import React, {useEffect, useState} from 'react';
import mapboxgl from 'mapbox-gl';
import PlacesAutocomplete, {
  geocodeByAddress,
  getLatLng,
} from 'react-places-autocomplete';

mapboxgl.accessToken = 'pk.eyJ1IjoiZGF2aWRtYXIyMzExIiwiYSI6ImNsaWR2MWdzNjAzYXAzaG16MXJvYmk4NDMifQ.CYEcO7xQQ-ROj0-dTxayOg';

const AutoCompletePlaces = ({setUseCurrentLocation, useCurrentLocation, setCurrentLocation, point, setPoint}) => {
  const [address, setAddress] = useState('');

    useEffect( () => {
    if (useCurrentLocation && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const {latitude, longitude} = position.coords;
          setCurrentLocation(`${latitude}, ${longitude}`);
          await reverseGeocode(longitude, latitude);
        },
        (error) => {
          console.error(error);
          setCurrentLocation(null);
        }
      );
    }
  }, [useCurrentLocation]);

  const reverseGeocode = (longitude, latitude) => {
  const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${longitude},${latitude}.json?access_token=${mapboxgl.accessToken}`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      const addressOfCoords = data.features[0].place_name;
      console.log('Reverse Geocoded Address:', addressOfCoords);
      setAddress(addressOfCoords);
    })
    .catch(error => {
      console.error('Reverse Geocoding Error:', error);
    });
};
    // const reverseGeocode = async (longitude, latitude) => {
  //   try {
  //     const response = await axios.get(
  //       `https://api.mapbox.com/geocoding/v5/mapbox.places/${longitude},${latitude}.json?access_token=${mapboxgl.accessToken}`
  //     );
  //
  //     // Extract the address from the response
  //     const addressName = response.data.features[0].place_name;
  //     console.log('Reverse Geocoded Address:', addressName);
  //     setAddress(addressName);
  //   } catch (error) {
  //     console.error('Reverse Geocoding Error:', error);
  //   }
  // };
  const handleChange = (newAddress) => {
    setAddress(newAddress);
  };

  const handleUseCurrentLocationChange = () => {
    setUseCurrentLocation(!useCurrentLocation);
  };

  const handleSelect = async (selectedAddress) => {
    try {
      const results = await geocodeByAddress(selectedAddress);
      const latLng= await getLatLng(results[0]);
      console.log(latLng);
      console.log(`${latLng.lat}, ${latLng.lng}`);
      setAddress(selectedAddress);
      setCurrentLocation(`${latLng.lat}, ${latLng.lng}`);
      setPoint(`${latLng.lat}, ${latLng.lng}`);
    }
    catch(error) {
      console.error('Error', error)
    }
  };

  return (
      <PlacesAutocomplete
      value={address}
      onChange={handleChange}
      onSelect={handleSelect}
    >
      {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
        <div style={{ position: 'relative' }}>
          <div className="input-group input-group-append" style={{position: "relative", display: "flex"}}>
           <input
               {...getInputProps({
                type: "text",
                name: "point",
                className: "form-control",
                style: {flex: "1"},
                placeholder: "Location",
                })}
        />
         <button type={"button"} className="btn btn-primary d-flex align-items-center" onClick={handleUseCurrentLocationChange}>
           <span className="material-icons">my_location</span>
         </button>
       </div>

          <div className="autocomplete-dropdown-container">
            {loading && <div>Loading...</div>}
            {suggestions.map((suggestion, index) => {
              const className = suggestion.active
                ? 'suggestion-item--active'
                : 'suggestion-item';
              const style = suggestion.active
                ? { backgroundColor: '#fafafa', cursor: 'pointer' }
                : { backgroundColor: '#ffffff', cursor: 'pointer' };
              return (
                <div
                    key={index}
                  {...getSuggestionItemProps(suggestion, {
                    className,
                    style,
                  })}
                >
                  <span>{suggestion.description}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </PlacesAutocomplete>
  );
};

export default AutoCompletePlaces;


// import React, {useRef} from "react";
// import {LoadScript, StandaloneSearchBox} from "@react-google-maps/api";
// import {googleMapsApiKey} from "./data";
//
// const AutoCompletePlaces = () => {
//     const inputRef = useRef();
//
//     const handlePlacesChanged = () => {
//         // const [place] = inputRef.current.getPlaces();
//         // const [place] = this.searchBox.getPlaces();
//
//         // if(place) {
//         //     console.log(place.formatted_address);
//         //     console.log(place.geometry.location.lat());
//         //     console.log(place.geometry.location.lng());
//         // }
//     }
//
//      return (
//          <LoadScript
//              googleMapsApiKey={googleMapsApiKey}
//              libraries={["places"]}
//          >
//              <StandaloneSearchBox
//              onLoad={ref => (inputRef.current = ref)}
//              onPlacesChanged={handlePlacesChanged}
//              >
//              <div className="input-group input-group-append" style={{position: "relative", display: "flex"}}>
//                 <input
//                 type="text"
//                 className="form-control"
//                 style={{flex: "1"}}
//                 placeholder="Location"
//                 // value={location}
//                 // onChange={(e) => setLocation(e.target.value)}
//                 ref={inputRef}
//               />
//                <button className="btn btn-primary d-flex align-items-center"><span className="material-icons">my_location</span></button>
//              </div>
//
//              </StandaloneSearchBox>
//          </LoadScript>
//      );
// };
//
// export default AutoCompletePlaces;








// import React, {useRef, useEffect, useState} from "react";
// const AutoCompletePlaces = () => {
//  const [location, setLocation] = useState('');
//  const autoCompleteRef = useRef();
//  const inputRef = useRef();
//  const options = {
//   componentRestrictions: { country: "ng" },
//   fields: ["address_components", "geometry", "icon", "name"],
//   types: ["establishment"]
//  };
//
//  // const handleUseCurrentLocationChange = (e) => {
//  //    setUseCurrentLocation(e.target.checked);
//  //  };
//
//  // const handlePointChange = (e) => {
//  //    setPoint(e.target.value);
//  //  };
//
//  useEffect(() => {
//   autoCompleteRef.current = new window.google.maps.places.Autocomplete(
//    inputRef.current,
//    options
//   );
//  }, []);
//  return (
//
//  <div className="input-group input-group-append" style={{position: "relative", display: "flex"}}>
//     <input
//     type="text"
//     className="form-control"
//     style={{flex: "1"}}
//     placeholder="Location"
//     // value={location}
//     // onChange={(e) => setLocation(e.target.value)}
//     ref={inputRef}
//   />
//    <button className="btn btn-primary d-flex align-items-center"><span className="material-icons">my_location</span></button>
//  </div>
//
//  );
// };
// export default AutoCompletePlaces;