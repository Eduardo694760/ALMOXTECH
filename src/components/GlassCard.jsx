import React from "react";
import "../styles/glass.css";

const GlassCard = ({ children, width = "400px", height = "auto", padding = "20px" }) => {
  return (
    <div 
      className="glass" 
      style={{ 
        width, 
        height, 
        padding, 
        borderRadius: "12px", 
        boxShadow: "0 4px 20px rgba(0,0,0,0.3)" 
      }}
    >
      {children}
    </div>
  );
};

export default GlassCard;
