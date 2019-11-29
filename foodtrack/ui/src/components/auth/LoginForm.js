import "./Authentications.css";
import React, {Component} from 'react';
import {connect} from "react-redux";
import {Alert, Button, Container, Form, Row} from "react-bootstrap";
import {Redirect, withRouter} from "react-router-dom";

import {authLoginAction} from "../../store/states/auth-state";
import {authenticate} from "../../backend/api";
import {BASE_URL} from "../../config";


class LoginForm extends Component {

    state = {
        user: null,
        pass: null,
        success: false,
        errorMsg: null,
        errorData: null
    };

    userNameChange = event => this.setState({user: event.target.value});
    passWordChange = event => this.setState({pass: event.target.value});
    submitForm = event => {
        event.preventDefault();
        event.stopPropagation();
        const form = event.currentTarget;
        if (form.checkValidity() === true) {
            authenticate(this.state.user, this.state.pass).then(
                response => {
                    this.props.loginSuccess(this.state.user, response.data.token);
                    this.setState({success: true, errorMsg: null, errorData: null,})
                }
            ).catch(
                error => {
                    this.setState({success: false, errorMsg: error.message,
                        errorData: error.response ? error.response.data : null});
                }
            );
        }
    };

    render() {
        if (this.state.success) return <Redirect to={BASE_URL} />;

        let errorMessage = this.state.errorMessage;
        if (this.state.errorData && this.state.errorData["non_field_errors"]) {
            errorMessage = this.state.errorData["non_field_errors"];
        }
        return (
            <Container>
                <Row className={"justify-content-center"}>
                    <div className={"auth-dialog bg-light mt-5 p-4"}>
                        <Form onSubmit={this.submitForm}>
                            { errorMessage ? <Alert variant={"danger"}>{errorMessage}</Alert> : null}
                            <h4>Authentication Required</h4>
                            <Form.Group controlId="authForm.user">
                                <Form.Label column={false}>Username:</Form.Label>
                                <Form.Control required type="text" onChange={this.userNameChange}/>
                            </Form.Group>
                            <Form.Group controlId="authForm.pass">
                                <Form.Label column={false}>Password:</Form.Label>
                                <Form.Control required type="password" onChange={this.passWordChange}/>
                            </Form.Group>
                            <Button variant="primary" type={"submit"} block={true}>Login</Button>
                        </Form>
                    </div>
                </Row>
            </Container>
        );
    }
}

const mapDispatchToProps = dispatch => {
    return {
        loginSuccess: (user, token) => {
            dispatch(authLoginAction(user, token));
        }
    }
};

export default connect(null, mapDispatchToProps)(withRouter(LoginForm))