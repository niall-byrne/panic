import React, { Component } from "react";
import PropTypes from 'prop-types';
import LoginAuth from "./authentication/login"
import LogoutAuth from "./authentication/logout"
import StatefulShelves from './kitchen/shelves';
import Stores from './kitchen/stores';
import Items from './kitchen/items';


// eslint-disable-next-line react/prefer-stateless-function
class Main extends Component {
  
  render() {
    // TODO: breakout state into individual connects for each high level component
    // shelves
    const {syncShelves, addShelf, delShelf} = this.props
    // items
    const {syncItems, addItem, delItem} = this.props
    // stores
    const {syncStores, addStore, delStore} = this.props

    // TODO: I'm unsure on how to pass state to these profile components efficiently
    // Will do some reading

    const {state, login, logout} = this.props    
    const {profile, isAuthenticated, token} = state.auth
    const content = isAuthenticated ? (
      <div>
        <div>
          <p>Authenticated</p>
          <div>{profile.name}</div>
          <div>{profile.email}</div>
        </div>
        <LogoutAuth token={token} clear={logout} />
        <StatefulShelves />
        <Stores token={token} save={syncStores} add={addStore} del={delStore} stores={state.stores} />
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
  addShelf: PropTypes.func.isRequired,
  addItem: PropTypes.func.isRequired,
  addStore: PropTypes.func.isRequired,
  delShelf: PropTypes.func.isRequired,
  delItem: PropTypes.func.isRequired,
  delStore: PropTypes.func.isRequired,
  syncShelves: PropTypes.func.isRequired,
  syncStores: PropTypes.func.isRequired,
  syncItems: PropTypes.func.isRequired,  
  state: PropTypes.shape({
    shelves: PropTypes.arrayOf(PropTypes.object),
    items: PropTypes.arrayOf(PropTypes.object),
    stores: PropTypes.arrayOf(PropTypes.object),
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
