// login
export function login(name) {
  return {
    type: 'LOGIN',
    name
  }
}

// logout
export function logout(name) {
  return {
    type: 'LOGOUT',
    name
  }
}
