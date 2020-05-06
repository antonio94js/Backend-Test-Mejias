import React, { useState } from 'react';
import { Button, Col, Row } from 'reactstrap';
import MenuList from "./MenuList";
import ModalCreate from "./ModalCreate";

const MenuPage = (props) => {
  const [modal, setModal] = useState(false);
  const [refresh, setRefresh] = useState(0);

  const toggle = () => setModal(!modal);

  const onMenuCreate = () => setRefresh(refresh + 1);

  return (
    <React.Fragment>
      <Row>
          
        <Col md={10}><h4>Welcome to the menu management page</h4></Col>
        <Col md={2}><Button onClick={toggle} color="primary" size="sm">Create menu</Button></Col>
      </Row>
      <br/>
      
      <MenuList  refresh={refresh}/>
      <ModalCreate isOpen={modal} toggle={toggle} onMenuCreate={onMenuCreate}/>
    </React.Fragment>
  );
}


export default MenuPage;
