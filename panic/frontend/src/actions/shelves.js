// syncrhonize from api
export function syncShelves(name) {
  return {
    type: 'FETCH_SHELVES',
    name
  }
}

// add
export function addShelf(name) {
  return {
    type: 'ADD_SHELF',
    name
  }
}

// remove
export function delShelf(shelfId, name) {
  return {
    type: 'DEL_SHELF',
    shelfId,
    name,
  }
}
