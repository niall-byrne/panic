import React, { Component, createRef } from "react";
import PropTypes from "prop-types";
import RemovableRow from "./controls/removableRow"
import AppendFormRow from "./controls/appendableRow"

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
    fetch(`${process.env.BASE_URL}/api/v1/shelf/`, {
      method: "GET",
      headers: {
        'Accept': 'application/json'
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
    const refs = {
      inputRef: this.shelfNameRef,
      formRef: this.shelfFormRef
    }
    const listStores = shelves.map((d) => (
      <RemovableRow key={d.id} row={d} controlFn={this.del} controlName="Remove" />
    ))
    const ul = (
      <ul id="shelfList">
        {listStores.length > 0 ? listStores : <li className="section">None</li>}
        <AppendFormRow init="shelf name" refs={refs} text="Add Shelf" submit={this.add} />
      </ul>
    )
    return (
      <div className="component">
        <span>Shelves:</span>
        {ul}
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
