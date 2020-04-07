import React, { Component } from "react";
import PropTypes from "prop-types";

class Items extends Component {
  constructor(props) {
    super(props);
    this.getAllItem = this.getAllItems.bind(this);
  }

  componentDidMount() {
    this.getAllItems();
  }

  getAllItems() {
    const { token, save } = this.props;
    fetch(`${process.env.BASE_URL}/api/v1/item/`, {
      method: "GET",
      headers: {
        'Accept': 'application/json',
        'Authorization': `token ${token}`
      },
    })
      .then(apiResponse => {       
        return apiResponse.json()
      })
      .then(apiResponseJSON => {
        save(apiResponseJSON);
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.debug(err);
      });
  }

  render() {
    const { items, add, del } = this.props 
    const listItems = items.map((d) => (
      <li key={d.name}>
        {`${d.id} - ${d.name} - qty: ${d.quantity} -> `}
        <button name={`add${d.id}`} onClick={() => add(d.name)} type="button">Add</button>
        <button name={`remove${d.id}`} onClick={() => del(d.id, d.name)} type="button">Remove</button>
      </li>
    ))
    return (
      <div className="section">
        <span>Items:</span>
        {listItems.length > 0 ? listItems : <li>None</li>}
      </div>
    )
  }
}

Items.propTypes = {
  token: PropTypes.string.isRequired,
  save: PropTypes.func.isRequired,
  add: PropTypes.func.isRequired,
  del: PropTypes.func.isRequired,
  items: PropTypes.arrayOf(PropTypes.object)
};

Items.defaultProps = {
  items: []
}

export default Items;
