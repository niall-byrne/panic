import React from "react";
import PropTypes from 'prop-types';

function RemovableRow(props) {
  const {row, controlFn, controlName} = props
  const {id, name} = row
  return (
    <li key={name} className="component">
      {`${id} - ${name} -> `}
      <button onClick={() => controlFn(row)} type="button">
        {controlName}
      </button>
    </li> 
  );
}

RemovableRow.propTypes = {
  row: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
  }).isRequired,  
  controlName: PropTypes.string.isRequired,
  controlFn: PropTypes.func.isRequired
};

export default RemovableRow;
