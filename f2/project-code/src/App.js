import { useEffect } from 'react';
import './App.css';
import SearchIcon from './search.svg'

const API_URL = 'http://localhost:3030/devices'

const device1 ={
  "id": 2,
  "type": "Outdoors",
  "name": "Cameras",
  "image": "N/A",
  "activated": true,
  "enabled": true,
}

const App = () => {

  const listDevices = async (device) => {
    const response = await fetch(`${API_URL}&s=${device}`);
    const data = await response.json();

    console.log(data.Search);
  }

  useEffect(() => {
    listDevices('cameras');
  }, []);

  return (
    <div className="app">
      <h1>Smart Device Interface</h1>
    
      <div className="search">
        <input 
          placeholder="Search activated devices"
          value="Camera"
          onChange= {() => {}}
        />
          <img
            src={SearchIcon}
            alt="SearchIcon"
            onClick={() => {}}
        />
      </div>
      <div className="container">
        <div className="device">
          <div>
            <p>{device1.name}</p>
          </div>
          <div>
            <img src={device1.image !=='N/A' ? device1.image : "https://via.placeholder.com/400"} alt={device1.name} />
          </div>

          <div>
            <span>{device1.type}</span>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
