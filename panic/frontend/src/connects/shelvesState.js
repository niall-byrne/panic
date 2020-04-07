// Injects State Into the Shelves Component

import stateWrapper from './wrapper'
import Shelves from '../components/kitchen/shelves'

import * as shelfActions from '../actions/shelves'

function stateFilter(state) {
  return {
    shelves: state.shelves,
    auth: state.auth
  }
}

const StatefulShelves = stateWrapper(Shelves, shelfActions, stateFilter);

export default StatefulShelves;
