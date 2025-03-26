import React from 'react';
import {  FileText } from 'react-feather'; // Ensure lucide-react is installed
import './App.css';
import { Database, Shield, CheckCircle } from "react-feather";

const Stats = () => {
  return (
    <div className="stats-container">
      <div className="stats-grid">
        {/* Entities Extracted */}
        <div className="stat-item">
          <div className="stat-icon">
            <Database size={40} color="#CD1309" /> {/* Database icon */}
          </div>
          <div className="stat-content">
            <span className="stat-description">3,500+ Entities Extracted</span>
            <span className="stat-change">+15% vs Last Year</span>
          </div>
        </div>

        {/* Risks Identified */}
        <div className="stat-item">
          <div className="stat-icon">
            <Shield size={40} color="blue" /> {/* Security shield icon */}
          </div>
          <div className="stat-content">
            <span className="stat-description">1,200+ Risks Identified</span>
            <span className="stat-change2">-5% vs Last Year</span>
          </div>
        </div>

        {/* Validated Reports */}
        <div className="stat-item">
          <div className="stat-icon">
            <FileText size={40} color="orange" /> {/* Document icon */}
          </div>
          <div className="stat-content">
            <span className="stat-description">500+ Validated Reports</span>
            <span className="stat-change">+20% vs Last Year</span>
          </div>
        </div>

        {/* Accuracy Achieved */}
        <div className="stat-item">
          <div className="stat-icon">
            <CheckCircle size={40} color="green" /> {/* Checkmark icon */}
          </div>
          <div className="stat-content">
            <span className="stat-description">98% Accuracy Achieved</span>
            <span className="stat-change">+2% vs Last Year</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Stats;