const initialAuthState = {
    token: null,
    user: null,
};

export const AUTH_LOGIN = "AUTH_LOGIN";
export const authLoginAction = (user, token) => {
    return {
        type: AUTH_LOGIN,
        user: user,
        token: token
    }
};

export const AUTH_LOGOUT = "AUTH_LOGOUT";
export const authLogoutAction = () => {
    return {
        type: AUTH_LOGOUT,
    }
};


export const authenticationReducer = (state = initialAuthState, action) => {
    switch (action.type) {
        case AUTH_LOGIN:
            return {
                ...state,
                user: action.user,
                token: action.token,
            };
        case AUTH_LOGOUT:
            return {
                ...state,
                user: null,
                token: null
            };
        default:
            return state;
    }
};