import React from 'react';
import './LogPopup.css'; // Make sure to create this CSS file for styling

const LogPopup = ({ isVisible, text, onClose }) => {
  if (!isVisible) return null;

  return (
    <div className="log-popup-overlay">
      <div className="log-popup">
        <button className="close-btn" onClick={onClose}>×</button>
        <h2>Log</h2>
        <div className="log-content">
          <pre>{text}</pre>
        </div>
      </div>
    </div>
  );
};

export default LogPopup;
