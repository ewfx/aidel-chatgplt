import React from 'react';
import './App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faClock, faShieldAlt, faExclamationTriangle } from '@fortawesome/free-solid-svg-icons'; // Importing icons

export default function KeyFeatures() {
  return (
    <div className="how-it-works-container" style={{marginRight:"10px"}}>
    <h2 className="section-title">Key Features</h2>
    <ul className="steps-list steps-list2">
      <li><FontAwesomeIcon icon={faClock} size='lg'/><div style={{marginLeft:"20px"}}>Real-Time Processing: Provides instant feedback on data inputs.</div></li>
      <li><FontAwesomeIcon icon={faShieldAlt} size='lg'/><div style={{marginLeft:"20px"}}>Advanced Validation: Multi-layer verification against trusted sources.</div></li>
      <li><FontAwesomeIcon icon={faExclamationTriangle} size='lg'/><div style={{marginLeft:"20px"}}>Risk Scoring: Assigns risk scores to entities with detailed evidence trails.</div></li>
    </ul>
  </div>
  )
}