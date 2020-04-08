import { createBrowserHistory } from 'history';
import { applyMiddleware, compose, createStore } from 'redux';
import { routerMiddleware } from 'connected-react-router';

// root reducer
import createRootReducer from '../reducers';

export const history = createBrowserHistory();

function configureStore(initialState) {
  const composeEnhancer =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  const store = createStore(
    createRootReducer(history),
    initialState,
    composeEnhancer(applyMiddleware(routerMiddleware(history))),
  );
  return store;
}

export default configureStore;
