import React from "react";
import PropTypes from 'prop-types';

function AppendFormRow(props) {
  const {submit, init, text, refs} = props
  const {inputRef, formRef} = refs
  return (
    <li key="form" className="component">
      <div>
        <form ref={formRef} className="" onSubmit={submit}>
          <input type="text" ref={inputRef} placeholder={init} required />
          <button type="button" onClick={submit}>{text}</button>
        </form>  
      </div>
    </li> 
  );
}

AppendFormRow.propTypes = {
  refs: PropTypes.shape({
    inputRef: PropTypes.any.isRequired,
    formRef: PropTypes.any.isRequired,
  }).isRequired,  
  text: PropTypes.string.isRequired,
  submit: PropTypes.func.isRequired,
  init: PropTypes.string.isRequired
};

export default AppendFormRow;
