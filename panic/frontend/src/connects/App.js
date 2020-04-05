import { bindActionCreators } from 'redux';
import {connect} from 'react-redux';
import Main from '../components/main'

import * as authActions from '../actions/auth'
import * as itemActions from '../actions/items'
import * as shelfActions from '../actions/shelves'
import * as storeActions from '../actions/stores'

function mapStateToProps(state) {
  return {
    state
  }
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators({
    ...authActions,
    ...itemActions,
    ...shelfActions,
    ...storeActions
  }, dispatch);  
}

const App = connect(mapStateToProps, mapDispatchToProps)(Main);

export default App;
