import React, { Component, createRef } from 'react';
import PropTypes from 'prop-types';
import RemovableRow from './controls/removableRow';
import AppendFormRow from './controls/appendableRow';

class Stores extends Component {
  constructor(props) {
    super(props);
    this.storeFormRef = createRef();
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
    fetch(`${process.env.BASE_URL}/api/v1/store/`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    })
      .then((apiResponse) => {
        return apiResponse.json();
      })
      .then((apiResponseJSON) => {
        syncStores(apiResponseJSON);
      })
      .catch((err) => {
        // eslint-disable-next-line no-console
        console.debug(err);
      });
  }

  add(event) {
    event.preventDefault();
    const { stores, addStore } = this.props;
    const name = this.storeNameRef.current.value;
    const search = stores.find((o) => o.name === name);
    // Crude Validation, TODO: Improve
    if (search === undefined && name.length > 0) addStore(name);
    this.storeFormRef.current.reset();
  }

  del(shelf) {
    const { delStore } = this.props;
    delStore(shelf.id, shelf.name);
  }

  render() {
    const { stores } = this.props;
    const refs = {
      inputRef: this.storeNameRef,
      formRef: this.storeFormRef,
    };
    const listStores = stores.map((d) => (
      <RemovableRow
        key={d.id}
        row={d}
        controlFn={this.del}
        controlName="Remove"
      />
    ));
    const ul = (
      <ul id="storeList">
        {listStores.length > 0 ? listStores : <li className="section">None</li>}
        <AppendFormRow
          init="store name"
          refs={refs}
          text="Add Store"
          submit={this.add}
        />
      </ul>
    );
    return (
      <div className="component">
        <span>Stores:</span>
        {ul}
      </div>
    );
  }
}

Stores.propTypes = {
  syncStores: PropTypes.func.isRequired,
  addStore: PropTypes.func.isRequired,
  delStore: PropTypes.func.isRequired,
  stores: PropTypes.arrayOf(PropTypes.object),
  auth: PropTypes.shape({
    token: PropTypes.string,
  }).isRequired,
};

Stores.defaultProps = {
  stores: [],
};

export default Stores;
