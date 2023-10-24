import React, { StrictMode } from 'react';
// {depricated library} import ReactDOM from 'react-dom';
import { createRoot } from 'react-dom/client'; //https://www.npmjs.com/package/react-dom
import App from './App';
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';

// ReactDOM.render(
//  <App />,
//  document.getElementById('root')
// );
// {depricated code}

//https://stackoverflow.com/questions/71668256/deprecation-notice-reactdom-render-is-no-longer-supported-in-react-18
const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

root.render(
    <App />
);