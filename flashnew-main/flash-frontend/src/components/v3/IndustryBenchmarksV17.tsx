import React from 'react';
import { motion } from 'framer-motion';
import { Card } from '../ui/Card';
import { ProgressBar } from '../ui/Progress';
import './IndustryBenchmarksV17.css';

interface BenchmarkData {
  metric: string;
  value: number;
  unit?: string;
  percentile: number;
  p25: number;
  p50: number;
  p75: number;
  description?: string;
}

interface IndustryBenchmarksV17Props {
  sector: string;
  stage: string;
  benchmarks: BenchmarkData[];
}

export const IndustryBenchmarksV17: React.FC<IndustryBenchmarksV17Props> = ({
  sector,
  stage,
  benchmarks
}) => {
  const getPerformanceLevel = (percentile: number) => {
    if (percentile >= 75) return { label: 'Excellent', color: 'var(--color-success)', icon: '🚀' };
    if (percentile >= 50) return { label: 'Good', color: 'var(--color-primary)', icon: '✓' };
    if (percentile >= 25) return { label: 'Average', color: 'var(--color-warning)', icon: '📊' };
    return { label: 'Below Average', color: 'var(--color-error)', icon: '⚠️' };
  };

  const formatValue = (value: number, unit?: string) => {
    if (unit === '%') return `${Math.round(value)}%`;
    if (unit === 'x') return `${value.toFixed(1)}x`;
    if (unit === 'months') return `${Math.round(value)} months`;
    if (unit === '$B') return `$${(value / 1000000000).toFixed(1)}B`;
    if (unit === '$M') return `$${(value / 1000000).toFixed(1)}M`;
    return Math.round(value).toString();
  };

  return (
    <div className="industry-benchmarks-v17">
      <div className="benchmarks-header">
        <h2>Industry Analysis</h2>
        <p className="benchmarks-subtitle">
          Comparing against {stage} stage {sector} companies
        </p>
      </div>

      <div className="benchmarks-grid">
        {benchmarks.map((benchmark, index) => {
          const performance = getPerformanceLevel(benchmark.percentile);
          
          return (
            <motion.div
              key={benchmark.metric}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Card variant="bordered" className="benchmark-card">
                <div className="benchmark-header">
                  <h3>{benchmark.metric}</h3>
                  <div className="benchmark-value">
                    {formatValue(benchmark.value, benchmark.unit)}
                  </div>
                </div>

                <div className="benchmark-percentile">
                  <div className="percentile-label">
                    <span className="percentile-number">{benchmark.percentile}th</span>
                    <span className="percentile-text">percentile</span>
                  </div>
                  <div className="performance-badge" style={{ color: performance.color }}>
                    <span className="performance-icon">{performance.icon}</span>
                    <span className="performance-label">{performance.label}</span>
                  </div>
                </div>

                <div className="benchmark-chart">
                  <ProgressBar 
                    value={benchmark.percentile} 
                    max={100}
                    variant="gradient"
                    showLabel={false}
                  />
                  <div className="benchmark-markers">
                    <div className="marker" style={{ left: '25%' }}>
                      <div className="marker-line" />
                      <div className="marker-label">25th</div>
                      <div className="marker-value">{formatValue(benchmark.p25, benchmark.unit)}</div>
                    </div>
                    <div className="marker" style={{ left: '50%' }}>
                      <div className="marker-line" />
                      <div className="marker-label">50th</div>
                      <div className="marker-value">{formatValue(benchmark.p50, benchmark.unit)}</div>
                    </div>
                    <div className="marker" style={{ left: '75%' }}>
                      <div className="marker-line" />
                      <div className="marker-label">75th</div>
                      <div className="marker-value">{formatValue(benchmark.p75, benchmark.unit)}</div>
                    </div>
                  </div>
                </div>

                {benchmark.description && (
                  <p className="benchmark-description">{benchmark.description}</p>
                )}
              </Card>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};