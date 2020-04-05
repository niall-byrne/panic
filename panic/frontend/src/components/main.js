import React, { Component } from "react";
import PropTypes from 'prop-types';
import LoginAuth from "./authentication/login"
import LogoutAuth from "./authentication/logout"
import Shelves from './kitchen/shelves';
import Stores from './kitchen/stores';
import Items from './kitchen/items';


// eslint-disable-next-line react/prefer-stateless-function
class Main extends Component {
  
  render() {
    const {state, login, logout, shelves, stores, items} = this.props
    const { syncShelves, syncStores, syncItems} = this.props
    const {profile, isAuthenticated, token} = state.auth
    const content = isAuthenticated ? (
      <div>
        <div>
          <p>Authenticated</p>
          <div>{profile.name}</div>
          <div>{profile.email}</div>
        </div>
        <LogoutAuth token={token} clear={logout} />
        <Shelves token={token} save={syncShelves} shelves={shelves} />
        <Stores token={token} save={syncStores} stores={stores} />
        <Items token={token} save={syncItems} items={items} />
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
  syncShelves: PropTypes.func.isRequired,
  syncStores: PropTypes.func.isRequired,
  syncItems: PropTypes.func.isRequired,
  shelves: PropTypes.arrayOf(PropTypes.object),
  items: PropTypes.arrayOf(PropTypes.object),
  stores: PropTypes.arrayOf(PropTypes.object),
  state: PropTypes.shape({
    auth: PropTypes.shape({
      token: PropTypes.string,
      isAuthenticated: PropTypes.bool.isRequired,
      profile: PropTypes.shape({
        email: PropTypes.string,
        name: PropTypes.string
      }).isRequired
    }).isRequired
  }).isRequired
};

Main.defaultProps = {
  items: [],
  shelves: [],
  stores: []
}

export default Main;
