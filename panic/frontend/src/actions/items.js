// synchronize from api
export function syncItems(items) {
  return {
    type: 'FETCH_ITEMS',
    items
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
