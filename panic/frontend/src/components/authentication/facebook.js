import React, { Component } from "react";
import FacebookLogin from "react-facebook-login";
import PropTypes from "prop-types";
import { post } from '../../util/requests'

class FacebookAuth extends Component {
  constructor(props) {
    super(props);
    this.facebookAuthenticate = this.facebookAuthenticate.bind(this);
  }

  facebookAuthenticate(authentication) {
    // eslint-disable-next-line no-console
    console.debug(authentication);
    
    // Setup Request
    const { save } = this.props;
    const data = {
      access_token: authentication.accessToken,
      code: authentication.userID,
    }
    const token = null;    
    const path = '/api/v1/auth/social/facebook/'
  
    post(path, token, data)
    .then(response => {
      const [socialLoginResponse, statusCode] = response;
      if ( statusCode!== 200 ) {        
        throw new Error(`Login: ${statusCode} - ${JSON.stringify(socialLoginResponse)}`);
      }
      // eslint-disable-next-line no-console
      console.debug(socialLoginResponse);
      const profileObj = {
        name: authentication.name,
        email: authentication.email
      };
      save(profileObj, socialLoginResponse.key);
    })
    .catch(err => {
      // eslint-disable-next-line no-console
      console.debug(err);
    });
  }

  render() {
    return (
      <div>
        <FacebookLogin
          appId={process.env.FACEBOOK_APP_ID}
          autoLoad={false}
          cookie={false}
          textButton="Facebook"
          fields="name,email,picture"
          callback={this.facebookAuthenticate}
        />
      </div>
    );
  }
}

FacebookAuth.propTypes = {
  save: PropTypes.func.isRequired
};

export default FacebookAuth;
