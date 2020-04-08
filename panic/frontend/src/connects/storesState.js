// Injects State Into the Store Component

import stateWrapper from './wrapper';
import Stores from '../components/kitchen/stores';

import * as storeActions from '../actions/stores';

function stateFilter(state) {
  return {
    stores: state.stores,
    auth: state.auth,
  };
}

const StatefulStores = stateWrapper(Stores, storeActions, stateFilter);

export default StatefulStores;
