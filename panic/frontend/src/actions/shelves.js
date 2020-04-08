// syncrhonize from api
export function syncShelves(shelves) {
  return {
    type: 'FETCH_SHELVES',
    shelves,
  };
}

// add
export function addShelf(name) {
  return {
    type: 'ADD_SHELF',
    name,
  };
}

// remove
export function delShelf(shelfId, name) {
  return {
    type: 'DEL_SHELF',
    shelfId,
    name,
  };
}
