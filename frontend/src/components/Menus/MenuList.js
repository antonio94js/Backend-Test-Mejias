import React, { useEffect, useState } from 'react';
import { Table } from 'reactstrap';
import ToolComponent from '../../shared/ToolComponent';
import { http } from "../../utils/http";
import OrderList from "./OrderList";
import MenuEdit from "./MenuEdit";

const MenuList = ({ refresh }) => {
  const [menus, setMenu] = useState([])
  const [modal, setModal] = useState(false);
  const [activeMenu, setActiveOrderMenu] = useState('');
  const [editModal, setEditModal] = useState(false);
  const [editRefresh, setEditRefresh] = useState(0);

  useEffect(() => {
    fetchMenus()

  }, [refresh, editRefresh])

  const fetchMenus = async () => {
    const { data } = await http.get('/api/v1/menus')
    console.log({data});
    setMenu(data)
  }

  const openOrderModal = (id) => {
    setActiveOrderMenu(id);
    toggle();
  }
  const openEditModal = (id) => {
    setActiveOrderMenu(id);
    toggleEdit();
  }

  const toggle = () => setModal(!modal);

  const toggleEdit = () => setEditModal(!editModal);

  const onMenuEdited = () => setEditRefresh(editRefresh + 1);

  const Row = ({ data }) => {
    return (
      <>
      <tr className="" >
        <td >{data.name}</td>
        <td >{data.description}</td>
        <td >{data.available_date}</td>
        <td>
          <center>

            <ToolComponent
              placement="top"
              toolContent="Edit"
              componetContent={<i className="fa fa-pencil-square-o cursor grey-color" aria-hidden="true" />}
              Component="span"
              target={`EditMenu${data.id}`}
              className="cursor marg-betw-small" 
              onClick={openEditModal.bind(this, data.id)}
              />

            <ToolComponent
              placement="top"
              toolContent="Orders"
              componetContent={<i className="fa fa-cutlery cursor grey-color" aria-hidden="true" />}
              Component="span"
              target={`ShowOrders${data.id}`}

              className="cursor marg-betw-small" 
              onClick={openOrderModal.bind(this, data.id)}
              />   

          </center>
        </td>
      </tr>
      </>
    );
  }
  
  return (
    <React.Fragment>
      <Table hover striped responsive className="fm-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Availability date </th>
            <th><center>Acciones</center></th>
          </tr>
        </thead>
        <tbody className="fm-body-table">
          {menus.map(menu => (<Row key={menu.id} data={menu}/>))}
        </tbody>
      </Table>
      <OrderList id={activeMenu} toggle={toggle} isOpen={modal}/>
      <MenuEdit id={activeMenu} toggle={toggleEdit} isOpen={editModal} onMenuEdited={onMenuEdited}/>
      
    </React.Fragment>
    
  );
}

export default MenuList;