// Framework Visualization Component
// Renders different visualization types for business frameworks

import React from 'react';
import { FrameworkAnalysis } from '../../../services/frameworkAnalysisEngine';
import './FrameworkVisualization.css';

interface FrameworkVisualizationProps {
  framework: string;
  analysis: FrameworkAnalysis;
}

export const FrameworkVisualization: React.FC<FrameworkVisualizationProps> = ({ 
  framework, 
  analysis 
}) => {
  const { visualizationData } = analysis;

  switch (visualizationData?.type) {
    case 'matrix_2x2':
      return <Matrix2x2Visualization data={visualizationData} />;
    case 'quadrant':
      return <QuadrantVisualization data={visualizationData} />;
    case 'spider':
      return <SpiderVisualization data={visualizationData} />;
    default:
      return <div className="fv-no-visualization">No visualization available</div>;
  }
};

// BCG Matrix Visualization
const Matrix2x2Visualization: React.FC<{ data: any }> = ({ data }) => {
  const { x, y, position, axes } = data;
  
  // Convert normalized coordinates to percentage
  const xPercent = x * 100;
  const yPercent = y * 100;

  return (
    <div className="fv-matrix-container">
      <div className="fv-matrix">
        {/* Quadrant labels */}
        <div className="fv-quadrant fv-quadrant-tl">
          <span className="fv-quadrant-label">Star</span>
          <div className="fv-quadrant-desc">High Growth, High Share</div>
        </div>
        <div className="fv-quadrant fv-quadrant-tr">
          <span className="fv-quadrant-label">Question Mark</span>
          <div className="fv-quadrant-desc">High Growth, Low Share</div>
        </div>
        <div className="fv-quadrant fv-quadrant-bl">
          <span className="fv-quadrant-label">Cash Cow</span>
          <div className="fv-quadrant-desc">Low Growth, High Share</div>
        </div>
        <div className="fv-quadrant fv-quadrant-br">
          <span className="fv-quadrant-label">Dog</span>
          <div className="fv-quadrant-desc">Low Growth, Low Share</div>
        </div>

        {/* Position marker */}
        <div 
          className="fv-position-marker"
          style={{
            left: `${xPercent}%`,
            bottom: `${yPercent}%`
          }}
        >
          <div className="fv-position-dot" />
          <div className="fv-position-label">{position}</div>
        </div>

        {/* Axes */}
        <div className="fv-axis fv-axis-x">
          <span>{axes.x.label}</span>
        </div>
        <div className="fv-axis fv-axis-y">
          <span>{axes.y.label}</span>
        </div>
      </div>
    </div>
  );
};

// SWOT Quadrant Visualization
const QuadrantVisualization: React.FC<{ data: any }> = ({ data }) => {
  const { strengths, weaknesses, opportunities, threats } = data;

  return (
    <div className="fv-swot-container">
      <div className="fv-swot-grid">
        <div className="fv-swot-section fv-strengths">
          <h4>Strengths</h4>
          <ul>
            {strengths.map((item: string, i: number) => (
              <li key={i}>{item}</li>
            ))}
            {strengths.length === 0 && <li className="fv-empty">None identified</li>}
          </ul>
        </div>
        <div className="fv-swot-section fv-weaknesses">
          <h4>Weaknesses</h4>
          <ul>
            {weaknesses.map((item: string, i: number) => (
              <li key={i}>{item}</li>
            ))}
            {weaknesses.length === 0 && <li className="fv-empty">None identified</li>}
          </ul>
        </div>
        <div className="fv-swot-section fv-opportunities">
          <h4>Opportunities</h4>
          <ul>
            {opportunities.map((item: string, i: number) => (
              <li key={i}>{item}</li>
            ))}
            {opportunities.length === 0 && <li className="fv-empty">None identified</li>}
          </ul>
        </div>
        <div className="fv-swot-section fv-threats">
          <h4>Threats</h4>
          <ul>
            {threats.map((item: string, i: number) => (
              <li key={i}>{item}</li>
            ))}
            {threats.length === 0 && <li className="fv-empty">None identified</li>}
          </ul>
        </div>
      </div>
    </div>
  );
};

// Porter's Five Forces Spider Chart
const SpiderVisualization: React.FC<{ data: any }> = ({ data }) => {
  const { forces, maxValue } = data;
  
  // Calculate positions for pentagon
  const centerX = 150;
  const centerY = 150;
  const radius = 120;
  
  const forceNames = [
    'Competitive Rivalry',
    'Buyer Power',
    'Supplier Power',
    'Threat of Substitutes',
    'Threat of New Entry'
  ];
  
  const forceKeys = [
    'competitive_rivalry',
    'buyer_power',
    'supplier_power',
    'threat_of_substitutes',
    'threat_of_new_entrants'
  ];

  // Calculate points for the spider web
  const points = forceKeys.map((key, i) => {
    const angle = (i * 72 - 90) * Math.PI / 180; // 72 degrees for pentagon
    const value = forces[key] || 0;
    const distance = (value / maxValue) * radius;
    
    return {
      x: centerX + distance * Math.cos(angle),
      y: centerY + distance * Math.sin(angle),
      value,
      name: forceNames[i]
    };
  });

  // Create path for the shape
  const pathData = points
    .map((point, i) => `${i === 0 ? 'M' : 'L'} ${point.x},${point.y}`)
    .join(' ') + ' Z';

  // Create concentric circles for scale
  const circles = [0.2, 0.4, 0.6, 0.8, 1].map(scale => scale * radius);

  return (
    <div className="fv-spider-container">
      <svg width="300" height="300" viewBox="0 0 300 300">
        {/* Background circles */}
        {circles.map((r, i) => (
          <circle
            key={i}
            cx={centerX}
            cy={centerY}
            r={r}
            fill="none"
            stroke="#E8E8ED"
            strokeWidth="1"
          />
        ))}

        {/* Axis lines */}
        {points.map((point, i) => (
          <line
            key={i}
            x1={centerX}
            y1={centerY}
            x2={centerX + radius * Math.cos((i * 72 - 90) * Math.PI / 180)}
            y2={centerY + radius * Math.sin((i * 72 - 90) * Math.PI / 180)}
            stroke="#E8E8ED"
            strokeWidth="1"
          />
        ))}

        {/* Force values shape */}
        <path
          d={pathData}
          fill="rgba(255, 59, 48, 0.2)"
          stroke="#FF3B30"
          strokeWidth="2"
        />

        {/* Force points */}
        {points.map((point, i) => (
          <circle
            key={i}
            cx={point.x}
            cy={point.y}
            r="4"
            fill="#FF3B30"
          />
        ))}

        {/* Labels */}
        {points.map((point, i) => {
          const angle = (i * 72 - 90) * Math.PI / 180;
          const labelX = centerX + (radius + 20) * Math.cos(angle);
          const labelY = centerY + (radius + 20) * Math.sin(angle);
          
          return (
            <text
              key={i}
              x={labelX}
              y={labelY}
              textAnchor="middle"
              dominantBaseline="middle"
              className="fv-spider-label"
            >
              <tspan x={labelX} dy="0">{point.name}</tspan>
              <tspan x={labelX} dy="16" className="fv-spider-value">
                {point.value.toFixed(1)}/10
              </tspan>
            </text>
          );
        })}
      </svg>

      <div className="fv-spider-legend">
        <div className="fv-legend-item">
          <div className="fv-legend-color" style={{ background: '#34C759' }} />
          <span>Favorable (0-3)</span>
        </div>
        <div className="fv-legend-item">
          <div className="fv-legend-color" style={{ background: '#FF9500' }} />
          <span>Moderate (3-7)</span>
        </div>
        <div className="fv-legend-item">
          <div className="fv-legend-color" style={{ background: '#FF3B30' }} />
          <span>Challenging (7-10)</span>
        </div>
      </div>
    </div>
  );
};

export default FrameworkVisualization;