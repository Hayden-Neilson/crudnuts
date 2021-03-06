import React, { Component } from "react";

import Footer from "./footer";

export default class About extends Component {
  render() {
    return (
      <div className="about-container">
        <div className="about-header">
          <h1>About Us</h1>
        </div>
        <div className="center-pic">
          <img
            src="https://images.designtrends.com/wp-content/uploads/2016/01/09121102/Donut-Logo1.jpg"
            alt=""
          />
        </div>

        <div className="header-text">
          <h1>Why do we make donuts and name them this way?</h1>
        </div>

        <div className="center-text">
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam,quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat. Duis aute irure dolor in
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
            culpa qui officia deserunt mollit anim id est laborum.
          </p>
        </div>
        <div className="bottom-image-about">
          <img
            src="https://static9.depositphotos.com/1629907/1124/i/950/depositphotos_11244101-stock-photo-tray-of-sugar-donuts.jpg"
            alt="donut tray"
          />
        </div>
        <Footer />
        <div className="about-footer"></div>
      </div>
    );
  }
}
