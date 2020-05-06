/* eslint react/no-multi-comp: 0, react/prop-types: 0 */

import React, { useState, useEffect } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, UncontrolledAlert, Container, Form, FormGroup, Label, Input, Row, Col } from 'reactstrap';
import DatePicker from 'react-datepicker'
import { toast } from 'react-toastify';
import dayjs from 'dayjs'
import { http } from "../../utils/http";

const EditMenu = (props) => {
  const {
    isOpen,
    id,
    onMenuEdited,
    toggle,
  } = props;

  const [name, setName] = useState('');
  const [menuID, setMenuID] = useState('');
  const [description, setDescription] = useState('');
  const [date, setDate] = useState(new Date());
  const [optionList, setOption] = useState([]);
  const [error, setError] = useState({ error: false, message: '' });
  const [errors, setOptionError] = useState({});
  const [refresh, setRefresh] = useState(0);

  useEffect(() => {
    fetchMenu()
  }, [id, refresh])

  const fetchMenu = async () => {
    if (id) {
      const { data } = await http.get(`/api/v1/menus/${id}`)
      setMenu(data)
    }
  }

  const setMenu = (data) => {

    setMenuID(data.id)
    setName(data.name);
    setDescription(data.description);
    setDate(dayjs(data.available_date).toDate());
    setOptionError({});
    setError({ error: false, message: '' })
    setOption(data.options)
  }

  const editMenu = async () => {
    try {
      await http.put(`api/v1/menus/${menuID}`, {
        name,
        description,
        available_date: dayjs(date).format('YYYY-MM-DD'),
        options: []
      });
      onMenuEdited();
      toggle();
      toast.success('Menu saved successfully.');
    } catch (error) {
      toast.error('There was an error editing the menu, please check the details in the form.');
      console.error(error);
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
      if (!event) {
        options[index] = input;
      } else {
        options[index][input] = event.target.value;
      }
    }

    setOption(options)
  }

  const saveOption = async (option, index, remove) => {
    let data = null;

    try {
      if (option.id) {
        if (remove) {
          await http.delete(`api/v1/menus/${menuID}/options/${option.id}`)
          toast.success('Option deleted successfully.');

        } else {
          data = (await http.put(`api/v1/menus/${menuID}/options/${option.id}`, option)).data;
          toast.success('Option updated successfully.');
        }
      } else if (!remove) {

        data = (await http.post(`api/v1/menus/${menuID}/options`, option)).data;
        toast.success('Option saved successfully.');
      }

      handleOptionChange(index, data)

    } catch (error) {
      console.error(error);
      toast.error('There was an error processing the action, please check the details in the form.');
      setOptionError({
        ...errors,
        [index]: {
          error: true,
          message: JSON.stringify(error.response ? error.response.data : error)
        },
      })
    }
  }


  return (
    <Modal isOpen={isOpen} toggle={() => {setRefresh(refresh + 1); toggle();}} size='lg'>
      <ModalHeader toggle={() => {setRefresh(refresh + 1); toggle();}}>Edit Menu</ModalHeader>
      <ModalBody>
        <Container>
          {error.error && <UncontrolledAlert onClick={() => setError({ error: false, message: '' })} color="danger"> {error.message} </UncontrolledAlert>}
          <Form>

            <FormGroup>
              <Label for="menuName">Name</Label>
              <Input
                type="text"
                name="name"
                id="menuName"
                onChange={event => setName(event.target.value)}
                placeholder=""
                value={name}
              />
            </FormGroup>
            <FormGroup>
              <Label for="menuDescription">Description</Label>
              <Input type="textarea" name="text" id="menuDescription" value={description} onChange={event => setDescription(event.target.value)} />
            </FormGroup>
            <FormGroup>
              <Label style={{ marginRight: '10px' }} for="menuDate">Availability Date:  </Label>

              <DatePicker id="menuDate" dateFormat="yyyy-MM-dd" value={date} selected={date} onChange={event => setDate(event.target.value)} onChange={date => setDate(date)} />
            </FormGroup>
          </Form>
          <Container>

            {optionList.map((input, index) => (<Form key={index} style={{ 'position': 'relative' }}>
              {errors[index] && errors[index].error && <UncontrolledAlert  onClick={() => setOptionError({...error,  [index]: { error: false, message: '' }})} color="danger"> {errors[index].message} </UncontrolledAlert>}
              <Row form>
                <Button style={{ 'position': 'absolute', 'left': '610px', 'top': '-3px', 'cursor': 'pointer', zIndex:10 }} onClick={saveOption.bind(this, input, index, true)} close />
                <Col md={6}>
                  <FormGroup>
                    <Label for="optionName">Option Name</Label>
                    <Input
                      data-idx={index}
                      type="text"
                      name="name"
                      id="optionName"
                      placeholder=""
                      value={input ? input.name : ''}
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
                      value={input ? input.price : 0}
                      onChange={handleOptionChange.bind(this, index, 'price')}
                    />
                  </FormGroup>
                </Col>
              </Row>
              <FormGroup>
                <Label for="optionDescription">Option Description</Label>
                <Input type="textarea" data-idx={index} name="text" value={input ? input.description : ''} id="optionDescription" onChange={handleOptionChange.bind(this, index, 'description')} />
              </FormGroup>
              <Button className='pull-righst' onClick={saveOption.bind(this, input, index, false)} color="success" size="sm">Save</Button>
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
        <Button color="primary" onClick={editMenu}>Edit</Button>{' '}
        <Button color="secondary" onClick={() => {setRefresh(refresh + 1); toggle();}}>Cancel</Button>
      </ModalFooter>
    </Modal>
  );
}

export default EditMenu;