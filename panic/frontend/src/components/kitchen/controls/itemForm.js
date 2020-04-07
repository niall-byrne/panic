import React from "react";
import PropTypes from 'prop-types';

function locationSelector(props) {
  const {refs, items} = props
  const {locationSelectionRef} = refs
  const options = items.map((d) => (
    <option key={d.id} value={d.name}>{d.name}</option>
  ))
  return (
    <select ref={locationSelectionRef} value="">
      {options}
    </select>
  )
}

function itemForm(props) {
  const {submit, refs} = props
  const {inputRef, formRef} = refs
  return (
    <div className="component">
      <div>
        <form ref={formRef} className="" onSubmit={submit}>
          <input type="text" ref={inputRef} placeholder={init} required />
          <input type="text" ref={inputRef} placeholder={init} required />
          <button type="button" onClick={submit}>{text}</button>
        </form>  
      </div>
    </div> 
  );
}

locationSelector.propTypes = {
  refs: PropTypes.shape({
    locationSelectionRef: PropTypes.any.isRequired,
  }).isRequired,  
  items: PropTypes.arrayOf(PropTypes.object)
}

locationSelector.defaultProps = {
  items: []
}

itemForm.propTypes = {
  refs: PropTypes.shape({
    inputRef: PropTypes.any.isRequired,
    formRef: PropTypes.any.isRequired,
  }).isRequired,  
  text: PropTypes.string.isRequired,
  submit: PropTypes.func.isRequired,
  init: PropTypes.string.isRequired
};

export default itemForm;
