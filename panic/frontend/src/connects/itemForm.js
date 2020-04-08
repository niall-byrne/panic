// Injects State Into the Main Component

import stateWrapper from './wrapper';
import ItemForm from '../components/kitchen/controls/itemForm';

import * as itemActions from '../actions/items';

function stateFilter(state) {
  return {
    state,
  };
}

function allActions() {
  return {
    ...itemActions,
  };
}

const StatefulItemForm = stateWrapper(ItemForm, allActions(), stateFilter);

export default StatefulItemForm;
