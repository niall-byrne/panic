import React, { Component } from "react";
import FacebookLogin from "react-facebook-login";
import PropTypes from "prop-types";

class FacebookAuth extends Component {
  constructor(props) {
    super(props);
    this.facebookAuthenticate = this.facebookAuthenticate.bind(this);
  }

  facebookAuthenticate(response) {
    const { save } = this.props;
    let statusCode = null;
    // eslint-disable-next-line no-console
    console.debug(response);
    fetch(`${process.env.BASE_URL}/api/v1/auth/social/facebook/`, {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        access_token: response.accessToken
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
        name: response.name,
        email: response.email
      };
      save(profileObj, socialLoginResponseJSON.key);
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
