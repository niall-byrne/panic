import React, { Component, createRef } from "react";
import PropTypes from "prop-types";

class Shelves extends Component {
  constructor(props) {
    super(props);
    this.shelfFormRef = createRef()
    this.shelfNameRef = createRef();
    this.getAllShelves = this.getAllShelves.bind(this);
    this.add = this.add.bind(this);
    this.del = this.del.bind(this);
  }

  componentDidMount() {
    this.getAllShelves();    
  }

  getAllShelves() {
    const { syncShelves } = this.props;
    const { auth } = this.props;
    fetch(`${process.env.BASE_URL}/api/v1/shelf/`, {
      method: "GET",
      headers: {
        'Accept': 'application/json',
        'Authorization': `token ${auth.token}`
      },
    })
      .then(apiResponse => {       
        return apiResponse.json()
      })
      .then(apiResponseJSON => {
        syncShelves(apiResponseJSON);
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.debug(err);
      });
  }

  add(event) {
    event.preventDefault()
    const { shelves, addShelf } = this.props 
    const name = this.shelfNameRef.current.value;
    const search = shelves.find(o => o.name === name);
    // Crude Validation, TODO: Improve
    if (search === undefined && name.length > 0) addShelf(name);    
    this.shelfFormRef.current.reset();
  }

  del(shelf) {
    const { delShelf } = this.props 
    delShelf(shelf.id, shelf.name)
  }

  render() {
    const { shelves } = this.props 
    const listShelves = shelves.map((d) => (
      <li key={d.name}>
        {`${d.id} - ${d.name} -> `}
        <button name={`remove${d.id}`} onClick={() => this.del(d)} type="button">Remove</button>
      </li> 
    ))
    // TODO: Refactor the buttons into reusable components
    // TODO: Refactor the form into a reusable component
    return (
      <div>
        <span>Shelves:</span>
        {listShelves.length > 0 ? listShelves : <li>None</li>}
        <form ref={this.shelfFormRef} className="" onSubmit={this.add}>
          <input type="text" ref={this.shelfNameRef} placeholder="name" required />
          <button type="button" onClick={this.add}>Add A New Shelf</button>
        </form>  
      </div>
    )
  }
}

Shelves.propTypes = {
  syncShelves: PropTypes.func.isRequired,
  addShelf: PropTypes.func.isRequired,
  delShelf: PropTypes.func.isRequired,
  shelves: PropTypes.arrayOf(PropTypes.object),
  auth: PropTypes.shape({
    token: PropTypes.string
  }).isRequired
};

Shelves.defaultProps = {
  shelves: []
}

export default Shelves;
