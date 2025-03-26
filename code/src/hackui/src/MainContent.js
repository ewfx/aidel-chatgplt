import React from 'react';
import './App.css';
import Stats from './Stats';
import KeyFeatures from './KeyFeatures';
import HowItWorks from './HowItWorks';
import RiskFactors from './RiskFactors';
import { useNavigate } from "react-router-dom";

function MainContent() {
    const navigate = useNavigate()

    return (
        <div className="App">
            <header className="header">
                <img src={`/header.png`} alt="Header" className="header-image" />
            </header>

            <div className='main-body'>
                <div style={{ width: "80%" }}>
                    <div style={{ textAlign: "center" }}>
                        <h1 style={{ marginTop: "15px" }}>RiskWise</h1>
                        <p>
                            Automated entity extraction, classification, and risk scoring to empower
                            smarter financial decisions.
                        </p>
                    </div>

                    <div className='cs'>
                        <div className='left-conta'>
                            <KeyFeatures />
                        </div>
                        <div className='right-conta'>
                            <HowItWorks />
                        </div>
                    </div>
                    <Stats />
                    <RiskFactors />

                    <div style={{ textAlign: "center" }}>
                        <button
                            onClick={() => navigate("/input")}
                            className={`input-button active`}
                            style={{ width: "40%", marginTop: "15px", marginLeft: "0", marginBottom: "50px" }}
                        >
                            Get Started
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default MainContent;