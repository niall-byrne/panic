import React from "react";
import PropTypes from 'prop-types';
import FacebookAuth from "./facebook";
import GoogleAuth from "./google";

export const Login = (props) => {
  const {save} = props
  return (     
    <div className="login">
      <GoogleAuth save={save} />
      <FacebookAuth save={save} />
    </div>
  );
}

Login.propTypes = {
  save: PropTypes.func.isRequired,
};


export default Login;


