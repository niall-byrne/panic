import React, { Component } from "react";
import Login from "./authentication/login"

// eslint-disable-next-line react/prefer-stateless-function
class Splash extends Component {
  
  render() {
    const {state, login} = this.props
    const {auth} = state
    const content = auth.isAuthenticated ? (
      <div>
        <p>Authenticated</p>
        <div>{this.profile.email}</div>
      </div>
    ) : (
      <div>
        <Login save={login} />
      </div>
    );
    return <div className="Splash">{content}</div>;
  }
}

export default Splash;
