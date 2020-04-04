import React, { Component } from "react";
import Authentication from "./oauth/main"
import FacebookAuth from "./oauth/facebook";
import GoogleAuth from "./oauth/google";
import LogoutAuth from "./oauth/logout";
import Shelves from './kitchen/shelves';
import Stores from './kitchen/stores';
import Items from './kitchen/items';

class App extends Component {
  constructor() {
    super();
    this.state = { 
      isAuthenticated: false, 
      profile: null, 
      token: null, 
      shelves: [], 
      stores: [], 
      items: []
    };
    this.clearLogin = this.clearLogin.bind(this);
    this.storeLogin = this.storeLogin.bind(this);
    this.storeShelves = this.storeShelves.bind(this);
    this.storeStores = this.storeStores.bind(this);
    this.storeItems = this.storeItems.bind(this);
  }

  clearLogin() {
    this.setState({ 
      isAuthenticated: false, 
      profile: null, 
      token: null, 
      shelves: [], 
      stores: [], 
      items: []
    });
  }

  storeLogin(profile, token) {
    this.setState({
      isAuthenticated: true,
      token,
      profile
    });
  }

  storeShelves(shelves) {
    this.setState({shelves});
  }

  storeStores(stores) {
    this.setState({stores});
  }

  storeItems(items) {
    this.setState({items});
  }

  render() {
    console.log("here")
    console.log(this.props.store)
    console.log(this.props);
    const {isAuthenticated, token, profile, shelves, stores, items} = this.props
    const content = isAuthenticated ? (
      <div>
        <p>Authenticated</p>
        <div>{profile.email}</div>
        <LogoutAuth token={token} clear={this.clearLogin} />
        <br />
        <Shelves token={token} save={this.storeShelves} shelves={shelves} />
        <Stores token={token} save={this.storeStores} stores={stores} />
        <Items token={token} save={this.storeItems} items={items} />
      </div>
    ) : (
      <div>
        <GoogleAuth save={this.storeLogin} />
        <FacebookAuth save={this.storeLogin} />
      </div>
    );
    return <div className="App">{content}</div>;
  }
}

export default App;
