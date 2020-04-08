// synchronize from api
export function syncItems(items) {
  return {
    type: 'FETCH_ITEMS',
    items,
  };
}

// add
export function addItem(item) {
  return {
    type: 'ADD_ITEM',
    item,
  };
}

// remove
export function delItem(itemID, name) {
  return {
    type: 'DEL_ITEM',
    itemID,
    name,
  };
}
