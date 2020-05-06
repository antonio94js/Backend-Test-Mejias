/* eslint react/no-multi-comp: 0, react/prop-types: 0 */

import React, { useState, useContext } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, UncontrolledAlert, Container, Form, FormGroup, Label, Input } from 'reactstrap';
import { toast } from 'react-toastify';
import { Link } from "react-router-dom";
import { http } from "../../utils/http";
import { UserContext } from "../../shared/userContext";

const PlaceOrder = (props) => {
  const {
    isOpen,
    option_id,
    toggle,
  } = props;

  const [additionalNotes, setAdditionalNotes] = useState('');
  const userContextValue = useContext(UserContext);
  const [error, setError] = useState({ error: false, message: '' });

  const isLoggedIn = !!userContextValue.token;

  const cleanState = () => {
    setAdditionalNotes('');
    setError({ error: false, message: '' });
  }

  const placeOrder = async () => {
    try {
      await http.post('api/v1/orders', {
        additional_notes: additionalNotes,
        option_id
      });
      cleanState();
      toggle();
      toast.success('Order placed successfully.');

    } catch (error) {
      toast.error('There was an error placing your order.');

      console.error(error)
      setError({
        error: true,
        message: JSON.stringify(error.response ? error.response.data : error)
      })
    }
  }

  return (
    <Modal isOpen={isOpen} toggle={toggle} size='lg'>
      <ModalHeader toggle={toggle}>Place a new order</ModalHeader>
      <ModalBody>
        <Container>
          {error.error && <UncontrolledAlert onClick={() => setError({ error: false, message: '' })} color="danger"> {error.message} </UncontrolledAlert>}
          {isLoggedIn &&
            <Form>
              <FormGroup>
                <Label for="menuDescription">Additional Notes</Label>
                <Input type="textarea" name="orderNotes" id="orderNotes" onChange={event => setAdditionalNotes(event.target.value)} />
              </FormGroup>
            </Form>
          }
          {!isLoggedIn &&
            <div>
              To place a new order please <Link to={'/login'} target="_blank">sign in</Link> first, after that come back here and refresh to place an order :) If you don't have an active account do not hesitate to <Link to={'/sign-up'} target="_blank">sign up</Link>
            </div>
          }

        </Container>

      </ModalBody>
      <ModalFooter>
        <Button color="primary" onClick={placeOrder}>Place order</Button>{' '}
        <Button color="secondary" onClick={() => { cleanState(); toggle(); }}>Cancel</Button>
      </ModalFooter>
    </Modal>
  );
}

export default PlaceOrder;