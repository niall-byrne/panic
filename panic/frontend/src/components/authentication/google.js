import React, { Component } from 'react';
import { GoogleLogin } from 'react-google-login';
import PropTypes from 'prop-types';

class GoogleAuth extends Component {
    constructor(props) {
      super(props);
      this.googleAuthenticate = this.googleAuthenticate.bind(this);
    }

  googleAuthenticate(response) {
    const { save } = this.props;
    let statusCode = null;
    // eslint-disable-next-line no-console
    console.debug(response);
    fetch(`${process.env.BASE_URL}/api/v1/auth/social/google/`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        access_token: response.tokenObj.access_token,
        code: response.tokenObj.login_hint,
      })
    })
    .then(socialLoginResponse => {
      statusCode = socialLoginResponse.status         
      return socialLoginResponse.json()
    })
    .then(socialLoginResponseJSON => {
      if ( statusCode!== 200 ) {
        throw new Error(`Login: ${JSON.stringify(socialLoginResponseJSON)}`);
      }
      // eslint-disable-next-line no-console
      console.debug(socialLoginResponseJSON);
      const profileObj = {
        name: response.profileObj.name,
        email: response.profileObj.email
      };
      save(profileObj, socialLoginResponseJSON.key);
    })
    .catch(err => {
      // eslint-disable-next-line no-console
      console.debug(err);
    });
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

GoogleAuth.propTypes = {
  save: PropTypes.func.isRequired
};

export default GoogleAuth;
