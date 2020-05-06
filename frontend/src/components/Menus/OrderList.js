/* eslint react/no-multi-comp: 0, react/prop-types: 0 */

import React, { useState, useEffect } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, ListGroup, ListGroupItem, ListGroupItemText,ListGroupItemHeading } from 'reactstrap';
import { http } from "../../utils/http";

const ModalExample = (props) => {
  const {
    isOpen,
    id,
    toggle,
  } = props;

  const [orders, setOrders] = useState([])


  useEffect(() => {
    fetchOrders()
  }, [id])

  const fetchOrders = async () => {
    if (id) {
      const { data } = await http.get(`/api/v1/menus/${id}/orders?expand=user,option`)
      setOrders(data)
    }
  }


  const Orders = ({ data }) => (
    <ListGroupItem>
      <ListGroupItemText>
        <p><b>Requester:</b> {`${data.user.first_name} ${data.user.last_name}`}</p>
        <p><b>Option:</b> {data.option.name}</p>
        <p><b>Notes:</b> {data.additional_notes}</p>
        <p><b>Price:</b> {data.option.price}</p>
      </ListGroupItemText>
    </ListGroupItem>
  )
console.log(id);
  return (
    <Modal isOpen={isOpen} toggle={toggle}>
      <ModalHeader toggle={toggle}>Menu Orders</ModalHeader>
      <ModalBody>
        <ListGroup>
          {
            orders.length > 0 ? orders.map((order) => <Orders key={order.id} data={order}></Orders>) : 'There is not any order for this menu'
          }
        </ListGroup>
      </ModalBody>
      <ModalFooter>
        <Button color="secondary" onClick={toggle}>Cancel</Button>
      </ModalFooter>
    </Modal>
  );
}

export default ModalExample;