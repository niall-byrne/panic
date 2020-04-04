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
    const { token, save } = this.props;
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
    const listShelves = shelves.map((d) => (
      <li key={d.name}>
        {`${d.id} - ${d.name} -> `}
        <button name={`add${d.id}`} type="button">Add</button>
        <button name={`remove${d.id}`} type="button">Remove</button>
      </li>
    ))
    return (
      <div>
        <span>Shelves:</span>
        {listShelves.length > 0 ? listShelves : <li>None</li>}
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
