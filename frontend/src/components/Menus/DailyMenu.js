import React, { useState, useEffect, useContext } from "react";
import { ListGroup, ListGroupItem, ListGroupItemHeading, ListGroupItemText, Container, UncontrolledAlert } from 'reactstrap';
import { useParams, Link } from 'react-router-dom';
import ToolComponent from "../../shared/ToolComponent";
import { http } from "../../utils/http";
import OrderModal from "../Order/OrderModal";
import { UserContext } from "../../shared/userContext";

const DailyMenu = () => {
  let { id } = useParams();
  const [menu, setMenu] = useState({});
  const [modal, setModal] = useState(false);
  const [activeOption, setActiveOption] = useState('');
  const userContextValue = useContext(UserContext);
  const isLoggedIn = !!userContextValue.token

  const [error, setError] = useState({ error: false, message: '' });

  useEffect(() => {
    fetchDailyMenu()

  }, [])

  const openOrderModal = (id) => {
    setActiveOption(id)
    setModal(!modal);
  };

  const fetchDailyMenu = async () => {
    try {
      const { data } = await http.get(`/api/v1/daily-menu/${id}`)
      setMenu(data)
    } catch (error) {
      setError({
        error: true,
        message: JSON.stringify(error.response ? error.response.data : error)
      })
    }
  }
  return (
    <Container style={{ padding: '80px 30px 30px 30px' }}>
      {error.error && <UncontrolledAlert color="danger"> {error.message} </UncontrolledAlert>}
      {!error.error && <div>

        {isLoggedIn &&
          <div>
            <Link to={'/app'}> Go to dashboard</Link>
          </div>
        }

        <h4>Welcome to the daily Menu {menu.name}</h4>
        <h5>{menu.description}</h5>
        <br></br>

        <ListGroup>
          {menu && menu.options && menu.options.map((option) => (
            <ListGroupItem key={option.id} >
              <ListGroupItemHeading>{option.name}</ListGroupItemHeading>
              <ListGroupItemText>
                <div>
                  {option.description}
                  <ToolComponent
                    placement="top"
                    toolContent="Order"
                    componetContent={<i className="fa fa-cutlery cursor grey-color" aria-hidden="true" />}
                    Component="span"
                    style={{ float: 'right', fontSize: '22px', color: 'color' }}
                    target={`OrderMenu`}
                    className="cursor marg-betw-small"
                    onClick={openOrderModal.bind(this, option.id)}
                  />
                </div>
                <div><b>Price:</b> $ {option.price}</div>

              </ListGroupItemText>
            </ListGroupItem>
          ))}
        </ListGroup>
        <OrderModal isOpen={modal} toggle={setModal} option_id={activeOption} ></OrderModal>
      </div>}
    </Container>
  );
}

export default DailyMenu