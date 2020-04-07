// Injects State Into the Main Component

import stateWrapper from './wrapper'
import Main from '../components/main'

import * as authActions from '../actions/auth'
import * as itemActions from '../actions/items'

function stateFilter(state) {
  return {
    state
  }
}

function allActions() {
  return {
    ...authActions,
    ...itemActions,
  };  
}

const StatefulMain = stateWrapper(Main, allActions(), stateFilter);

export default StatefulMain;
