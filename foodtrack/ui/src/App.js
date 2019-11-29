import React from 'react';
import './App.css';
import SiteNavigation from "./components/ui/Navigation";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import LoginForm from "./components/auth/LoginForm";
import {Provider} from "react-redux";
import AppDataStore from "./store/stores";
import {BASE_URL, UI} from "./config";
import Logout from "./components/auth/Logout";

const app = () => {
  return (
      <Provider store={AppDataStore}>
          <Router basename={BASE_URL}>
              <SiteNavigation />
              <Switch>
                  <Route path={UI.AUTH_LOGIN} exact component={LoginForm} />
                  <Route path={UI.AUTH_LOGOUT} exact component={Logout} />
              </Switch>
          </Router>
      </Provider>
  );
};

export default app; 
