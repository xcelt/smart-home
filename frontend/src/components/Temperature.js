import React, { useState } from 'react';

function Temperature() {
    const [temperature, setTemp] = useState(22)

    return (
        <div className="temperature m-3 text-center">
            <div className="">
            Internal Temperature: {temperature}&deg;C 
            <button className="btn btn-sm btn-secondary m-3" onClick={() => setTemp(temperature + 1)}>+</button>
            <button className="btn btn-sm btn-secondary"onClick={() => setTemp(temperature - 1)}>--</button>
            </div>
        
        </div>
    )
}

export default Temperature