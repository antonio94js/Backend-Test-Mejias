import React, { useEffect, useState } from 'react';
import { Table, Col, Row } from 'reactstrap';
import ToolComponent from '../../shared/ToolComponent';
import { http } from "../../utils/http";
import OrderList from "./OrderList";

const OrderPage = () => {
  // const [modal, setModal] = useState(false);

  // const toggle = () => setModal(!modal);

  return (
    <React.Fragment>
      <Row>
        <Col md={10}><h4>Your previous orders</h4></Col>
      </Row>
      <br></br>
      <OrderList/>
    </React.Fragment>
  );
}


export default OrderPage;
