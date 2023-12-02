// src/TopRow.js
import React from 'react';
import './TopRow.css';

function TopRow({ onToggleDocumentation, showDocumentation }) {
  return (
    <div className="top-row">
      <h2>RNAScape</h2>
      <button className="toggle-docs-btn" onClick={onToggleDocumentation}>
        {showDocumentation ? "Hide Documentation" : "Show Documentation"}
      </button>
    </div>
  );
}

export default TopRow;
