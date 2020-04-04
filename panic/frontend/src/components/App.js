import { bindActionCreators } from 'redux';
import {connect} from 'react-redux';
import Splash from './splash'

import * as authActions from './actions/auth'

function mapStateToProps(state) {
  return {
    state
  }
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(authActions, dispatch);
}

const App = connect(mapStateToProps, mapDispatchToProps)(Splash);

export default App;
