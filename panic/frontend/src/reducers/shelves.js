function filterShelves(state, name) {
  return state.filter(shelf => shelf.name !== name)
}

function shelves(state = [], action) {

  const mockNewShelf = {id: action.name, name: action.name}

  switch(action.type) {
    case "FETCH_SHELVES":      
      return [...action.shelves]
    case "ADD_SHELF":    
      // API CALL NEEDED HERE
      return [
        ...state,
        {...mockNewShelf}
      ]
    case "DEL_SHELF":    
      // API CALL NEEDED HERE
      return filterShelves(state, action.name)
    default:
      return state;
  }
}

export default shelves;
