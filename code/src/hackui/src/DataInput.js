import React, { useState } from 'react';
import { Upload, FileText } from 'react-feather';
import './App.css';
import { useNavigate } from "react-router-dom";
import StepperComponent from "./StepStatus"; // Import the stepper
import { useTransactions } from "./TransactionContext";

function DataInput() {
    const [showManualEntry, setShowManualEntry] = useState(false);
    const [file, setFile] = useState(null);
    const [text, setText] = useState("");
    const navigate = useNavigate()
    const { setTransactions } = useTransactions();
    const [loading, setLoading] = useState(false)

    // Handle File Upload
    const handleFileChange = (event) => {
        const uploadedFile = event.target.files[0];
        if (uploadedFile) {
            setFile(uploadedFile);
        }
    };

    // Remove Uploaded File
    const clearFile = () => {
        setFile(null);
    };

    // Process Data (Can be expanded based on your use case)
    const processData = async () => {
        if (showManualEntry) {
            alert(`Processing Manual Entry:\n${text}`);
            return;
        }

        if (!file) {
            alert("No file provided!");
            return;
        }
        setLoading(true)
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:8002/upload", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();

            if (response.ok) {
                console.log("File processed successfully!", result);
                setTransactions(result.output_json.transaction);
                setLoading(false)
                navigate("/stepper");
            } else {
                console.error("Error:", result.error);
                setLoading(false)
            }
        } catch (error) {
            setLoading(false)
            console.error("Error processing file:", error);
            alert("Failed to process file. Please try again.");
        }
    }

    return (
        <div className="App">
            <header className="header">
                <img src={`/header.png`} alt="Header" className="header-image" />
            </header>
            <div className='main-body'>
                <div className="left-container">
                    <div className="header-content">
                        <h1>RiskWise</h1>
                        <p>Automating entity extraction, classification, and risk scoring to empower smarter financial decisions.</p>
                    </div>

                    <StepperComponent />
                    {/* Data Input Section */}
                    <div className="data-input">
                        <h2 className="section-title">Data Input</h2>

                        {/* Toggle Between File Upload & Manual Entry */}
                        <div className="input-options">
                            <button
                                onClick={() => setShowManualEntry(false)}
                                className={`input-button ${!showManualEntry ? 'active' : ''}`}
                                style={{ marginRight: "40px" }}
                            >
                                Upload File
                            </button>
                            <button
                                onClick={() => setShowManualEntry(true)}
                                className={`input-button ${showManualEntry ? 'active' : ''}`}
                            >
                                Enter Manual
                            </button>
                        </div>

                        {/* File Upload Section */}
                        {!showManualEntry ? (
                            <div className="file-upload-container">
                                <input
                                    type="file"
                                    accept=".txt,.csv"
                                    onChange={handleFileChange}
                                    className="hidden"
                                    id="file-upload"
                                    style={{ display: "none" }}
                                />
                                <label htmlFor="file-upload" className="upload-label">
                                    <Upload className="upload-icon" />
                                    Drop a file here or click to upload
                                    <span className="supported-formats">Supported formats: .txt, .csv</span>
                                </label>

                                {/* Show Uploaded File Info */}
                                {file && (
                                    <div className="uploaded-file-info">
                                        <FileText className="file-icon" />
                                        <span>{file.name}</span>
                                        <button onClick={clearFile} className="clear-file-btn">✖</button>
                                    </div>
                                )}

                                {/* Process Data Button */}
                                {file && (
                                    <button style={{ marginTop: "10px" }} onClick={processData} className="process-button">Process Data</button>
                                )}
                            </div>
                        ) : (
                            /* Manual Entry Section */
                            <div className="manual-entry-container">
                                <textarea
                                    value={text}
                                    onChange={(e) => setText(e.target.value)}
                                    placeholder="Yet to add this functionality..."
                                    className="textarea-input"
                                />
                                <div className="manual-entry-actions">
                                    <button onClick={() => setText('')} className="clear-text-btn">Clear</button>
                                    <button onClick={processData} className="process-button" disabled>Process Data</button>
                                </div>
                            </div>
                        )}
                    </div>

                    {loading && <div style={{ textAlign: "center", marginTop: "15px" }}>
                        <h2 className="section-title">Loading..</h2>
                    </div>}
                </div>
            </div>
        </div>


    );
}

export default DataInput;