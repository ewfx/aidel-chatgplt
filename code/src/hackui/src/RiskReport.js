import React, { useState, useRef } from "react";
import GaugeChart from "react-gauge-chart";
import Accordian from "./Accordian";
import StepperComponent from "./StepStatus";
import { useTransactions } from "./TransactionContext";
import html2canvas from "html2canvas";

const RiskReport = () => {
    const { transactions } = useTransactions();
    const [currentIndex, setCurrentIndex] = useState(0);
    const ref = useRef(null);

    const handleNext = () => {
        if (currentIndex < transactions.length - 1) {
            setCurrentIndex(currentIndex + 1);
        }
    };

    const handlePrevious = () => {
        if (currentIndex > 0) {
            setCurrentIndex(currentIndex - 1);
        }
    };

    if (!transactions || transactions.length === 0) {
        return (
            <div className="risk-report" ref={ref}>
                <header className="header">
                    <img src={`/header.png`} alt="Header" className="header-image" />
                </header>
    
                <div className="main-body" style={{marginTop:"20px"}}>
                    <p>No Data available, try again with uploading below files</p>
    
                    {/* File Download Links */}
                    <div className="download-links" style={{margin:"20px 0",width:"30%",display:"flex"}}>
                        <button className="input-button active" style={{marginRight:"5px"}}>
                        <a href="/sample_transactions.csv" download="transactions.csv" className="download-button">
                            transactions.csv
                        </a>
                        </button>
                        <button className="input-button active">
                        <a href="/sample_transactions.txt" download="transactions.txt" className="download-button">
                            transactions.txt
                        </a>
                        </button>
                    </div>
                </div>
            </div>
        );
    }
    

    const transaction = transactions[currentIndex];

    const takeScreenshot = () => {
        if (!ref.current) return;

        html2canvas(ref.current).then((canvas) => {
            const image = canvas.toDataURL("image/jpeg"); // Convert to JPG format
            const link = document.createElement("a");
            link.href = image;
            link.download = "evidence.jpg"; // Download as JPG
            link.click();
        });
    };
    return (
        <div className="risk-report" ref={ref}>
            <header className="header">
                <img src={`/header.png`} alt="Header" className="header-image" />
            </header>

            <div className="main-body">
                <div className="header-content">
                    <h1 style={{ marginTop: "15px" }}>Risk Report</h1>
                    <p>Automated entity extraction, classification, and risk scoring to empower smarter financial decisions.</p>
                </div>
                <StepperComponent />
                <div className="txid">
                    <div>Transaction ID: {transaction["Transaction ID"]}</div>
                    <div className="navigation-buttons" style={{ display: "flex", width: "30%" }}>
                        <button onClick={handlePrevious} disabled={currentIndex === 0} className="input-button active prev">&lt;</button>
                        <button onClick={handleNext} disabled={currentIndex === transactions.length - 1} className="input-button active next">&gt;</button>
                    </div>
                </div>
                <div className="cl">
                    <div className="left-cont">

                        <RiskScoreIndicator score={transaction.riskScore} />
                        <ConfidenceScoreBar score={transaction.confidenceScore} />
                    </div>
                    <div className="right-cont">
                        <Accordian transaction={transaction} />
                        <button onClick={takeScreenshot} style={{ marginTop: "10px", marginLeft: "23px", width: "92%" }} className="input-button active">
                            Capture Evidence
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RiskReport;

const RiskScoreIndicator = ({ score }) => {
    let riskLevel = score < 0.3 ? "Low" : score < 0.75 ? "Medium" : "High";

    return (
        <div className="risk-score-container">
            <h2 className="section-title">Risk Score Indicator</h2>
            <div className="legend">
                <div className="legend-div"><div className="legend-color one" style={{ backgroundColor: "#5BE12C" }}></div> Low</div>
                <div className="legend-div"><div className="legend-color two" style={{ backgroundColor: "#F5CD19" }}></div> Medium</div>
                <div className="legend-div"><div className="legend-color three" style={{ backgroundColor: "#EA4228" }}></div> High</div>
            </div>
            <GaugeChart
                id="gauge-chart"
                nrOfLevels={30}
                arcsLength={[0.3, 0.45, 0.25]}
                colors={['#5BE12C', '#F5CD19', '#CD1309']}
                percent={score}
                arcWidth={0.3}
                needleColor="grey"
                arcPadding={0.1}
            />
            <div className="risk-level">
                <span className="risk-label">{riskLevel} Risk</span>
            </div>
        </div>
    );
};

const ConfidenceScoreBar = ({ score }) => {
    let barColor = score < 0.5 ? "#CD1309" : score < 0.8 ? "#F5CD19" : "#5BE12C";

    return (
        <div className="confidence-score-container">
            <h2 className="section-title">Confidence Score</h2>
            <div className="legend">
                <div className="legend-div"><div className="legend-color one" style={{ backgroundColor: "#5BE12C" }}></div> Low</div>
                <div className="legend-div"><div className="legend-color two" style={{ backgroundColor: "#F5CD19" }}></div> Medium</div>
                <div className="legend-div"><div className="legend-color three" style={{ backgroundColor: "#EA4228" }}></div> High</div>
            </div>
            <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${score * 100}%`, backgroundColor: barColor }}></div>
            </div>
            <div className="risk-level">
                <span className="risk-label">{score * 100}% Confident</span>
            </div>
        </div>
    );
};
