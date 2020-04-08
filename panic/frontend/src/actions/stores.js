// syncrhonize from api
export function syncStores(stores) {
  return {
    type: 'FETCH_STORES',
    stores,
  };
}

// add
export function addStore(name) {
  return {
    type: 'ADD_STORE',
    name,
  };
}

// remove
export function delStore(storeId, name) {
  return {
    type: 'DEL_STORE',
    storeId,
    name,
  };
}
