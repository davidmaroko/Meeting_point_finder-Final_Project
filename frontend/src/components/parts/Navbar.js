import React from 'react';
import logo from '../../img/default-monochrome.svg';
import {Link} from "react-router-dom";

const Navbar = () => {
  return (
      <nav className="navbar navbar-expand-lg navbar-light bg-light w-100">
        <div className="container"> {/* Use container class */}
          <Link className="navbar-brand" to="/">
          <img
              src={logo}
              height='50'
              className={"me-3"}
              alt='Minyan Finder'
              loading='lazy'
            />
          </Link>
          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse justify-content-end" id="navbarNav">
            <ul className="navbar-nav ml-auto">
              <li className="nav-item">
                <Link className="nav-link" to="/">Home</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/status">Status</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/about">About</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/contact">Contact</Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
  );
};

export default Navbar;
