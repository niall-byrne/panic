import React, { Component } from 'react';
import { render } from "react-dom";
import { GoogleLogin, GoogleLogout } from 'react-google-login';

class App extends Component {

    constructor() {
        super();
        this.state = { isAuthenticated: false, user: null, token: ''};
        this.googleResponse = this.googleResponse.bind(this);
        this.logout = this.logout.bind(this);
    }

    logout() {
        this.setState({isAuthenticated: false, token: '', user: null})
    };

    googleResponse(response) {
        fetch('/api/v1/auth/social/google/', {
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
            return response.json()
          })
          .then(data => {
            // console.log(response['profileObj'])
            this.setState({
                isAuthenticated: true,
                token: data['key'],
                user: response['profileObj']
            });
          })
          .catch(err => {
            console.log(err);
          })
    };

    render() {
        let content = this.state.isAuthenticated ?
            (
                <div>
                    <p>Authenticated</p>
                    <div>
                        {this.state.user.email}
                    </div>
                    <div>
                        <GoogleLogout
                          clientId="339118650780-srpsm9hu7kaolv25f7cn5nnvbdcafie6.apps.googleusercontent.coms"
                          buttonText="Logout"
                          onLogoutSuccess={this.logout}
                        />
                    </div>
                </div>
            ) :
            (
                <div>
                    <GoogleLogin
                        clientId="339118650780-srpsm9hu7kaolv25f7cn5nnvbdcafie6.apps.googleusercontent.com"
                        buttonText="Login"
                        onSuccess={this.googleResponse}
                        onFailure={this.googleResponse}
                    />
                </div>
            );
        console.log(content);
        return (
            <div className="App">
                {content}
            </div>
        );
    }
}

export default App;
const container = document.getElementById("app");
render(<App />, container);