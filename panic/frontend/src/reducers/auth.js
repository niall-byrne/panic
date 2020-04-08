function auth(state = {}, action) {
  const { type, profile } = action;
  switch (type) {
    case 'LOGIN':
      return {
        isAuthenticated: true,
        profile: { ...profile },
      };
    case 'LOGOUT':
      return {
        isAuthenticated: false,
        profile: {},
      };
    default:
      return state;
  }
}

export default auth;
