
import React, { useContext } from 'react';
import { Route, Switch, Redirect } from 'react-router-dom';

// import { UserContext } from '../shared/userContext/userContext';
import Login from '../components/Login/Login';
import SignUp from '../components/SignUp/SignUp';
import App from '../App';
// import LoggedInRoutes from './LoggedInRoutes';

export default function Routes() {
  // const userContextValue = useContext(UserContext);
  const isLoggedIn = false;

  return (
    <Switch>
      {!isLoggedIn && <Route path={'/login'} component={Login} />}
      {!isLoggedIn && <Route path={'/sign-up'} component={SignUp} />}
      {!isLoggedIn && <Redirect to="/login" />}

      {isLoggedIn && <Route component={App} />}
    </Switch>
  );
}
