import React, { useState } from 'react';
import jwtDecode from 'jwt-decode';

export const UserContext = React.createContext({
  token: undefined,
  setToken: () => {},
  logout: () => {},
});

const TOKEN_KEY = 'auth-token';
const token = localStorage.getItem(TOKEN_KEY);

export const UserContextConsumer = UserContext.Consumer;
export const UserContextProvider = ({ children }) => {
  const [stateToken, setToken] = useState(token);

  const saveToken = (token) => {
    localStorage.setItem(TOKEN_KEY, token);
    setToken(token);
  };

  const logout = async () => {
    localStorage.removeItem(TOKEN_KEY);
    setToken('');
  };

  const decodedToken = stateToken ? jwtDecode(stateToken) : {};

  return (
    <UserContext.Provider
      value={{
        token: stateToken || '',
        setToken: saveToken,
        logout,
        user: decodedToken,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};
