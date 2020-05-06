import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import { UserContextProvider } from './shared/userContext';
import './index.css';
import './assets/styles/font-awesome.min.css';
import * as serviceWorker from './serviceWorker';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import Router from "./routes/router";
import 'react-datepicker/dist/react-datepicker.min.css';
import 'react-toastify/dist/ReactToastify.min.css';

ReactDOM.render(
  <BrowserRouter>
    {/* <React.StrictMode> */}
    <UserContextProvider>
      <Router />
      <ToastContainer/>
    </UserContextProvider>
    
    {/* </React.StrictMode> */}
  </BrowserRouter>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
