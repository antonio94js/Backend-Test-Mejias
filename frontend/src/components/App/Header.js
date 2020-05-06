import React, { useContext } from 'react';
import { UserContext } from '../../shared/userContext';
import { NavLink } from 'react-router-dom'
import {
  Navbar,
  Nav,
  NavItem,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem
} from 'reactstrap';

const Header = () => {
  const userContextValue = useContext(UserContext);
  const isAdmin = userContextValue.user.is_staff;

  return (
    <header>
      <Navbar color="faded" light expand="md">
        <NavLink className="plain-a" to="/dashboard">
        </NavLink>
        
        <Nav className="ml-auto" navbar>
          <NavItem className="mar-betw-med pull-left">
            
            
        </NavItem> 
        
          <NavItem className="mar-betw-med">
            <UncontrolledDropdown>
              <DropdownToggle tag="div" className="drop-header-padding ">

                <span className="marg-betw-small cursor element-drop" >
                  {userContextValue.user.name}
                </span>

              </DropdownToggle>
              <DropdownMenu>
                <DropdownItem className="cursor" onClick={userContextValue.logout}><i className="fa fa-sign-out" aria-hidden="true"></i>&nbsp;Log Out</DropdownItem>
              </DropdownMenu>
            </UncontrolledDropdown>
          </NavItem>
        </Nav>
      </Navbar>
    </header>)
}

export default Header;
