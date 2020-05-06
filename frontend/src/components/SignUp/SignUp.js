import React, { useState } from 'react';
import { Button, Form, FormGroup, Label, Input, Container, UncontrolledAlert } from 'reactstrap';
import { Link, useHistory } from 'react-router-dom';
import { toast } from 'react-toastify';

import { http } from "../../utils/http";

import '../Login/Login.css';

const Login = (props) => {
  const [error, setError] = useState({ error: false, message: '' });
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [first_name, setFirstname] = useState('');
  const [last_name, setLastname] = useState('');
  const history = useHistory();

  return (
    <Container className="themed-container login">
      {error.error && <UncontrolledAlert color="danger"> {error.message} </UncontrolledAlert>}
      <h2>Sign Up</h2>
      <Form className="form">
        <FormGroup>
          <Label for="exampleEmail">Email</Label>
          <Input type="email" name="email" onChange={event => setEmail(event.target.value)} id="exampleEmail" placeholder="" />
        </FormGroup>
        <FormGroup>
          <Label for="exampleFirst">First Name</Label>
          <Input type="text" name="firstname" onChange={event => setFirstname(event.target.value)} id="exampleFirst" placeholder="" />
        </FormGroup>
        <FormGroup>
          <Label for="exampleLast">Last Name</Label>
          <Input type="text" name="lastname" onChange={event => setLastname(event.target.value)} id="exampleLast" placeholder="" />
        </FormGroup>
        <FormGroup>
          <Label for="examplePassword">Password</Label>
          <Input type="password" name="password" onChange={event => setPassword(event.target.value)} id="examplePassword" placeholder="" />
        </FormGroup>

        <Button
          color="primary"
          disabled={!email || !password || !first_name || !last_name}
          onClick={async () => {
            try {
              await http.post('/api/v1/sign-up/', {
                email,
                password,
                first_name,
                last_name
              })
              toast.info('User created successfully.');
              history.push('/login');
            } catch (error) {
              toast.error('There was an error during the sign up process.')
              setError({
                error: true,
                message: JSON.stringify(error.response.data)
              })
            }
          }}
        >Sign Up</Button>
        <span style={{ 'float': 'right' }}>
          Already a member yet? <Link to={'/login'}>Sign In</Link>
        </span>

      </Form>
    </Container>

  );
}

export default Login;