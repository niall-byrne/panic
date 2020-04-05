// login
export function login(profile, token) {
  return {
    type: 'LOGIN',
    profile,
    token
  }
}

// logout
export function logout(profile, token) {
  return {
    type: 'LOGOUT',
    profile,
    token
  }
}
