
import React, { useContext} from 'react';
import { Row, Col } from 'reactstrap';
import { UserContext } from "../../shared/userContext";
import Header from "./Header";
import MenuPage from "../Menus/MenuPage";
import OrderPage from "../Order/OrderPage";
import './App.css'

import { Switch, Route, Redirect } from 'react-router-dom';

const App = ({match}) => {

  const userContextValue = useContext(UserContext);
  const isAdmin = userContextValue.user.is_staff;

  return (
    <div className="wrapper">
      <Header />
      <Row className="total-height">
          <Col md="12" xs="12" sm="12" className="total-height no-padd">
            <div className="main-wrapper">
            <Switch>

              {isAdmin && <Route path={`${match.url}/menus`} component={MenuPage} />}
              {isAdmin && <Redirect to={`${match.url}/menus`} /> }

              {!isAdmin && <Route path={`${match.url}/orders`} component={OrderPage} />}
              {!isAdmin && <Redirect to={`${match.url}/orders`} /> }
  
            </Switch>
          </div>
        </Col>
      </Row>
    </div>
  )
}

export default App;

