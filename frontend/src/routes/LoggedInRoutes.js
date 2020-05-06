import React from 'react';
import { Route, Switch, Redirect } from 'react-router-dom';

import App from '../components/App/App';

const LoggedInRoutes = () => {

  return (
    <Switch>
      <Route path={'/app'} component={App} />
      <Redirect to={'/app'} />
    </Switch>
  );
};

export default LoggedInRoutes;