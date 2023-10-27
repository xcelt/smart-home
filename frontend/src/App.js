import React, { Component } from 'react'
import './App.css';
import axios from 'axios'
import Temperature from "./components/Temperature"
import BootstrapSwitchButton from 'bootstrap-switch-button-react' // needs to be added to req'd deps

// Main code Reference: 
// Chat GPT corrections (ChatGPT, 2023):
// 41:45: ...devices" ==> ...devices/"
// 60:7: return this.setState({ deviceEnabled: true}) ==> return this.state.deviceEnabled;
// 72:28: { viewActivated } ==> 
// 81:42: onClick={this.handleSubmit() --> onClick={ () => this.handleSubmit(device)}
// 93:83: checked=[this.displayEnabled] ==> checked={this.displayEnabled(device.enabled)}
// 103:30: className ==> class
// See full source list in README/References

class App extends Component {
  constructor(props) {
    super(props);
    this.state= {
      deviceEnabled: false,
      viewActivated: true,
      deviceList: []
    };
  }

  componentDidMount() {
    this.refreshList();
  }

  refreshList = () => {
    axios
    .get("http://localhost:8000/api/devices/")
    .then(res => this.setState({ deviceList: res.data }))
    .catch(err => console.log(err))
  };
  
  handleSubmit = device => {
    if (device.id) {
      axios
      .put(`http://localhost:8000/api/tasks/${device.id}/`, device)
      .then(res => this.refreshList())
    }
    axios
    .post("http://localhost:8000/api/devices/", device)
    .then(res => this.refreshList()
    )
  }

// Checks if device is activated or not
  displayActivated = status => {
    if (status) {
      return this.setState({ viewActivated: true })
    }
    return this.setState({ viewActivated: false })
  }

  displayEnabled = status => {
    if (status) {
      return !this.state.deviceEnabled;
    }
    return this.state.deviceEnabled;
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
    const { viewActivated, deviceList } = this.state;
    const newDevices = this.state.deviceList.filter(
      device => device.activated === viewActivated
    );   
    
    return newDevices.map(device => (
      <li key={device.id} className="list-group-device d-flex justify-content-between align-devices-center">

        <span className={`list-name m-3 ${this.state.viewActivated ? "activated-list" : ""}`} name={device.name}>
          {device.name}
        </span>
        <span className="switch-button">
        <BootstrapSwitchButton onClick={ () => this.handleSubmit(device) } checked={this.displayEnabled(device.enabled)} onstyle="success" offstyle="danger" height={40} width={70}/>
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
                <Temperature class="temp-counter" /> 
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