/* eslint react/no-multi-comp: 0, react/prop-types: 0 */

import React from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, Container, Form, FormGroup, Label, Input } from 'reactstrap';
import 'react-datepicker/dist/react-datepicker.min.css'

const NotesModal = (props) => {
  const {
    isOpen,
    notes,
    toggle,
  } = props;

  return (
    <Modal isOpen={isOpen} toggle={toggle} size='lg'>
      <ModalHeader toggle={toggle}>Additional notes</ModalHeader>
      <ModalBody>
        <Container>
          <Form>
            <FormGroup disabled>
              <Label for="menuDescription">Additional Notes</Label>
              <Input type="textarea" name="orderNotes" id="orderNotes" value={notes} />
            </FormGroup>
          </Form>
        </Container>

      </ModalBody>
      <ModalFooter>
        <Button color="secondary" onClick={toggle}>Cancel</Button>
      </ModalFooter>
    </Modal>
  );
}

export default NotesModal;