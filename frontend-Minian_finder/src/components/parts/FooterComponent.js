import React from 'react';

const FooterComponent = () => {
  return (
      <footer className="App-footer bg-light py-2">
        &copy; {new Date().getFullYear()} Minyan Finder.
      </footer>
  );
};

export default FooterComponent;
