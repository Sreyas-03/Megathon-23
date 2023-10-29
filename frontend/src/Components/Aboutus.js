import React, { useState, useEffect } from "react"
import Fade from "react-reveal/Fade"
import { Link } from "react-router-dom"
import WestIcon from '@mui/icons-material/West';
import { useNavigate } from "react-router";


export default function Aboutus() {
    const navigate = useNavigate();
    const onClick = () => {
        navigate("/")
    }
    return (
        <>
            <button className="backArrow flex" onClick={onClick}><WestIcon /></button>

            <div id="mainContainer" className="flex fcol">
                <div className="line line1 flex"><Fade big cascade>About Us</Fade></div>
                <div className="subtitle subtitle2 flex">
                    <Fade big cascade>
                        This Project was created during the Megathon Hackathon 2023
                        for Prompt 3 under KonnectNXT. The problem statement was to
                        use psychometric tests & behavioral analysis to help further
                        narrow down candidate selection during employment/recruitment.
                        In this way, the lives of the recruiter becomes much simpler
                        and they get a more whole view of the candidate field.
                    </Fade></div>
            </div>
        </>
    )
}