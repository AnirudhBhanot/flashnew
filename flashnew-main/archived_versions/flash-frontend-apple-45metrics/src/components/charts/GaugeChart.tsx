import React from 'react';
import { motion } from 'framer-motion';
import styles from './GaugeChart.module.scss';

interface GaugeChartProps {
  value: number; // 0-1
  size?: number;
  thickness?: number;
  label?: string;
  showPercentage?: boolean;
}

export const GaugeChart: React.FC<GaugeChartProps> = ({
  value,
  size = 300,
  thickness = 40,
  label = '',
  showPercentage = true
}) => {
  const percentage = Math.round(value * 100);
  const radius = (size - thickness) / 2;
  const circumference = Math.PI * radius; // Half circle
  const strokeDashoffset = circumference - (circumference * value);
  
  // Get color based on value
  const getColor = () => {
    if (value < 0.4) return '#FF453A';
    if (value < 0.6) return '#FF9F0A';
    if (value < 0.8) return '#007AFF';
    return '#32D74B';
  };
  
  const getColorClass = () => {
    if (value < 0.4) return styles.fail;
    if (value < 0.6) return styles.warning;
    if (value < 0.8) return styles.info;
    return styles.success;
  };
  
  return (
    <div className={styles.container} style={{ width: size, height: size / 2 + 40 }}>
      <svg
        width={size}
        height={size / 2 + 40}
        viewBox={`0 0 ${size} ${size / 2 + 40}`}
        className={styles.gauge}
      >
        {/* Background arc */}
        <path
          d={`M ${thickness / 2} ${size / 2 + 20} A ${radius} ${radius} 0 0 1 ${size - thickness / 2} ${size / 2 + 20}`}
          fill="none"
          stroke="#F2F2F7"
          strokeWidth={thickness}
          strokeLinecap="round"
        />
        
        {/* Progress arc */}
        <motion.path
          d={`M ${thickness / 2} ${size / 2 + 20} A ${radius} ${radius} 0 0 1 ${size - thickness / 2} ${size / 2 + 20}`}
          fill="none"
          stroke={getColor()}
          strokeWidth={thickness}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
        />
        
        {/* Labels */}
        <text
          x={thickness / 2}
          y={size / 2 + 40}
          textAnchor="middle"
          fill="#8E8E93"
          fontSize="14"
          fontFamily="-apple-system, BlinkMacSystemFont, 'SF Pro Text'"
        >
          0
        </text>
        <text
          x={size - thickness / 2}
          y={size / 2 + 40}
          textAnchor="middle"
          fill="#8E8E93"
          fontSize="14"
          fontFamily="-apple-system, BlinkMacSystemFont, 'SF Pro Text'"
        >
          100
        </text>
      </svg>
      
      {showPercentage && (
        <div className={styles.centerDisplay}>
          <motion.div 
            className={`${styles.percentage} ${getColorClass()}`}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
          >
            {percentage}%
          </motion.div>
          {label && (
            <motion.div 
              className={styles.label}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8, duration: 0.4 }}
            >
              {label}
            </motion.div>
          )}
        </div>
      )}
    </div>
  );
};