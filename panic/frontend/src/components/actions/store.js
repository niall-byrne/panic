// add
export function addStore(name) {
  return {
    type: 'ADD_STORE',
    name
  }
}

// remove
export function removeStore(storeId, name) {
  return {
    type: 'ADD_COMMENT',
    storeId,
    name,
  }
}
