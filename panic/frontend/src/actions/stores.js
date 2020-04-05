// syncrhonize from api
export function syncStores(name) {
  return {
    type: 'FETCH_STORES',
    name
  }
}

// add
export function addStore(name) {
  return {
    type: 'ADD_STORE',
    name
  }
}

// remove
export function delStore(storeId, name) {
  return {
    type: 'DEL_STORE',
    storeId,
    name,
  }
}
