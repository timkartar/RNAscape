import React, { useEffect, useState } from 'react';
import './SplashScreen.css';
import logo from './modern_logo.png'; // Update the path to your logo

function SplashScreen() {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
    }, 2000); // 2 seconds

    return () => clearTimeout(timer);
  }, []);

  if (!visible) return null;

  return (
    <div className="splash-screen">
      <img src={logo} alt="Logo" className="logo-animate" />
    </div>
  );
}

export default SplashScreen;
