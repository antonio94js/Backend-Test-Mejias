import React, { useEffect, useState } from 'react';
import { Table } from 'reactstrap';
import ToolComponent from '../../shared/ToolComponent';
import { http } from "../../utils/http";
import NoteModal from "./NoteModal";

const OrderPage = () => {
  const [orders, setOrders] = useState([]);
  const [activeOrder, setActiveOrder] = useState('');
  const [modal, setModal] = useState(false);
  const [notes, setNotes] = useState('');

  useEffect(() => {
    fetchOrders()
  }, [])

  const fetchOrders = async () => {
    const { data } = await http.get('/api/v1/orders?expand=option')
    setOrders(data)
  }

  const openOrderNotes = (id, additionalNotes) => {
    setActiveOrder(id);
    setNotes(additionalNotes);
    toggle();
  }

  const toggle = () => setModal(!modal);

  const Row = ({ data }) => {
    return (
      <>
        <tr className="" >
          <td >{data.option.menu.name}</td>
          <td >{data.option.name}</td>
          <td >{data.created_at}</td>
          <td>
            <center>

              <ToolComponent
                placement="top"
                toolContent="Edit"
                componetContent={<i className="fa fa-pencil-square-o cursor grey-color" aria-hidden="true" />}
                Component="span"
                target={`EditOrder${data.id}`}
                className="cursor marg-betw-small"
                onClick={openOrderNotes.bind(this, data.id, data["additional_notes"])}
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
            <th>Menu name</th>
            <th>Selected option</th>
            <th>Order date </th>
            <th><center>Notes</center></th>
          </tr>
        </thead>
        <tbody className="fm-body-table">
          {orders.map(order => (<Row key={order.id} data={order} />))}
        </tbody>
      </Table>
      <NoteModal id={activeOrder} notes={notes} toggle={toggle} isOpen={modal} />

    </React.Fragment>
  );
}


export default OrderPage;
