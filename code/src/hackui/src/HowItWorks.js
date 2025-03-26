import React from 'react';
import './App.css';

export default function HowItWorks() {
  return (
    <div className="how-it-works-container">
    <h2 className="section-title">How It Works</h2>
    <ol className="steps-list">
      <li><div>Upload Data → Upload transaction data via file or manual entry.</div></li>
      <li><div>Process Data → AI extracts key information and classifies entities.</div></li>
      <li><div>Generate Report → Assigns risk levels and provides insights.</div></li>
    </ol>
  </div>
  )
}
