function filterStores(state, name) {
  return state.filter(store => store.name !== name)
}

function stores(state = [], action) {

  const mockNewStore = {id: (999 + state.length), name: action.name}

  switch(action.type) {
    case "FETCH_STORES":      
      return [...action.stores]
    case "ADD_STORE":    
      // API CALL NEEDED HERE
      return [
        ...state,
        {...mockNewStore}
      ]
    case "DEL_STORE":    
      // API CALL NEEDED HERE
      return filterStores(state, action.name)
    default:
      return state;
  }
}

export default stores;
