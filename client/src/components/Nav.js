import React from "react";
import Navbar from "react-bootstrap/Navbar";
import logo from '../logo.png'

const Nav = () => {
    return (
        <>
            <Navbar className='navbar'>
                <Navbar.Brand href="#home">
                    <img
                        alt="Verbal Seasoning"
                        src={logo}
                        width="30"
                        height="30"
                        className="d-inline-block align-top nav-logo"
                    />
                    <span>Verbal Seasoning</span>
                </Navbar.Brand>
            </Navbar>
        </>
    )
}

export default Nav;
