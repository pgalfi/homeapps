import "./Authentications.css";
import React, {Component} from "react";
import {connect} from "react-redux";
import {Alert, Button, Form, FormGroup} from "react-bootstrap";
import {change_password} from "../../backend/api";

class ChangePasswordForm extends Component {

    state = {
        old: null,
        new1: null,
        new2: null,
        success: false,
        error: {
            msg: null,
            details: false,
            data: {
                old_password: null,
                new_password: null
            }
        }
    };

    checkSame = () => {
        const pass1 = document.getElementById("new_password");
        const pass2 = document.getElementById("passwordForm.new2");
        if (pass1.value === pass2.value) pass2.setCustomValidity("");
        else pass2.setCustomValidity("New password and confirmation password must match!")
    };
    oldPassChange = (event) => this.setState({old: event.target.value});
    new1PassChange = (event) => {
        this.setState({new1: event.target.value});
        this.checkSame();
    };
    new2PassChange = (event) => {
        this.setState({new2: event.target.value});
        this.checkSame();
    };

    submitForm = event => {
        event.preventDefault();
        event.stopPropagation();
        const form = event.currentTarget;
        if (form.checkValidity() === true) {
            change_password(this.props.token, this.state.old, this.state.new1).then(
                response => {
                    this.setState({success: true});
                }
            ).catch(
                error => {
                    this.setState({
                        error: {
                            msg: error.message,
                            details: !!error.response,
                            data: error.response ? error.response.data : null,
                        }
                    });
                }
            )
        }
    };

    render() {
        if (this.state.success) {
            return (
                <div className="row justify-content-center">
                    <div className="auth-dialog bg-light mt-5 p-4">
                        <Alert variant={"success"}>Password has been changed.</Alert>
                    </div>
                </div>
            )
        }
        const error = this.state.error;
        return (
            <div className="row justify-content-center">
                <div className="auth-dialog bg-light mt-5 p-4">
                    <Form onSubmit={this.submitForm}>
                        {!error.details && error.msg ? <Alert variant={"danger"}>{error.msg}</Alert> : null}
                        <h4>Change Password</h4>
                        <FormGroup controlId={"old_password"}>
                            <Form.Label column={false}>Old password:</Form.Label>
                            <Form.Control required type={"password"} onChange={this.oldPassChange}/>
                            {error.data["old_password"] ? <Alert variant={"danger"}>{error.data["old_password"]}</Alert> : null}
                        </FormGroup>
                        <FormGroup controlId={"new_password"}>
                            <Form.Label column={false}>New password:</Form.Label>
                            <Form.Control required type={"password"} onChange={this.new1PassChange}/>
                            {error.data["new_password"] ? <Alert variant={"danger"}>{error.data["new_password"]}</Alert> : null}
                        </FormGroup>
                        <FormGroup controlId={"passwordForm.new2"}>
                            <Form.Label column={false}>Password confirmation:</Form.Label>
                            <Form.Control required type={"password"} onChange={this.new2PassChange}/>
                        </FormGroup>
                        <Button variant="primary" type={"submit"} block={true}>Change Password</Button>
                    </Form>
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        token: state.auth.token
    }
};

export default connect(mapStateToProps)(ChangePasswordForm);