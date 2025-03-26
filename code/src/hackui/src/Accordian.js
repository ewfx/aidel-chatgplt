import * as React from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import './App.css'

export default function CustomAccordion({ transaction }) {
  return (
    <div className="accordion-container">
      {/* Justification */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <h2 style={{fontSize:"1.7em"}}>Justification</h2>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>{transaction.reason}</Typography>
        </AccordionDetails>
      </Accordion>

      {/* Supporting Evidence */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <h2 style={{fontSize:"1.7em"}}>Supporting Evidence</h2>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>{transaction.supportingEvidence.join(", ")}</Typography>
        </AccordionDetails>
      </Accordion>

      {/* Entities Extracted */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <h2 style={{fontSize:"1.7em"}}>Entities Extracted</h2>
        </AccordionSummary>
        <AccordionDetails>
          {transaction.extractedEntities.map((entity, index) => (
            <Typography key={index}>
              <strong>{entity}</strong> - {transaction.entityTypes[index]}
            </Typography>
          ))}
        </AccordionDetails>
      </Accordion>
    </div>
  );
}
