import React, { Component } from "react";
import { render } from "react-dom";
import FacebookAuth from "./oauth/facebook";
import GoogleAuth from "./oauth/google";
import LogoutAuth from "./oauth/logout";
import Shelves from './kitchen/shelves';
import Stores from './kitchen/stores';

class App extends Component {
  constructor() {
    super();
    this.state = { isAuthenticated: false, profile: null, token: null, shelves: [], stores: [] };
    this.clearLogin = this.clearLogin.bind(this);
    this.storeLogin = this.storeLogin.bind(this);
    this.storeShelves = this.storeShelves.bind(this);
    this.storeStores = this.storeStores.bind(this);
  }

  clearLogin() {
    this.setState({ isAuthenticated: false, token: null, profile: null, shelves: [], stores: [] });
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

  render() {
    const {token, profile, shelves, stores, isAuthenticated} = this.state
    const content = isAuthenticated ? (
      <div>
        <p>Authenticated</p>
        <div>{profile.email}</div>
        <LogoutAuth token={token} clear={this.clearLogin} />
        <br />
        <Shelves token={token} save={this.storeShelves} shelves={shelves} />
        <Stores token={token} save={this.storeStores} stores={stores} />
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
const container = document.getElementById("app");
render(<App />, container);
