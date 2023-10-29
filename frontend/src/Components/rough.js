import React, { useState, useEffect } from "react"
import { Link, Outlet } from "react-router-dom";

export default function Menu() {
    return (
        <>
            <div id="whiteOverlay"></div>
            <div id="mainContainer" className="flex fcol">
                <div id="navContainer" className="flex frow">
                    <Link to="/">Home</Link>
                    <Link to="/candidate">Candidate</Link>
                    <Link to="/recruiter">Recruiter</Link>
                </div>

                <Outlet />

            </div>
        </>
    );
    
}



