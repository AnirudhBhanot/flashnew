import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import './CAMPRadarChart.css';

interface CAMPRadarChartProps {
  scores: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  benchmarks?: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  stageThresholds?: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
}

export const CAMPRadarChart: React.FC<CAMPRadarChartProps> = ({
  scores,
  benchmarks,
  stageThresholds
}) => {
  const dimensions = ['Capital', 'Advantage', 'Market', 'People'];
  const center = { x: 150, y: 150 };
  const radius = 120;
  const levels = 5;
  
  // Validate and sanitize scores
  const validatedScores = useMemo(() => {
    const validateScore = (score: number, name: string): number => {
      if (typeof score !== 'number' || isNaN(score) || !isFinite(score)) {
        return 0.5;
      }
      const bounded = Math.max(0, Math.min(1, score));
      if (bounded !== score) {
      }
      return bounded;
    };
    
    return {
      capital: validateScore(scores.capital, 'capital'),
      advantage: validateScore(scores.advantage, 'advantage'),
      market: validateScore(scores.market, 'market'),
      people: validateScore(scores.people, 'people')
    };
  }, [scores]);

  // Calculate points for the radar chart
  const calculatePoint = (value: number, index: number, scale: number = radius) => {
    const angle = (Math.PI * 2 * index) / dimensions.length - Math.PI / 2;
    return {
      x: center.x + Math.cos(angle) * value * scale,
      y: center.y + Math.sin(angle) * value * scale
    };
  };

  const scorePoints = useMemo(() => {
    return dimensions.map((_, i) => {
      const value = Object.values(validatedScores)[i];
      return calculatePoint(value, i);
    });
  }, [scores]);

  const benchmarkPoints = useMemo(() => {
    if (!benchmarks) return null;
    return dimensions.map((_, i) => {
      const value = Object.values(benchmarks)[i];
      return calculatePoint(value, i);
    });
  }, [benchmarks]);

  const thresholdPoints = useMemo(() => {
    if (!stageThresholds) return null;
    return dimensions.map((_, i) => {
      const value = Object.values(stageThresholds)[i];
      return calculatePoint(value, i);
    });
  }, [stageThresholds]);

  // Create path string from points
  const createPath = (points: { x: number; y: number }[]) => {
    return points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ') + ' Z';
  };

  const getScoreColor = (pillar: string, score: number) => {
    const threshold = stageThresholds ? stageThresholds[pillar.toLowerCase() as keyof typeof stageThresholds] : 0.5;
    if (score >= threshold + 0.2) return '#FFFFFF';
    if (score >= threshold) return '#E8EAED';
    if (score >= threshold - 0.1) return '#9CA3AF';
    return '#6B7280';
  };

  const getIcon = (dimension: string) => {
    const icons: Record<string, string> = {
      Capital: '💰',
      Advantage: '⚡',
      Market: '📈',
      People: '👥'
    };
    return icons[dimension] || '📊';
  };

  return (
    <div className="radar-chart-container">
      <svg viewBox="0 0 300 300" className="radar-svg">
        {/* Grid circles */}
        {Array.from({ length: levels }, (_, i) => (
          <circle
            key={i}
            cx={center.x}
            cy={center.y}
            r={(radius / levels) * (i + 1)}
            fill="none"
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth="1"
          />
        ))}

        {/* Grid lines */}
        {dimensions.map((_, i) => {
          const endPoint = calculatePoint(1, i);
          return (
            <line
              key={i}
              x1={center.x}
              y1={center.y}
              x2={endPoint.x}
              y2={endPoint.y}
              stroke="rgba(255, 255, 255, 0.1)"
              strokeWidth="1"
            />
          );
        })}

        {/* Threshold area (if provided) */}
        {thresholdPoints && (
          <motion.path
            d={createPath(thresholdPoints)}
            fill="rgba(255, 149, 0, 0.1)"
            stroke="rgba(255, 149, 0, 0.4)"
            strokeWidth="2"
            strokeDasharray="5,5"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          />
        )}

        {/* Benchmark area (if provided) */}
        {benchmarkPoints && (
          <motion.path
            d={createPath(benchmarkPoints)}
            fill="none"
            stroke="rgba(255, 255, 255, 0.3)"
            strokeWidth="2"
            strokeDasharray="10,5"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          />
        )}

        {/* Score area */}
        <motion.path
          d={createPath(scorePoints)}
          fill="rgba(59, 130, 246, 0.2)"
          stroke="rgba(59, 130, 246, 0.8)"
          strokeWidth="3"
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.3, type: "spring" }}
          style={{ transformOrigin: "150px 150px" }}
        />

        {/* Score points */}
        {scorePoints.map((point, i) => (
          <motion.circle
            key={i}
            cx={point.x}
            cy={point.y}
            r="6"
            fill={getScoreColor(dimensions[i], Object.values(validatedScores)[i])}
            stroke="#ffffff"
            strokeWidth="2"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.3, delay: 0.5 + i * 0.1 }}
          />
        ))}

        {/* Dimension labels */}
        {dimensions.map((dim, i) => {
          const labelPoint = calculatePoint(1.25, i);
          return (
            <text
              key={i}
              x={labelPoint.x}
              y={labelPoint.y}
              textAnchor="middle"
              dominantBaseline="middle"
              className="dimension-label"
            >
              {getIcon(dim)}
            </text>
          );
        })}
      </svg>

      {/* Legend */}
      <div className="radar-legend">
        {dimensions.map((dim, i) => {
          const score = Object.values(validatedScores)[i];
          const threshold = stageThresholds ? Object.values(stageThresholds)[i] : 0.5;
          return (
            <motion.div 
              key={dim}
              className="legend-item"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.7 + i * 0.1 }}
            >
              <div className="legend-header">
                <span className="legend-icon">{getIcon(dim)}</span>
                <span className="legend-name">{dim}</span>
              </div>
              <div className="score-bar-container">
                <div className="score-bar">
                  <motion.div 
                    className="score-fill"
                    style={{ 
                      backgroundColor: getScoreColor(dim, score),
                      width: `${score * 100}%` 
                    }}
                    initial={{ width: 0 }}
                    animate={{ width: `${score * 100}%` }}
                    transition={{ duration: 0.8, delay: 0.9 + i * 0.1 }}
                  />
                  {threshold && (
                    <div 
                      className="threshold-marker"
                      style={{ left: `${threshold * 100}%` }}
                      title={`Minimum: ${Math.round(threshold * 100)}%`}
                    />
                  )}
                </div>
                <span className="score-value">{Math.round(score * 100)}%</span>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Performance Summary */}
      <motion.div 
        className="performance-summary"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.2 }}
      >
        <div className="summary-item">
          <span className="summary-label">Overall Score</span>
          <span className="summary-value">
            {Math.round((Object.values(validatedScores).reduce((a, b) => a + b, 0) / 4) * 100)}%
          </span>
        </div>
        {benchmarks && (
          <div className="summary-item">
            <span className="summary-label">vs. Industry</span>
            <span className="summary-value">
              {(() => {
                const avgScore = Object.values(validatedScores).reduce((a, b) => a + b, 0) / 4;
                const avgBenchmark = Object.values(benchmarks).reduce((a, b) => a + b, 0) / 4;
                const diff = Math.round((avgScore - avgBenchmark) * 100);
                return diff > 0 ? `+${diff}%` : `${diff}%`;
              })()}
            </span>
          </div>
        )}
      </motion.div>
    </div>
  );
};