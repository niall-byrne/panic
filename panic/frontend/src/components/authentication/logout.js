import React, { Component } from 'react';
import PropTypes from 'prop-types';

class LogoutAuth extends Component {
  constructor(props) {
    super(props);
    this.performLogout = this.performLogout.bind(this);
  }

  performLogout() {    
    const { clear, token } = this.props;
    fetch(`${process.env.BASE_URL}/api/v1/auth/logout/`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Authorization': `token ${token}`
      },      
    }).then(logoutResponse => {
        return logoutResponse.json();
      })
      .then(logoutResponseJSON => {
      // eslint-disable-next-line no-console
      console.debug(logoutResponseJSON);
        clear();
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.debug(err);
      })
  };

  render() {
    return (
      <div className="section">
        <button type="button" onClick={this.performLogout}>Logout</button>            
      </div>
    )
  }
}

LogoutAuth.propTypes = {
  clear: PropTypes.func.isRequired,
  token: PropTypes.string.isRequired
};

export default LogoutAuth;
