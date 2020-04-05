// synchronize from api
export function syncItems(name) {
  return {
    type: 'FETCH_ITEMS',
    name
  }
}

// add
export function addItem(name) {
  return {
    type: 'ADD_ITEM',
    name
  }
}

// remove
export function delItem(itemID, name) {
  return {
    type: 'DEL_ITEM',
    itemID,
    name,
  }
}
