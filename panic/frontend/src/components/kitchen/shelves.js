import React, { Component } from "react";
import PropTypes from "prop-types";

class Shelves extends Component {
  constructor(props) {
    super(props);
    this.getAllShelves = this.getAllShelves.bind(this);
  }

  componentDidMount() {
    this.getAllShelves();    
  }

  getAllShelves() {
    const { token } = this.props;
    const { save } = this.props;
    fetch(`${process.env.BASE_URL}/api/v1/shelf/`, {
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
    const { shelves } = this.props 
    const listItems = shelves.map((d) => <li key={d.name}>{d.name}</li>);
    return (
      <div>
        <span>Shelves:</span>
        {listItems}
      </div>
    )
  }
}

Shelves.propTypes = {
  token: PropTypes.string.isRequired,
  save: PropTypes.func.isRequired,
  shelves: PropTypes.arrayOf(PropTypes.object).isRequired
};

export default Shelves;
