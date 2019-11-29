import React from "react";
import {Redirect} from "react-router-dom";
import {connect} from "react-redux";

import {BASE_URL} from "../../config";
import {authLogoutAction} from "../../store/states/auth-state";

const logout = (props) => {
    props.logout();
    return <Redirect to={BASE_URL} />;
};

const mapDispatchToProps = dispatch => {
    return {
        logout: () => {
            dispatch(authLogoutAction());
        }
    }
};

export default connect(null, mapDispatchToProps)(logout)