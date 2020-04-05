function auth(state = {}, action) {
    const {type, profile, token} = action
    switch(type) {
    case "LOGIN":      
      return {        
          isAuthenticated: true, 
          profile: {...profile}, 
          token
        }
    case "LOGOUT":      
      return {        
        isAuthenticated: false, 
        profile: {}, 
        token: null
      }
    default:
      return state;
  }
}

export default auth;
