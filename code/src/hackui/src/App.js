import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import MainContent from './MainContent';
import RiskReport from './RiskReport';
import FancyStepper from './Stepper';
import DataInput from './DataInput';

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainContent />} />
        <Route path="/input" element={<DataInput />} />
        <Route path="/stepper" element={<FancyStepper />} />
        <Route path="/risk-analysis" element={<RiskReport />} />
      </Routes>
    </Router>
  );
}

export default App;
