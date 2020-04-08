function filterItems(state, name) {
  return state.filter((item) => item.name !== name);
}

function items(state = [], action) {
  const mockId = 999 + state.length;

  switch (action.type) {
    case 'FETCH_ITEMS':
      return [...action.items];
    case 'ADD_ITEM':
      // API CALL NEEDED HERE
      return [{ ...action.item, id: mockId }, ...state];
    case 'DEL_ITEM':
      // API CALL NEEDED HERE
      return filterItems(state, action.name);
    default:
      return state;
  }
}

export default items;
