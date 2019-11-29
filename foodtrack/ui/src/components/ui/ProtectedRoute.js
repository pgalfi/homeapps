import React from "react";
import {Redirect, Route} from "react-router-dom";
import {connect} from "react-redux";
import {UI} from "../../config";

const protectedRoute = (props) => {
    if (props.isAuth) return <Route path={props.path} exact component={props.component}/>;
    else return <Redirect to={UI.AUTH_LOGIN}/>;
};

const mapStateToProps = (state) => {
    return {
        isAuth: state.auth.token !== null
    }
};

export default connect(mapStateToProps)(protectedRoute);