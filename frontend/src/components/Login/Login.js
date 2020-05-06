import React, { useContext, useState } from 'react';
import { UserContext } from '../../shared/userContext';
import { Button, Form, FormGroup, Label, Input, Container, UncontrolledAlert } from 'reactstrap';
import { Link, useHistory } from 'react-router-dom';
import { toast } from 'react-toastify';
import { http } from "../../utils/http";

import './Login.css';

const Login = (props) => {
  const userContextValue = useContext(UserContext);
  const history = useHistory();
  const [error, setError] = useState({ error: false, message: '' });
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (

    <Container className="themed-container login">
      {error.error && <UncontrolledAlert color="danger"> {error.message} </UncontrolledAlert>}
      <h2>Sign In</h2>
      <Form className="form">
        <FormGroup>
          <Label for="exampleEmail">Email</Label>
          <Input type="email" name="email" onChange={event => setEmail(event.target.value)} id="exampleEmail" placeholder="" />
        </FormGroup>
        <FormGroup>
          <Label for="examplePassword">Password</Label>
          <Input type="password" name="password" onChange={event => setPassword(event.target.value)} id="examplePassword" placeholder="" />
        </FormGroup>

        <Button
          color="primary"
          disabled={!email || !password}
          onClick={async () => {
            console.log({
              variables: {
                email,
                password,
              },
            });
            try {
              const { data } = await http.post('/api/token', {
                email,
                password,
              })

              userContextValue.setToken(data.access);
              history.push("/app");
              
              toast.info('Welcome.');
            } catch (error) {

              console.log(error);
              setError({
                error: true,
                message: JSON.stringify(error.response.data)
              })
            }
          }}
        >Sign in</Button>
        <span style={{ 'float': 'right' }}>
          Not a member yet? <Link to={'/sign-up'}>Create an account</Link>
        </span>

      </Form>
    </Container>
  );
}

export default Login;