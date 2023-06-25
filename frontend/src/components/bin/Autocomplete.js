import React, { useState } from 'react';
import { GoogleMap, Autocomplete } from '@react-google-maps/api';
import googleMapsApiKey from '../util/data'
const AutocompleteComponent = ({ apiKey }) => {
  const [autocomplete, setAutocomplete] = useState(null);
  const [autocompleteValue, setAutocompleteValue] = useState('');

  const onLoad = (autoC) => {
    setAutocomplete(autoC);
  };

  const onPlaceChanged = () => {
    if (autocomplete !== null) {
      const place = autocomplete.getPlace();
      const address = place.formatted_address || '';

      setAutocompleteValue(address);
    }
  };

  return (
    <GoogleMap
      onLoad={onLoad}
      mapContainerStyle={{ width: '100%', height: '400px' }}
      zoom={8}
      center={{ lat: 37.7749, lng: -122.4194 }} // Set your preferred initial center position
      apiKey={googleMapsApiKey}
    >
      <Autocomplete onLoad={onLoad} onPlaceChanged={onPlaceChanged}>
        <input
          type="text"
          placeholder="Enter your location"
          value={autocompleteValue}
          onChange={(e) => setAutocompleteValue(e.target.value)}
          style={{
            boxSizing: 'border-box',
            border: '1px solid transparent',
            width: '240px',
            height: '32px',
            padding: '0 12px',
            borderRadius: '3px',
            boxShadow: '0 2px 6px rgba(0, 0, 0, 0.3)',
            fontSize: '14px',
            outline: 'none',
            textOverflow: 'ellipses',
            position: 'absolute',
            left: '50%',
            marginLeft: '-120px',
          }}
        />
      </Autocomplete>
    </GoogleMap>
  );
};

export default AutocompleteComponent;
