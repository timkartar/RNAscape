import React from 'react';
import './TopRow.css';

function TopRow({ onToggleDocumentation, showDocumentation }) {
  return (
    <div className="top-row">
      <h2>RNAscape</h2>
      <div className="right-section">
        <a href="/rnascape/3zp8-assembly1.cif" download className="download-link">
          Example Input
        </a>
        <button className="toggle-docs-btn" onClick={onToggleDocumentation}>
          {showDocumentation ? "Hide Documentation" : "Show Documentation"}
        </button>
      </div>
    </div>
  );
}

export default TopRow;
