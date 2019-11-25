import React from 'react';
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import {BrowserRouter, Link} from "react-router-dom";

const siteNavigation = () => {
    return (
        <Navbar variant="dark" expand="md" bg="dark">
            <Navbar.Brand href="#">FoodTrack</Navbar.Brand>
            <Navbar.Toggle/>
            <Navbar.Collapse>
                <BrowserRouter>
                    <Nav>
                        <NavDropdown id="nav-account" title="Account">
                            <NavDropdown.Item as={Link} to="/login">Login</NavDropdown.Item>
                            <NavDropdown.Item as={Link} to="/logout">Logout</NavDropdown.Item>
                            <NavDropdown.Item as={Link} to="/password">Change Password</NavDropdown.Item>
                        </NavDropdown>
                        <NavDropdown id="nav-purchase" title="Purchase">
                            <NavDropdown.Item>New</NavDropdown.Item>
                            <NavDropdown.Item>List</NavDropdown.Item>
                            <NavDropdown.Item>Summary</NavDropdown.Item>
                        </NavDropdown>
                        <NavDropdown id="nav-foodlog" title="Food Log">
                            <NavDropdown.Item>New Entry</NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                </BrowserRouter>
            </Navbar.Collapse>
        </Navbar>
    );
};

export default siteNavigation;