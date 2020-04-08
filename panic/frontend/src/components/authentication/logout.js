import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { post } from '../../util/requests';

class LogoutAuth extends Component {
  constructor(props) {
    super(props);
    this.performLogout = this.performLogout.bind(this);
  }

  performLogout() {
    const { clear } = this.props;
    const data = {};
    const path = '/api/v1/auth/logout/';

    post(path, data)
      .then((response) => {
        const [socialLogoutResponse, statusCode] = response;
        if (statusCode !== 200) {
          throw new Error(
            `Logout: ${statusCode} - ${JSON.stringify(socialLogoutResponse)}`,
          );
        }
        // eslint-disable-next-line no-console
        console.debug(socialLogoutResponse);
        clear();
      })
      .catch((err) => {
        // eslint-disable-next-line no-console
        console.debug(err);
      });
  }

  render() {
    return (
      <div className="section">
        <button type="button" onClick={this.performLogout}>
          Logout
        </button>
      </div>
    );
  }
}

LogoutAuth.propTypes = {
  clear: PropTypes.func.isRequired,
};

export default LogoutAuth;
