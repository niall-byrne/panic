"use strict";

import React, { Component } from "react";
import FacebookLogin from "react-facebook-login";

class FacebookAuth extends Component {
  constructor(props) {
    super(props);
    this.facebookAuthenticate = this.facebookAuthenticate.bind(this);
  }

  facebookAuthenticate(response) {
    console.log(response);
    fetch(`${process.env.BASE_URL}/api/v1/auth/social/facebook/`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        access_token: response["accessToken"]
      })
    })
      .then(response => {
        return response.json();
      })
      .then(data => {
        const profileObj = {
          name: response["name"],
          email: response["email"]
        };
        this.props.save(profileObj, data["key"]);
      })
      .catch(err => {
        console.log(err);
      });
  }

  render() {
    return (
      <div>
        <FacebookLogin
          appId={process.env.FACEBOOK_APP_ID}
          autoLoad={false}
          fields="name,email,picture"
          callback={this.facebookAuthenticate}
        />
      </div>
    );
  }
}

export default FacebookAuth;
