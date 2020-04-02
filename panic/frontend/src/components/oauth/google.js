'use strict';

import React, { Component } from 'react';
import { GoogleLogin } from 'react-google-login';

class GoogleAuth extends Component {
    constructor(props) {
      super(props);
      this.googleAuthenticate = this.googleAuthenticate.bind(this);
    }

  googleAuthenticate(response) {
    console.log(response);
    fetch(`${process.env.BASE_URL}/api/v1/auth/social/google/`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        access_token: response['tokenObj']['access_token'],
        code: response['tokenObj']['login_hint'],
      })
    }).then(response => {
        return response.json();
      })
      .then(data => {
        this.props.save(response['profileObj'], data['key']);
      })
      .catch(err => {
        console.log(err);
      })
  };

  render() {
    return (
        <div>
          <GoogleLogin
            clientId={process.env.GOOGLE_CLIENT_ID}
            buttonText="Login"
            onSuccess={this.googleAuthenticate}
            onFailure={this.googleAuthenticate}
          />
        </div>
    )
  }
}

export default GoogleAuth;
