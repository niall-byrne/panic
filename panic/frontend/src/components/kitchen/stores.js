import React, { Component, createRef } from "react";
import PropTypes from "prop-types";

class Stores extends Component {
  constructor(props) {
    super(props);    
    this.storeFormRef = createRef()
    this.storeNameRef = createRef();
    this.getAllStores = this.getAllStores.bind(this);
    this.addStoreForm = this.addStoreForm.bind(this);
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

  addStoreForm() {
    const { add } = this.props 
    const name = this.storeNameRef.current.value;
    add(name);
    this.storeFormRef.current.reset();
  }


  render() {
    const { stores, del } = this.props 
    const listStores = stores.map((d) => (
      <li key={d.name}>
        {`${d.id} - ${d.name} -> `}        
        <button name={`remove${d.id}`} onClick={() => del(d.id, d.name)} type="button">Remove</button>
      </li>
    ))
    return (
      <div>
        <span>Stores:</span>
        {listStores.length > 0 ? listStores : <li>None</li>}
        <form ref={this.storeFormRef} className="">
          <input type="text" ref={this.storeNameRef} placeholder="name" />                    
          <button type="button" onClick={this.addStoreForm}>Add A New Store</button>
        </form>                        
      </div>
    )
  }
}

Stores.propTypes = {
  token: PropTypes.string.isRequired,
  save: PropTypes.func.isRequired,
  add: PropTypes.func.isRequired,
  del: PropTypes.func.isRequired,
  stores: PropTypes.arrayOf(PropTypes.object)
};

Stores.defaultProps = {
  stores: []
}

export default Stores;
