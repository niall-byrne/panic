import React from "react";
import PropTypes from 'prop-types';
import FacebookAuth from "./facebook";
import GoogleAuth from "./google";

function LoginAuth(props) {
  const {save} = props
  return (     
    <div className="section">
      <GoogleAuth save={save} />
      <FacebookAuth save={save} />
    </div>
  );
}

LoginAuth.propTypes = {
  save: PropTypes.func.isRequired,
};

export default LoginAuth;
