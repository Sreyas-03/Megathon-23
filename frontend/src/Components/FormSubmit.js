import React, { useState, useEffect } from "react"
import Fade from "react-reveal/Fade"
import { Link } from "react-router-dom"
import WestIcon from '@mui/icons-material/West';
import { useNavigate } from "react-router";

export default function FormSubmit() {
    const navigate = useNavigate();

    const onClick = () => {
        navigate("/")
    }
    return (
        <>
            <button className="backArrow flex" onClick={onClick}><WestIcon /></button>

            <div id="mainContainer" className="flex fcol">
                <div className="line line1 success"><Fade big cascade>Success!</Fade></div>
                <div className="subtitle">
                    <Fade big cascade>
                        Recruiters will be Notified that your registration was successful. You can return to the Homepage: <div style={{ overflow: "hidden" , display: "inline-block"}}><Link to="/">here</Link></div>
                    </Fade></div>
            </div>
        </>
    )
}