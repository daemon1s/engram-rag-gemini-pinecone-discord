"use client";

import React from "react";

export function BackgroundEffects() {
  return (
    <div
      aria-hidden="true"
      style={{
        position: "fixed",
        top: "-20px", 
        left: "-20px",
        right: "-20px",
        bottom: "-20px",
        zIndex: 0,
        pointerEvents: "none",
        overflow: "hidden",
        backgroundColor: "#020617",
      }}
    >
      <svg
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          inset: 0,
        }}
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="none"
      >
        <defs>
          <radialGradient id="glow1" cx="20%" cy="25%" r="70%">
            <stop offset="0%" stopColor="rgba(59,130,246,0.18)" />
            <stop offset="25%" stopColor="rgba(59,130,246,0.12)" />
            <stop offset="50%" stopColor="rgba(59,130,246,0.06)" />
            <stop offset="75%" stopColor="rgba(59,130,246,0.02)" />
            <stop offset="100%" stopColor="rgba(59,130,246,0)" />
          </radialGradient>
          
          <radialGradient id="glow2" cx="85%" cy="85%" r="75%">
            <stop offset="0%" stopColor="rgba(6,182,212,0.09)" />
            <stop offset="35%" stopColor="rgba(6,182,212,0.05)" />
            <stop offset="70%" stopColor="rgba(6,182,212,0.01)" />
            <stop offset="100%" stopColor="rgba(6,182,212,0)" />
          </radialGradient>

          <radialGradient id="glow-balance" cx="75%" cy="80%" r="80%">
            <stop offset="0%" stopColor="rgba(29,78,216,0.04)" />
            <stop offset="100%" stopColor="rgba(29,78,216,0)" />
          </radialGradient>

          <radialGradient id="vignette" cx="50%" cy="45%" r="100%">
            <stop offset="0%" stopColor="rgba(2,6,23,0)" />
            <stop offset="50%" stopColor="rgba(2,6,23,0)" />
            <stop offset="85%" stopColor="rgba(2,6,23,0.4)" />
            <stop offset="100%" stopColor="rgba(2,6,23,0.8)" />
          </radialGradient>
          
          <filter id="noiseFilter" x="-20%" y="-20%" width="140%" height="140%">
            <feTurbulence 
              type="fractalNoise" 
              baseFrequency="0.75" 
              numOctaves="3" 
              stitchTiles="stitch" 
            />
            <feColorMatrix type="saturate" values="0" />
            <feComponentTransfer>
              <feFuncA type="linear" slope="0.045" />
            </feComponentTransfer>
          </filter>
        </defs>

        <rect width="100%" height="100%" fill="#020617" />
        
        <rect width="100%" height="100%" fill="url(#glow1)" />
        <rect width="100%" height="100%" fill="url(#glow-balance)" />
        <rect width="100%" height="100%" fill="url(#glow2)" />
        
        <rect width="100%" height="100%" fill="url(#vignette)" />
        
        <rect 
          width="100%" 
          height="100%" 
          filter="url(#noiseFilter)" 
          opacity="0.5"
        />
      </svg>
    </div>
  );
}
