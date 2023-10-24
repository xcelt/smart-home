import React, { Component } from 'react'
import './App.css';

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
  },
  {
    id: 3,
    name: "Lights",
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

const rooms = [
  {
    id: 7,
    name: "Living Area",
    temperature: 14,
    description: "Chilly",
    activated: true,
  },
  {
    id: 8,
    name: "Bedroom 1",
    temperature: 22,
    description: "Warm",
    activated: true,
  },
  {
    id: 9,
    name: "Bedroom 2",
    temperature: 30,
    description: "Hot",
    activated: true,
  },
  {
    id: 10,
    name: "Bathroom",
    temperature: 9,
    description: "Cold",
    activated: true,
  },
]

class App extends Component {
  constructor(props) {
    super(props);
    this.state= {
      viewActivated:false,
      deviceList: devices,
      viewTemperature: false,
      roomList: rooms,
    };
  }

  displayActivatedDevices = status => {
    if (status) {
      return this.setstatus({ viewActivated: true });
    }
    return this.setstatus({ viewActivated: false });
  }

  displayTemperatureSettings = status => {
    if (status) {
      return this.setstatus({ viewTemperature: true });
    }
    return this.setstatus({ viewTemperature: false });
  }

  renderActivatedDevices = () => {
    <div className="my-5 tab-list">
      <span
      onClick={() => this.displayActivatedDevices(true)}
      className={this.state.viewActivated ? "active" : ""}
      >
        Device Settings
      </span>
    </div>
  }

  renderTemperatureSettings = () => {
    <div className="my-10 tab-list">
      <span
      onClick={() => this.displayTemperatureSettings(true)}
      className={this.state.viewTemperature(true)}
      >
        Temperature Settings
      </span>
    </div>
  }

// Render all activated devices
  renderDevices = () => {
    const { viewActivated } = this.state;
    const newDevices = this.state.deviceList.filter(
      device => device.activated == viewActivated
    );
  };

// Render all activated temp settings
  renderTemperature = () => {
    const { viewTemperature } = this.state;
    const newRoom = this.state.roomList.filter(
      room => room.activated == viewTemperature
    );
  };  

  render() {
    return (
      <main className="context">
        <h1 className="text-black text-uppercase text-center my-4"> Smart Home Settings</h1>
        <div className="row">
          <div classname="col-md-6 col-sma-10 mx-auto p-0">
            <div className="card p-3">
              {this.renderDevices()}
              </div>
          </div>
        </div>
      </main>
    )
  }

}

export default App;