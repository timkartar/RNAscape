import React from 'react';
import './TopRow.css';
import uscLogo from './usc_logotype_white.png'; // Import the USC logo

function TopRow({ onToggleDocumentation, showDocumentation, onLoadExampleData}) {
  return (
    <div className="top-row">
      <h2><a href="https://rohslab.usc.edu/rnascape/#" className="main">RNAscape</a></h2>
      <div className="buttons-and-logo">
        <div className="button-container">
          <button id="run-on-ex-data" className="toggle-docs-btn" type="button" onClick={onLoadExampleData}>
            Run on Example Data
          </button>
          <button className="toggle-docs-btn" onClick={onToggleDocumentation}>
            Documentation
          </button>
        </div>
        <a href="https://www.usc.edu/" className="usc-logo-link">
          <img src={uscLogo} alt="USC Logo" className="usc-logo" />
        </a>
      </div>
    </div>
  );
}

export default TopRow;
