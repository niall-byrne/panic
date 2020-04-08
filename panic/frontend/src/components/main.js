import React, { Component } from 'react';
import PropTypes from 'prop-types';
import LoginAuth from './authentication/login';
import LogoutAuth from './authentication/logout';

import StatefulShelves from '../connects/shelvesState';
import StatefulStores from '../connects/storesState';
import StatefulItem from '../connects/itemState';

// eslint-disable-next-line react/prefer-stateless-function
class Main extends Component {
  // TODO: Check if we are logged in when this component loads, by making a request with the cookie

  render() {
    const { state, login, logout } = this.props;
    const { profile, isAuthenticated } = state.auth;
    const content = isAuthenticated ? (
      <div className="section">
        <div>
          <p>Authenticated</p>
          <div>{profile.name}</div>
          <div>{profile.email}</div>
        </div>
        <LogoutAuth clear={logout} />
        <StatefulShelves />
        <StatefulStores />
        <StatefulItem />
      </div>
    ) : (
      <div>
        <LoginAuth save={login} />
      </div>
    );
    return <div className="Main">{content}</div>;
  }
}

Main.propTypes = {
  login: PropTypes.func.isRequired,
  logout: PropTypes.func.isRequired,
  state: PropTypes.shape({
    auth: PropTypes.shape({
      token: PropTypes.string,
      isAuthenticated: PropTypes.bool.isRequired,
      profile: PropTypes.shape({
        email: PropTypes.string,
        name: PropTypes.string,
      }).isRequired,
    }).isRequired,
  }).isRequired,
};

export default Main;
