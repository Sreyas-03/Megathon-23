import React, { useState, useEffect } from "react"
import Fade from "react-reveal/Fade"
import TurnLeftIcon from '@mui/icons-material/TurnLeft';
// import TurnRightIcon from '@mui/icons-material/TurnRight';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import { useNavigate } from "react-router";

export default function Home() {

    const navigate = useNavigate();
    return (
        <>
            <div id="mainContainer" className="flex fcol">
                <div className="flex fcol doubleLineContainer">
                    <div className="flex frow lineContainer">
                        <div className="line line1"><Fade big cascade>Needle</Fade></div>
                        <div className="line line2"><Fade big cascade>In A</Fade></div>
                        <div className="yFlip"><Fade big cascade><PlayArrowIcon /></Fade></div>

                    </div>
                    <div className="flex frow lineContainer">
                        <Fade big cascade>
                        <div className="line line3"><Fade big cascade>Haystack</Fade></div>
                            <div className="rotIcon"><TurnLeftIcon /></div>
                            </Fade>
                    </div>
                    <div className="subtitle subtitle1">
                        <Fade big cascade>
                            A Talent <br></br>Identifying <br></br>Powerhouse
                        </Fade>
                    </div>
                </div>
            </div>

            <div id="miniNav" className="flex frow">
                <Fade big cascade>
                <button className="navItem flex" onClick={() => navigate("aboutus")}> About the Tool </button>
                <button className="navItem flex" onClick={() => navigate("candidate")}> Candidate Registration </button>
                <button className="navItem flex" onClick={() => navigate("recruiter")}> Recruiter View </button>
                </Fade>
            </div>

            <Fade big cascade>
                <div className="names name1">Akshat Sanghvi</div>
                <div className="names name2">Vaibhav Agarwal</div>
                <div className="names name3">S Sreyas</div>
                <div className="names name4">Keshav Gupta</div>
                <div className="names name5">Shreyas Reddy Palley</div>
                <div className="names name6">The Bhumireddy Pappireddies</div>
            </Fade>
        </>
    )
}