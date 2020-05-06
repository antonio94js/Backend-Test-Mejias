/* eslint react/no-multi-comp: 0, react/prop-types: 0 */

import React, { useState } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, UncontrolledAlert, Container, Form, FormGroup, Label, Input, Row, Col } from 'reactstrap';
import DatePicker from 'react-datepicker'
import { toast } from 'react-toastify';
import dayjs from 'dayjs'
import { http } from "../../utils/http";

const CreateMenu = (props) => {
  const {
    isOpen,
    onMenuCreate,
    toggle,
  } = props;

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [date, setDate] = useState(new Date());
  const [optionList, setOption] = useState([]);
  const [error, setError] = useState({ error: false, message: '' });


  const cleanState = () => {
    setName('');
    setDescription('');
    setDate(new Date());
    setError({ error: false, message: '' });
    setOption([])
  }


  const createMenu = async () => {
    try {
      const { data } = await http.post('api/v1/menus', {
        name,
        description,
        available_date: dayjs(date).format('YYYY-MM-DD'),
        options: optionList
      }); 
      onMenuCreate();
      cleanState();
      toggle();
      toast.success('Menu created successfully.');
    } catch (error) {
      console.error(error);
      toast.error('There was an error creating the Menu, please check the details on the top.');
      setError({
        error: true,
        message: JSON.stringify(error.response ? error.response.data : error)
      })
    }
  }

  const handleOptionChange = (index, input, event) => {

    const options = [...optionList];

    if (!input) {
      options.splice(index, 1)
    } else {
      options[index][input] = event.target.value;
    }
    setOption(options)

  }


  return (
    <Modal isOpen={isOpen} toggle={toggle} size='lg'>
      <ModalHeader toggle={toggle}>Create new Menu</ModalHeader>
      <ModalBody>
        <Container>
          {error.error && <UncontrolledAlert color="danger"> {error.message} </UncontrolledAlert>}
          <Form>

            <FormGroup>
              <Label for="menuName">Name</Label>
              <Input
                type="text"
                name="name"
                id="menuName"
                onChange={event => setName(event.target.value)}
                placeholder=""
              />
            </FormGroup>
            <FormGroup>
              <Label for="menuDescription">Description</Label>
              <Input type="textarea" name="text" id="menuDescription" onChange={event => setDescription(event.target.value)} />
            </FormGroup>
            <FormGroup>
              <Label style={{ marginRight: '10px' }} for="menuDate">Availability Date:  </Label>

              <DatePicker id="menuDate" dateFormat="yyyy-MM-dd" selected={date} onChange={event => setDate(event.target.value)} onChange={date => setDate(date)} />
            </FormGroup>
          </Form>
          <Container>

            {optionList.map((input, index) => (<Form key={index} style={{ 'position': 'relative' }}>
              <Row form>
              <Button style={{ 'position': 'absolute', 'left': '610px', 'top': '-3px', 'cursor': 'pointer', zIndex:10 }} onClick={handleOptionChange.bind(this, index, null)} close />
                <Col md={6}>
                  <FormGroup>
                    <Label for="optionName">Option Name</Label>
                    <Input
                      data-idx={index}
                      type="text"
                      name="name"
                      id="optionName"
                      placeholder=""
                      value={input.name}
                      onChange={handleOptionChange.bind(this, index, 'name')}
                    />
                  </FormGroup>
                </Col>
                <Col md={6}>
                  <FormGroup>
                    <Label for="optionNumber">Option Price:</Label>
                    <Input
                      data-idx={index}
                      type="number"
                      name="optionNumber"
                      id="exampleNumber"
                      placeholder="number placeholder"
                      value={input.price}
                      onChange={handleOptionChange.bind(this, index, 'price')}
                    />
                  </FormGroup>
                </Col>
              </Row>
              <FormGroup>
                <Label for="optionDescription">Option Description</Label>
                <Input type="textarea" data-idx={index} name="text" value={input.description} id="optionDescription" onChange={handleOptionChange.bind(this, index, 'description')} />
              </FormGroup>
              <hr></hr>
            </Form>))}

            <Button onClick={() => {
              setOption([...optionList, {
                name: '',
                description: '',
                price: 0,
              }]);
            }} style={{ float: 'right' }} color="primary" size="sm">Add option</Button>

          </Container>
        </Container>

      </ModalBody>
      <ModalFooter>
        <Button color="primary" onClick={createMenu}>Create</Button>{' '}
        <Button color="secondary" onClick={() => {cleanState();toggle();}}>Cancel</Button>
      </ModalFooter>
    </Modal>
  );
}

export default CreateMenu;