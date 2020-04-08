import React, { Component } from 'react';
import PropTypes from 'prop-types';
import StatefulItemForm from '../../connects/itemForm';
import RemovableRow from './controls/removableRow';

class Items extends Component {
  constructor(props) {
    super(props);
    this.getAllItem = this.getAllItems.bind(this);
    this.add = this.add.bind(this);
    this.del = this.del.bind(this);
  }

  componentDidMount() {
    this.getAllItems();
  }

  getAllItems() {
    // I need to fetch all data used here
    // Not just relying on shared state
    // State is not a source of truth, the API is the source of truth

    const { syncItems } = this.props;
    fetch(`${process.env.BASE_URL}/api/v1/item/`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    })
      .then((apiResponse) => {
        return apiResponse.json();
      })
      .then((apiResponseJSON) => {
        syncItems(apiResponseJSON);
      })
      .catch((err) => {
        // eslint-disable-next-line no-console
        console.debug(err);
      });
  }

  add(formData) {
    const { addItem } = this.props;
    addItem(formData);
  }

  del(item) {
    const { delItem } = this.props;
    delItem(item.id, item.name);
  }

  render() {
    const { state } = this.props;
    const { items } = state;
    const listItems = items.map((d) => (
      <RemovableRow
        key={d.name}
        row={d}
        controlFn={this.del}
        controlName="Remove"
      />
    ));
    return (
      <div className="component">
        <span>Items:</span>
        {listItems.length > 0 ? listItems : <li>None</li>}
        <StatefulItemForm submit={this.add} />
      </div>
    );
  }
}

Items.propTypes = {
  syncItems: PropTypes.func.isRequired,
  addItem: PropTypes.func.isRequired,
  delItem: PropTypes.func.isRequired,
  state: PropTypes.shape({
    items: PropTypes.arrayOf(PropTypes.object),
  }).isRequired,
};

export default Items;
