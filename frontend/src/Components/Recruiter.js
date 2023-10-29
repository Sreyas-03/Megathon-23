import React, { useState, useEffect } from "react"
import pfp from "../assets/banana.jpg"
import mask from "../assets/oval.svg"
import WestIcon from '@mui/icons-material/West';
import Link, { useNavigate } from "react-router-dom"
import Aboutus from './Aboutus';

const data = { // Dummy data
    "name": "Shreyas R. Palley",
    "currentRole": "Frontend Developer",
    "currentCompany/University": "IIIT Hyderabad",
    "about": "I am a UG3 Student studying CSE",
    "email": "shreyas.palley@students.iiit.ac.in",
    "skills": "Rubix Cubing, Beatboxing",
    "education": "Studied in IIIT Hyderabad"
}

export default function Recruiter() {

    const big5 = ["Openness", "Conscientiousness", "Extraversion", "Agreeable", "Neuroticism"];

    const navigate = useNavigate();

    const [popularity, setPopularity] = useState(0)
    const [sentiment, setSentiment] = useState(0)
    const [truthfulness, setTruthfulness] = useState(0)
    const [aboutus, setAboutus] = useState('')
    const [result, setResult] = useState('')
    const [professions, setProfessions] = useState([])
    const [name, setName] = useState('')
    const [mcq, setMcq] = useState([])

    const onClick = () => {
        navigate("/")
    }

    useEffect(() => {

        const popularity1 = localStorage.getItem("popularity")
        const sentiment1 = localStorage.getItem("sentiment")
        const truthfulness1 = localStorage.getItem("truthfulness")
        const result1 = localStorage.getItem("result")
        const professions1 = localStorage.getItem("professions")
        const name1 = localStorage.getItem("name")
        const mcq1 = localStorage.getItem("mcq")

        const mcq2 = mcq1.split(',')
        const about1 = localStorage.getItem("about")
        // const aboutus1 = about1.join(' ')
        
        setPopularity(popularity1)
        setSentiment(sentiment1)
        setTruthfulness(truthfulness1)
        setAboutus(about1)
        setResult(result1)
        setProfessions(professions1)
        setName(name1)
        setMcq(mcq2)

        // console.log("TEST", popularity, sentiment, aboutus, result)
        console.log("MCQ", mcq2)

    }, [])

    return (
        <>
            <button className="backArrow flex" onClick={onClick}><WestIcon /></button>
            <div id="mainContainer" className="flex fcol mainContainer4" style={{height: "70%"}}>

                <div id="mainContainer2" className="flex fcol">
                    <div className="pageTitle">
                        Recruiter Display
                    </div>

                    <div id="mainContainer3" className="flex frow short" style={{height: "80%"}}>
                        <div className="rLeft flex rClass pad fcol">
                            <div className="heading">About Us</div> <br></br>
                            {aboutus} <br></br> <br></br> <br></br> 
                            <div className="heading">Result</div> <br></br>
                            {result} <br></br> <br></br> <br></br>
                            <div className="heading">Top 5 Predicted Professions</div> <br></br>
                            {professions} <br></br> <br></br>
                            <div className="heading">Big 5</div> <br></br>
                            {big5[0]}:{mcq[0]},  {big5[1]}:{mcq[1]},  {big5[2]}:{mcq[2]},  {big5[3]}:{mcq[3]},  {big5[4]}:{mcq[4]},  <br></br>

                        </div>
                        <div className="rRight flex pad fcol rClass">
                            <div className="heading">Popularity</div> <br></br>
                            {popularity} <br></br> <br></br> <br></br>
                            <div className="heading">Sentiment</div> <br></br>
                            {sentiment} <br></br> <br></br> <br></br>
                            <div className="heading">Truthfulness</div> <br></br>
                            {truthfulness} <br></br>    
                            
                            
                        </div>
                    </div>
                    <div className="flex fcol personalMiddle">
                        <img id="pfp" src={pfp}></img>
                        <div className="name">{name}
</div>
                    </div>
                </div>
            </div>
        </>
    )
}