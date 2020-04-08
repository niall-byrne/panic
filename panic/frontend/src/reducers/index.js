import { combineReducers } from 'redux';
import { connectRouter } from 'connected-react-router';

import auth from './auth';
import items from './items';
import shelves from './shelves';
import stores from './stores';

const createRootReducer = (history) =>
  combineReducers({
    router: connectRouter(history),
    auth,
    items,
    shelves,
    stores,
  });

export default createRootReducer;
