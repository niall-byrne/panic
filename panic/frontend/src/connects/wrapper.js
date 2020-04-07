import { bindActionCreators } from 'redux';
import {connect} from 'react-redux';

function wrapDispatchToProps(actions) {
  return function mapDispatchToProps(dispatch) {
    return bindActionCreators({
      ...actions,
    }, dispatch);  
  }
}

function stateWrapper(component, actions, stateFilter) {
  const dispatchPatcher = wrapDispatchToProps(actions)
  return connect(stateFilter, dispatchPatcher)(component)
}

export default stateWrapper;
