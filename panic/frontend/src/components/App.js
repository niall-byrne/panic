import React, { Component } from "react";
import { render } from "react-dom";
import FacebookAuth from "./oauth/facebook.js";
import GoogleAuth from "./oauth/google";

class App extends Component {
  constructor() {
    super();
    this.state = { isAuthenticated: false, user: null, token: "" };
    this.storeLogin = this.storeLogin.bind(this);
    this.logout = this.logout.bind(this);
  }

  logout() {
    this.setState({ isAuthenticated: false, token: "", user: null });
  }

  storeLogin(profile, token) {
    this.setState({
      isAuthenticated: true,
      token: token,
      user: profile
    });
  }

  render() {
    let content = this.state.isAuthenticated ? (
      <div>
        <p>Authenticated</p>
        <div>{this.state.user.email}</div>
        <div>Log Out Button WIP</div>
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
