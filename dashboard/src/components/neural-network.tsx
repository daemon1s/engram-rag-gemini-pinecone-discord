"use client";

import React, { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";

interface Point {
  x: number;
  y: number;
  vx: number;
  vy: number;
}

export function NeuralNetwork() {
  const [points, setPoints] = useState<Point[]>([]);
  const requestRef = useRef<number>(null);

  useEffect(() => {
    const initialPoints: Point[] = Array.from({ length: 40 }).map(() => ({
      x: Math.random() * 100,
      y: Math.random() * 100,
      vx: (Math.random() - 0.5) * 0.05,
      vy: (Math.random() - 0.5) * 0.05,
    }));
    setPoints(initialPoints);

    const animate = () => {
      setPoints((prevPoints) =>
        prevPoints.map((p) => {
          let nx = p.x + p.vx;
          let ny = p.y + p.vy;

          if (nx < 0 || nx > 100) p.vx *= -1;
          if (ny < 0 || ny > 100) p.vy *= -1;

          return { ...p, x: nx, y: ny };
        })
      );
      requestRef.current = requestAnimationFrame(animate);
    };

    requestRef.current = requestAnimationFrame(animate);
    return () => {
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
    };
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden opacity-20">
      <svg className="h-full w-full" preserveAspectRatio="none">
        {points.map((p1, i) =>
          points.slice(i + 1).map((p2, j) => {
            const dist = Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
            if (dist < 20) {
              return (
                <line
                  key={`line-${i}-${j}`}
                  x1={`${p1.x}%`}
                  y1={`${p1.y}%`}
                  x2={`${p2.x}%`}
                  y2={`${p2.y}%`}
                  stroke="white"
                  strokeWidth="0.5"
                  strokeOpacity={(1 - dist / 20) * 0.5}
                />
              );
            }
            return null;
          })
        )}
        {points.map((p, i) => (
          <circle
            key={`point-${i}`}
            cx={`${p.x}%`}
            cy={`${p.y}%`}
            r="1.5"
            fill="white"
            fillOpacity="0.8"
          />
        ))}
      </svg>
    </div>
  );
}
