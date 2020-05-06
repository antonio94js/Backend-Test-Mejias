
import React, { useContext } from 'react';
import { Route, Switch, Redirect } from 'react-router-dom';

import { UserContext } from '../shared/userContext';
import Login from '../components/Login/Login';
import SignUp from '../components/SignUp/SignUp';
import DailyMenu from '../components/Menus/DailyMenu';
import LoggedInRoutes from './LoggedInRoutes';

export default function Routes() {
  const userContextValue = useContext(UserContext);
  const isLoggedIn = !!userContextValue.token;

  return (
    <Switch>
      <Route path={'/menu/:id'} component={DailyMenu}/>
      
      {!isLoggedIn && <Route path={'/login'} component={Login} />}
      {!isLoggedIn && <Route path={'/sign-up'} component={SignUp} />}
      {!isLoggedIn && <Redirect to="/login" />}

      {isLoggedIn && <Route component={LoggedInRoutes} />}
    </Switch>
  );
}
