import React from 'react';
import './TopRow.css';

function TopRow({ onToggleDocumentation, showDocumentation, onLoadExampleData}) {
  return (
    <div className="top-row">
      <h2><a href="https://rohslab.usc.edu/rnascape/#" class="main">RNAscape</a></h2>
      <div className="right-section">
        <button id="run-on-ex-data" className="toggle-docs-btn" type="button" onClick={onLoadExampleData}>
          Run on Example Data
        </button>
        <button className="toggle-docs-btn" onClick={onToggleDocumentation}>
          {/* {showDocumentation ? "Hide Documentation" : "Show Documentation"} */}
          Documentation
        </button>
      </div>
    </div>
  );
}

export default TopRow;
