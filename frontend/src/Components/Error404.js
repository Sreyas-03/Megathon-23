import React, { useState, useEffect } from "react"
import Fade from "react-reveal/Fade"
import { Link } from "react-router-dom"
import WestIcon from '@mui/icons-material/West';
import { useNavigate } from "react-router";

export default function Error404() {
    const navigate = useNavigate();

    const onClick = () => {
        navigate("/")
    }
    return (
        <>
            <button className="backArrow flex" onClick={onClick}><WestIcon /></button>

            <div id="mainContainer" className="flex fcol">
                <div className="line line1"><Fade big cascade>ERROR 404</Fade></div>
                <div className="subtitle">
                    <Fade big cascade>
                    The page you have requested does not exist.
                        You can return back to the Homepage: <Link to="/">here</Link>
                    </Fade></div>
            </div>
        </>
    )
}