import React, { Component } from 'react';
import axios from 'axios'



class Temperature extends Component {
    constructor(props) {
      super(props);
      this.state= {
        setTemperature: [],
        modifiable:true,
      };
    }
    
    componentDidMount() {
        this.refreshTemp();
    }

    refreshTemp = () => {
        axios
        .get("http://localhost:8000/api/temperature/")
        .then(res => this.setState({ setTemperature: res.data }))
        .catch(err => console.log(err))
    }

    render () {
        const { modifiable, setTemperature } = this.state;
        const newTemperature = this.state.setTemperature.filter(
            temperature => temperature.modifiable === modifiable
        );
        return 
        <div>
            {newTemperature.map((temperature, index) => (
                <div key={index} className="temperature m-3 text-center">
                    <div className="">
                        Internal Temperature: {temperature.value}&deg;C
                        <button className="btn btn-sm btn-secondary m-3">+</button>
                        <button className="btn btn-sm btn-secondary">--</button>
                    </div>
                </div>
            ))}
        </div>
}
        
}
export default Temperature