import React, { Component } from "react";
import PropTypes from 'prop-types';
import LoginAuth from "./authentication/login"
import LogoutAuth from "./authentication/logout"

import Items from './kitchen/items';
import StatefulShelves from '../connects/shelvesState';
import StatefulStores from '../connects/storesState';


// eslint-disable-next-line react/prefer-stateless-function
class Main extends Component {
  
  render() {
    // TODO: breakout state into individual connects for each high level component
    // items
    const {syncItems, addItem, delItem} = this.props

    const {state, login, logout} = this.props    
    const {profile, isAuthenticated, token} = state.auth
    const content = isAuthenticated ? (
      <div className="section">
        <div>
          <p>Authenticated</p>
          <div>{profile.name}</div>
          <div>{profile.email}</div>
        </div>
        <LogoutAuth token={token} clear={logout} />
        <StatefulShelves />
        <StatefulStores />
        <Items token={token} save={syncItems} add={addItem} del={delItem} items={state.items} />
      </div>
    ) : (
      <div>
        <LoginAuth save={login} />
      </div>
    );
    return <div className="Main">{content}</div>;
  }
}


// TODO: This is too much state to pass down a level, using more connects might be ideal
Main.propTypes = {
  login: PropTypes.func.isRequired,
  logout: PropTypes.func.isRequired,
  addItem: PropTypes.func.isRequired,
  delItem: PropTypes.func.isRequired,
  syncItems: PropTypes.func.isRequired,  
  state: PropTypes.shape({
    items: PropTypes.arrayOf(PropTypes.object),
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

export default Main;
