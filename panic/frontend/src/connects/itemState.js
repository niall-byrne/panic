// Injects State Into the Main Component

import stateWrapper from './wrapper';
import Item from '../components/kitchen/items';

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

const StatefulItem = stateWrapper(Item, allActions(), stateFilter);

export default StatefulItem;
