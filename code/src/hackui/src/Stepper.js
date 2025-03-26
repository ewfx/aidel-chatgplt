import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faHourglassHalf } from "@fortawesome/free-solid-svg-icons";
import './App.css'
import StepperComponent from "./StepStatus";

const steps = [
    "Step 1: Fetching FATF Black & Grey List...",
    "Step 2: Fetching Corruption scores from Transparency International...",
    "Step 3: Fetching Basel AML scores ...",
    "Step 4: Processing Transaction details...",
    "Step 5: Checking if Politically Exposed persons are involved...",
    "Step 6: Checking if the entities are part of sanction lists...",
    "Step 7: Calculating the risk score..."
];

const FancyStepper = () => {
    const [currentStep, setCurrentStep] = useState(0);
    const navigate = useNavigate()

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentStep((prev) => {
                if (prev < steps.length - 1) {
                    return prev + 1;
                } else {
                    navigate("/risk-analysis");
                    return prev;
                }
            });
        }, 1000);

        return () => clearInterval(interval);
    }, [navigate]);

    return (
        <>
            <div className="App stepss">
                <header className="header">
                    <img src={`/header.png`} alt="Header" className="header-image" />
                </header>
                <div className='main-body'>
                    <div className="header-content" style={{ marginBottom: "35px" }}>
                        <h1 style={{ marginTop: "15px" }}>Executing...</h1>
                        <p>
                            Automated entity extraction, classification, and risk scoring to empower
                            smarter financial decisions.
                        </p>
                    </div>
                    <StepperComponent />
                    <div className="flex flex-col items-center justify-center h-screen bg-gray-100" style={{ marginTop: "30px" }}>
                        <div className="stepper">
                            {steps.map((stepText, index) => (
                                <div key={index} className="step-container">
                                    {index !== 0 && (
                                        <div className={`line ${index <= currentStep ? "active-line" : ""}`}></div>
                                    )}

                                    <div
                                        className={`step ${index === currentStep ? "active" : ""} ${index < currentStep ? "completed" : ""
                                            }`}
                                    >
                                        <div className="circle-wrapper">
                                            <div className="outer-circle">
                                                <div className="inner-circle">
                                                    {index < currentStep ? (
                                                        <FontAwesomeIcon icon={faCheck} size="md" />
                                                    ) : (
                                                        <FontAwesomeIcon icon={faHourglassHalf} size="md" />
                                                    )}
                                                </div>
                                            </div>
                                        </div>

                                        <div className="content">{stepText}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default FancyStepper;
