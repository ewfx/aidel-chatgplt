import React from 'react';
import './App.css';

export default function RiskFactors() {
    const riskFactors = [
        "Fraud Detection",
        "Credit Risk Assessment",
        "AML Compliance",
        "Market Volatility",
        "Regulatory Compliance",
        "Operational Risk",
        "Cybersecurity Threats",
        "Liquidity Risks",
        "Financial Crime Prevention",
        "Sanctions Screening"
      ];
  return (
    <div className="risk-factors-container">
    <h2 className="section-title">Risk Factors Focused On</h2>
    <div className='risk-factors-list'>
      {riskFactors.map((factor, index) => (
        <div className="risk-factor-item" key={index}>
          <div className="risk-factor-line"></div>
          <span>{factor}</span>
        </div>
      ))}
    </div>
  </div>
  )
}
