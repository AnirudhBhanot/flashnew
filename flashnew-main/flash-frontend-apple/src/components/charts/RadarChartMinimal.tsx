import React from 'react';
import { motion } from 'framer-motion';
import styles from './RadarChartMinimal.module.scss';

interface RadarChartMinimalProps {
  data: {
    axis: string;
    value: number;
  }[];
  size?: number;
}

export const RadarChartMinimal: React.FC<RadarChartMinimalProps> = ({ 
  data, 
  size = 300 
}) => {
  const center = size / 2;
  const radius = size * 0.4;
  const angleSlice = (Math.PI * 2) / data.length;

  // Create points for the polygon
  const points = data.map((d, i) => {
    const angle = angleSlice * i - Math.PI / 2;
    const x = center + Math.cos(angle) * radius * d.value;
    const y = center + Math.sin(angle) * radius * d.value;
    return { x, y, label: d.axis, value: d.value };
  });

  const polygonPoints = points.map(p => `${p.x},${p.y}`).join(' ');

  // Create axis lines
  const axes = data.map((_, i) => {
    const angle = angleSlice * i - Math.PI / 2;
    const x2 = center + Math.cos(angle) * radius;
    const y2 = center + Math.sin(angle) * radius;
    return { x1: center, y1: center, x2, y2 };
  });

  return (
    <div className={styles.container}>
      <svg width={size} height={size} className={styles.chart}>
        {/* Axis lines */}
        {axes.map((axis, i) => (
          <motion.line
            key={i}
            x1={axis.x1}
            y1={axis.y1}
            x2={axis.x2}
            y2={axis.y2}
            className={styles.axis}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: i * 0.1 }}
          />
        ))}

        {/* Data polygon */}
        <motion.polygon
          points={polygonPoints}
          className={styles.dataArea}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        />

        {/* Labels */}
        {points.map((point, i) => {
          const angle = angleSlice * i - Math.PI / 2;
          const labelRadius = radius + 30;
          const x = center + Math.cos(angle) * labelRadius;
          const y = center + Math.sin(angle) * labelRadius;
          
          return (
            <motion.text
              key={i}
              x={x}
              y={y}
              className={styles.label}
              textAnchor="middle"
              dominantBaseline="middle"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.5 + i * 0.1 }}
            >
              {point.label}
            </motion.text>
          );
        })}
      </svg>

      {/* Legend */}
      <div className={styles.legend}>
        {data.map((item, i) => (
          <motion.div
            key={i}
            className={styles.legendItem}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: 0.8 + i * 0.1 }}
          >
            <span className={styles.legendLabel}>{item.axis}</span>
            <span className={styles.legendValue}>{Math.round(item.value * 100)}%</span>
          </motion.div>
        ))}
      </div>
    </div>
  );
};