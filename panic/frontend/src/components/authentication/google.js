import React, { Component } from 'react';
import { GoogleLogin } from 'react-google-login';
import PropTypes from 'prop-types';
import { post } from '../../util/requests'

class GoogleAuth extends Component {
    constructor(props) {
      super(props);
      this.googleAuthenticate = this.googleAuthenticate.bind(this);
    }

  googleAuthenticate(authentication) {
    // eslint-disable-next-line no-console
    console.debug(authentication);
    
    // Setup Request
    const { save } = this.props;
    const data = {
      access_token: authentication.tokenObj.access_token,
      code: authentication.tokenObj.login_hint,
    }
    const token = null;    
    const path = '/api/v1/auth/social/google/'
  
    post(path, token, data)
    .then((response) => {
      const [socialLoginResponse, statusCode] = response;
      if ( statusCode!== 200 ) {        
          throw new Error(`Login: ${statusCode} - ${JSON.stringify(socialLoginResponse)}`);
      }
      // eslint-disable-next-line no-console
      console.debug(socialLoginResponse);
      const profileObj = {
        name: authentication.profileObj.name,
        email: authentication.profileObj.email
      };
      save(profileObj, socialLoginResponse.key);
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
