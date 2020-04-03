import React, { Component } from "react";
import PropTypes from "prop-types";

class Stores extends Component {
  constructor(props) {
    super(props);
    this.getAllStores = this.getAllStores.bind(this);
  }

  componentDidMount() {
    this.getAllStores();
  }

  getAllStores() {
    const { token, save } = this.props;
    fetch(`${process.env.BASE_URL}/api/v1/store/`, {
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
    const { stores } = this.props 
    const listItems = stores.map((d) => <li key={d.name}>{d.name}</li>);
    return (
      <div>
        <span>Stores:</span>
        {listItems}
      </div>
    )
  }
}

Stores.propTypes = {
  token: PropTypes.string.isRequired,
  save: PropTypes.func.isRequired,
  stores: PropTypes.arrayOf(PropTypes.object).isRequired
};

export default Stores;
