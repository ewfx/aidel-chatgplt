import React from "react";
import { Stepper, Step, StepLabel } from "@mui/material";
import { useLocation } from "react-router-dom";

const steps = ["Input", "Processing", "Risk Analysis"];

const StepperComponent = () => {
    const location = useLocation();

    const getStep = () => {
        if (location.pathname === "/input") return 0;
        if (location.pathname === "/stepper") return 1;
        if (location.pathname === "/risk-analysis") return 2;
        return 0; 
    };

    return (
        <Stepper activeStep={getStep()} alternativeLabel >
            {steps.map((label, index) => (
                <Step key={index}>
                    <StepLabel>{label}</StepLabel>
                </Step>
            ))}
        </Stepper>
    );
};

export default StepperComponent;
