import {applyMiddleware, combineReducers, compose, createStore} from 'redux';
import thunk from "redux-thunk";
import {authenticationReducer} from "./states/auth-state";

const all_reducers = combineReducers({
    auth: authenticationReducer,
});

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const AppDataStore = createStore(all_reducers, composeEnhancers(applyMiddleware(thunk)));

export default AppDataStore;