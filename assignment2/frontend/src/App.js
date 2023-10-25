import React, { Component } from 'react'
import './App.css';
import CustomModal from "./components/Modal"
import Temperature from "./components/Temperature"
import BootstrapSwitchButton from 'bootstrap-switch-button-react' // needs to be added to req'd deps

// Will be removed once hooked up to backend
const devices = [ 
  {
    id: 1,
    name: "Camera",
    activated: true,
  },
  {
    id: 2,
    name: "Thermostat",
    activated: true,
    temperatureSet: true,
    temperature: 22,
      
  },
  {
    id: 3,
    name: "Lighting",
    activated: true,
  },
  {
    id: 4,
    name: "Smart Lock",
    activated: true,
  },
  {
    id: 5,
    name: "Alarm",
    activated: true,
  },
  {
    id: 6,
    name: "Motion Sensor",
    activated: true,
  },
]

class App extends Component {
  constructor(props) {
    super(props);
    this.state= {
      modal: false,
      viewActivated: true,
      deviceList: devices,
      activeItem: {
        Name: "",
        value: "",
        completed: false,
      }
    };
  }
// Checks if device is activated or not
  displayActivated = status => {
    if (status) {
      return this.setState({ viewActivated: true })
    }
    return this.setState({ viewActivated: false })
  }

// Renders activated and inactive devices under proper heading
  renderDeviceList = () => {
    return (
      <div className="device-list m-3">
        <span
        onClick={() => this.displayActivated(true)}
        className={this.state.viewActivated ? "active" : "" }
        >
          Activated Devices
        </span>
      </div>
    )
  }

// Rendering devices in the list { activated || inactive }
  renderDevices = () => {
    const { viewActivated } = this.state;
    const newDevices = this.state.deviceList.filter(
      device => device.activated === viewActivated
    );   
    
    return newDevices.map(device => (
      <li key={device.id} className="list-group-device d-flex justify-content-between align-devices-center">

        <span className={`list-name m-3 ${this.state.viewActivated ? "activated-list" : ""}`} name={device.name}>
          {device.name}
        </span>
        <span className="switch-button">
        <BootstrapSwitchButton checked={`${this.state.viewActivated}`} onstyle="success" offstyle="danger" height={40} width={70}/>
        </span>
      </li>
    ))
  
  
  };

 

  render () {
    return (
      <main className="content p-3 mb-2">
        <h1 className="text-light text-uppercase text-center my-4"> Smart Device Manager </h1>
        <div className="row">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
            <div className="static-position card p=3">
              <div>
                <Temperature className="temp-counter" />
              </div>
              <h1 className="text-secondary text-uppercase text-center">
              {this.renderDeviceList()} </h1>
              <span className="text-center">
                  <button className="btn btn-success m-3">Enable All Devices</button>
                  <button className="btn btn-danger m-3">Disable All Devices</button>
              </span>
              <ul className=" list-group list-group-flush">
              {this.renderDevices()}
              </ul>
            </div>
          </div>
        </div>
        <footer className="m-4 mb-2 text-light text-center">Copyright 2023 &copy; All Rights Reserved</footer>

      </main>
    );
  };


}

export default App;