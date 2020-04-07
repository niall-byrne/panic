import React, { Component, createRef } from "react";
import PropTypes from "prop-types";

class Stores extends Component {
  constructor(props) {
    super(props);    
    this.storeFormRef = createRef()
    this.storeNameRef = createRef();
    this.getAllStores = this.getAllStores.bind(this);
    this.add = this.add.bind(this);
    this.del = this.del.bind(this);
  }

  componentDidMount() {
    this.getAllStores();
  }

  getAllStores() {
    const { syncStores } = this.props;
    const { auth } = this.props;
    fetch(`${process.env.BASE_URL}/api/v1/store/`, {
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
        syncStores(apiResponseJSON);
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.debug(err);
      });
  }

  add(event) {
    event.preventDefault()
    const { stores, addStore } = this.props 
    const name = this.storeNameRef.current.value;
    const search = stores.find(o => o.name === name);
    // Crude Validation, TODO: Improve
    if (search === undefined && name.length > 0) addStore(name);
    this.storeFormRef.current.reset();
  }

  del(shelf) {
    const { delStore } = this.props 
    delStore(shelf.id, shelf.name)
  }


  render() {
    const { stores } = this.props 
    const listStores = stores.map((d) => (
      <li key={d.name}>
        {`${d.id} - ${d.name} -> `}        
        <button name={`remove${d.id}`} onClick={() => this.del(d)} type="button">Remove</button>
      </li>
    ))
    return (
      <div>
        <span>Stores:</span>
        {listStores.length > 0 ? listStores : <li>None</li>}
        <form ref={this.storeFormRef} className="" onSubmit={this.add}>
          <input type="text" ref={this.storeNameRef} placeholder="name" required />
          <button type="button" onClick={this.add}>Add A New Store</button>
        </form>  
      </div>
    )
  }
}

Stores.propTypes = {
  syncStores: PropTypes.func.isRequired,
  addStore: PropTypes.func.isRequired,
  delStore: PropTypes.func.isRequired,
  stores: PropTypes.arrayOf(PropTypes.object),
  auth: PropTypes.shape({
    token: PropTypes.string
  }).isRequired
};

Stores.defaultProps = {
  stores: []
}

export default Stores;
