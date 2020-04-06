import React, { Component, createRef } from "react";
import PropTypes from "prop-types";

class Shelves extends Component {
  constructor(props) {
    super(props);
    this.shelfFormRef = createRef()
    this.shelfNameRef = createRef();
    this.getAllShelves = this.getAllShelves.bind(this);
    this.addShelfForm = this.addShelfForm.bind(this);
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

  addShelfForm() {
    const { add } = this.props 
    const name = this.shelfNameRef.current.value;
    add(name);
    this.shelfFormRef.current.reset();
  }


  render() {
    const { shelves, del } = this.props 
    const listShelves = shelves.map((d) => (
      <li key={d.name}>
        {`${d.id} - ${d.name} -> `}
        <button name={`remove${d.id}`} onClick={() => del(d.id, d.name)} type="button">Remove</button>
      </li> 
    ))
    return (
      <div>
        <span>Shelves:</span>
        {listShelves.length > 0 ? listShelves : <li>None</li>}
        <form ref={this.shelfFormRef} className="">
          <input type="text" ref={this.shelfNameRef} placeholder="name" />                    
          <button type="button" onClick={this.addShelfForm}>Add A New Store</button>
        </form>  
      </div>
    )
  }
}

Shelves.propTypes = {
  token: PropTypes.string.isRequired,
  save: PropTypes.func.isRequired,
  add: PropTypes.func.isRequired,
  del: PropTypes.func.isRequired,
  shelves: PropTypes.arrayOf(PropTypes.object)
};

Shelves.defaultProps = {
  shelves: []
}

export default Shelves;
