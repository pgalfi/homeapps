// DEPENDENCIES
import React from 'react';
import {Provider} from "react-redux";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
// STYLING
import './App.css';
// APP STATE AND CONFIGURATION
import AppDataStore from "./store/stores";
import {BASE_URL, UI} from "./config";
// COMPONENTS
import SiteNavigation from "./components/ui/Navigation";
import LoginForm from "./components/auth/LoginForm";
import Logout from "./components/auth/Logout";
import ChangePasswordForm from "./components/auth/ChangePasswordForm";
import ProtectedRoute from "./components/ui/ProtectedRoute";

const app = () => {
  return (
      <Provider store={AppDataStore}>
          <Router basename={BASE_URL}>
              <SiteNavigation />
              <Switch>
                  <Route path={UI.AUTH_LOGIN} component={LoginForm} />
                  <ProtectedRoute path={UI.AUTH_LOGOUT} exact component={Logout} />
                  <ProtectedRoute path={UI.AUTH_PASSWORD} exact component={ChangePasswordForm} />
              </Switch>
          </Router>
      </Provider>
  );
};

export default app; 
