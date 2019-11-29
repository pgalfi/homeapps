import React from 'react';
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import {Link, withRouter} from "react-router-dom";
import {connect} from "react-redux";
import {UI} from "../../config";

const navigation = (props) => {
    return (
        <Navbar variant="dark" expand="md" bg="dark">
            <Navbar.Brand href="#">FoodTrack</Navbar.Brand>
            <Navbar.Toggle/>
            <Navbar.Collapse>
                <Nav>
                    {props.isAuthenticated ? (
                        <React.Fragment>
                            <NavDropdown id="nav-account" title="Account">
                                <NavDropdown.Item as={Link} to={UI.AUTH_LOGIN}>Login</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={UI.AUTH_LOGOUT}>Logout</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={UI.AUTH_PASSWORD}>Change Password</NavDropdown.Item>
                            </NavDropdown>
                            <NavDropdown id="nav-purchase" title="Purchase">
                                <NavDropdown.Item as={Link} to={UI.PURCHASE_NEW}>New</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={UI.PURCHASE_LIST}>List</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={UI.PURCHASE_SUMMARY}>Summary</NavDropdown.Item>
                            </NavDropdown>
                            <NavDropdown id="nav-foodlog" title="Food Diary">
                                <NavDropdown.Item as={Link} to={UI.DIARY_NEW}>New Entry</NavDropdown.Item>
                            </NavDropdown>
                        </React.Fragment>
                    ) : (
                        <Nav.Item>
                            <Nav.Link as={Link} to={UI.AUTH_LOGIN}>Login</Nav.Link>
                        </Nav.Item>
                    )}
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
};

const mapStateToProps = state => {
    return {
        isAuthenticated: !!state.auth.token
    }
};

export default connect(mapStateToProps)(withRouter(navigation));