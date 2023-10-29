import React, { useState, useEffect } from "react"
import { useNavigate } from "react-router";
import "../BaN.css"
import WestIcon from '@mui/icons-material/West';


export default function Candidate() {

    return (
        <>
            <div id="mainContainer2" className="flex frow">
                {/* <p>wow</p> */}

                <Questions />
            </div>
        </>
    )
}

const questionsArray = [
    "I accept people the way they are.",
    "My moods change easily.",
    "I start arguments just for the fun of it.",
    "I change my plans frequently.",
    "I am Systematic"

]

const writtenQuestions = [
    "If you see a person in a wheelchair struggling to cross the road, but you are also almost running late to your interview. Would you help the person cross the road at the risk of missing your interview?"

]

const questionsLength = questionsArray.length;
const writtenQuestionLength = writtenQuestions.length
const initialResults = Array(questionsLength).fill(-1);
const initialLongResults = Array(writtenQuestionLength).fill(-1);


const initialSocialProfiles = [
    { social: "linkedin", profile: "" },
    { social: "facebook", profile: "" },
    { social: "Github", profile: "" },
    { social: "", profile: ""}
]

function Questions() {
    const [results, setResults] = useState(initialResults);
    const [inputs, setInputs] = useState(initialSocialProfiles);
    const [longResults, setLongResults] = useState(initialLongResults)
    const [name, setName] = useState('')

    const navigate = useNavigate();

    const handleSelection = (e, index, newValue) => {
        const updatedResults = results.map((value, i) => {
            // console.log(i, index, value, newValue)
          if (i === index) {
            return newValue;
          } else {
            return value;
          }
        });

        setResults(updatedResults)
    }

    const handleChange = (e) => {
        // console.log("CHANGED")
    }

    const handleFormChange = (e, index) => {

        // console.log("EEE", e.target.value)
        let data = [...inputs]
        data[index].profile = e.target.value
        setInputs(data)
        // console.log("WTF", data, inputs)
    }

    const handleLongFormChange = (e, index) => {
        let data = [...longResults]
        data[index] = e.target.value
        setLongResults(data)
    }

    const addField = () => {
        let socialMediaThreshold = 7;
        if (inputs.length >= socialMediaThreshold) {
            console.log("Too many social medias")
            return
        }
        let nextField = { social: "", profile: "" }
        setInputs([...inputs, nextField])
    }

    const removeField = (index) => {
        let data = [...inputs];
        data.splice(index, 1)
        setInputs(data)
    }

    const onSubmit = (e) => {
        e.preventDefault()
        console.log("hi")
        console.log(results)
        var notCompletedFlag = 0;
        for (var i = 0; i < results.length; i++) {
            if (results[i] === -1) {
                notCompletedFlag = 1;
                break;
            }
        }

        if (!notCompletedFlag) {
            console.log("RESULTS", results)
            // console.log(notCompletedFlag)
            // console.log("DONEODNONEOND")
            console.log("Long Results", longResults)

            // console.log("THE THINGS", inputs[0], inputs[0]["profile"])
            // console.log("THE THINGS2", inputs[1], inputs[1]["profile"])
            console.log("name", name)
            localStorage.setItem("name", name)

            const jsonbody = {
                "linkedin": inputs[0].profile,
                "facebook": inputs[1].profile,
                "answers_mcq": results, 
                "answers": longResults, 

            }

            fetch("http://10.2.130.139:5000/candidate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(jsonbody)
            })
                .then(
                    (res) => {
                        if (res.ok) {
                            res.json()
                                .then((body) => {
                                    localStorage.setItem("popularity", body["popularity_score"])
                                    localStorage.setItem("sentiment", body["sentiment_value"])
                                    localStorage.setItem("truthfulness", body["truthfulness"])
                                    localStorage.setItem("professions", body["professions"])
                                    localStorage.setItem("about", body["about"])
                                    localStorage.setItem("result", body["result"])
                                    // localStorage.setItem("name", name)
                                    localStorage.setItem("mcq", body["answers_mcq"])
                                    console.log(res, body)
                                });
                        }
                        else {
                            res.json()
                                .then((body) => {
                                    let errMsg = body.message;
                                    console.log(errMsg);
                                });
                        }
                    }
                )

            // navigate("/formsubmit")

        }
    }

    const onClick = () => {
        navigate("/")
    }

    const handleNameFormChange = (e) => {
        setName(e.target.value)
    }

    return (

        <>
            {/* <div className="noise"></div> */}
        <button className="backArrow flex" onClick={onClick} style={{left: "30vw"}}><WestIcon /></button>

        <div className="flex fcol mainContainer4">
            <div className="noise"></div>
            <form onSubmit={onSubmit} className="form1">
                <div id="getProfiles">
                    <div className="question flex section" style={{margin: "10px", marginTop: "40px"}}>
                        Section 1: Please Enter your name and your social media profiles:
                        </div>
                        
                    <div className="question flex">
                        Enter your name
                        </div>
                        
                    <input
                        type="text"
                        name='name'
                        placeholder='Enter your name here'
                        // defaultValue={input.}
                        onChange={e => handleNameFormChange(e)}
                    />
                    {inputs.map((input, index) => {
                        return (
                        <div key={index}>
                            <input
                                type="text"
                                name='social'
                                placeholder='social media'
                                defaultValue={input.social}
                                onChange={e => handleFormChange(e, index)}
                            />
                            <input
                                type="text"
                                name='profile'
                                placeholder='profile link'
                                defaultValue={input.profile}
                                onChange={e => handleFormChange(e, index)}
                                required={index === 0}
                                />

                                {index != 0 && <button className="formButton1" onClick={() => removeField(index)}>Remove</button>}
                        </div>
                        )
                    })}
                    <button onClick={addField} className="formButton1 formButton2">
                        Add Another
                    </button>
                </div>

                <div className="pageTitle">
                    Candidate Form
                </div>
                <div className="horizontalDivider"></div>
                <div className="question flex section" style={{marginTop: "20px", marginBottom: "10px"}}>
                    Section 2: Please fill out the following psychometric evaluation: (1 - Least True, 5 - Most True)
                </div>

                <div id="mainContainer3" className="flex2 fcol">


                    {questionsArray.map((question, index) => {
                        return (
                            <div key={index}>
                                <div className="question flex">
                                    {index + 1}. {question}
                                </div>

                                <div className="radioContainer flex frow">
                                    <input type="radio" checked={results[index] === 1} onChange={handleChange} onClick={(e) => handleSelection(e, index, 1)} value="1" /> 1
                                    <input type="radio" checked={results[index] === 2} onChange={handleChange} onClick={(e) => handleSelection(e, index, 2)} value="2" /> 2
                                    <input type="radio" checked={results[index] === 3} onChange={handleChange} onClick={(e) => handleSelection(e, index, 3)} value="3" /> 3
                                    <input type="radio" checked={results[index] === 4} onChange={handleChange} onClick={(e) => handleSelection(e, index, 4)} value="4" /> 4
                                    <input type="radio" checked={results[index] === 5} onChange={handleChange} onClick={(e) => handleSelection(e, index, 5)} value="5" /> 5
                                </div>

                            </div>
                        )
                    })}
                    <div className="horizontalDivider" style={{marginTop: "20px", marginLeft: "20px"}}></div>
                    <div className="question flex fcol section" style={{marginTop: "20px", marginBottom: "20px"}}>
                        
                        Section 3: Please answer the following puzzles:
                        </div>
                        
                    {writtenQuestions.map((question, index) => {
                        return (
                            <div key={index} className="flex fcol">
                                <div className="question flex longAnswerQuestion">
                                    {index + 1}. {question}
                                </div>

                                <input className="longAnswer"
                                    type="text"
                                    name="value"
                                    placeholder="Long Answer"
                                    onChange={e => handleLongFormChange(e, index)}
                                >
                                
                                </input>

                            </div>
                        )
                    })}



                    <input type="submit" onSubmit={onSubmit}></input>
                </div>
            </form>
            </div>
    </>
    )


}