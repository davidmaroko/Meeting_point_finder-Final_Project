import React, { useState } from 'react';
import SearchBox from './SearchBox';

const App = () => {
  const [searchValue, setSearchValue] = useState('');

  const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchValue(value);
    // Perform autocomplete suggestions here
  };

  return (
    <div className="container mt-4">
      <h1>Search Box Example</h1>
      <SearchBox value={searchValue} onChange={handleSearchChange} />
      {/* Render search results or autocomplete suggestions */}
    </div>
  );
};

export default App;
