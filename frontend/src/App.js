import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import './index.css';
import './BaN.css';
import Fade from "react-reveal/Fade";

import Home from './Components/Home';
import Aboutus from './Components/Aboutus';
import Candidate from './Components/Candidate';
import FormSubmit from './Components/FormSubmit';
import Recruiter from './Components/Recruiter';
import Error404 from './Components/Error404';

function Blobs() {
    return (
        <>
            <div className='noise'></div>
            <Fade big cascade>
                <div id="blobs" className="flex">
                    {/* <div className="blob circle1"></div> */}
                    {/* <div className="blob circle2"></div> */}
                    <div className="blob circle3"></div>
                    <div className="blob circle4"></div>
                    <div className="blob circle5"></div>
                </div>
            </Fade>
        </>
    )
}

function App() {
    return (
        <>
            <Blobs />
            
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="aboutus" element={<Aboutus />} />
                    <Route path="candidate" element={<Candidate />} />
                    <Route path="formsubmit" element={<FormSubmit /> } />
                    <Route path="recruiter" element={<Recruiter />} />
                    <Route path="*" element={<Error404 />} />
                </Routes>
            </BrowserRouter>
            
        </>
    );
}

export default App;
