import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { Route } from 'react-router';
import { ConnectedRouter } from 'connected-react-router';
import configureStore, { history } from './store/store';
import defaultState from './store/init';
import './index.scss';

import statefulMain from './connects/mainState';

const store = configureStore(defaultState);

render(
  <Provider store={store}>
    <ConnectedRouter history={history}>
      <Route path="/" component={statefulMain} />
    </ConnectedRouter>
  </Provider>,
  document.getElementById('app'),
);
