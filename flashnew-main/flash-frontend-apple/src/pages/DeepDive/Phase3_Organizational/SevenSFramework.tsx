import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js';
import { Radar } from 'react-chartjs-2';
import './SevenSFramework.scss';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

interface SevenSData {
  strategy: {
    current: number;
    desired: number;
    details: {
      clearGoals: number;
      competitivePositioning: number;
      resourceAllocation: number;
    };
  };
  structure: {
    current: number;
    desired: number;
    details: {
      organizationalDesign: number;
      reportingLines: number;
      decisionMaking: number;
    };
  };
  systems: {
    current: number;
    desired: number;
    details: {
      processes: number;
      workflows: number;
      techInfrastructure: number;
    };
  };
  sharedValues: {
    current: number;
    desired: number;
    details: {
      coreBeliefs: number;
      missionAlignment: number;
      culture: number;
    };
  };
  style: {
    current: number;
    desired: number;
    details: {
      leadershipApproach: number;
      managementPractices: number;
    };
  };
  staff: {
    current: number;
    desired: number;
    details: {
      teamComposition: number;
      capabilities: number;
      development: number;
    };
  };
  skills: {
    current: number;
    desired: number;
    details: {
      coreCompetencies: number;
      expertiseGaps: number;
    };
  };
}

const initialData: SevenSData = {
  strategy: {
    current: 3,
    desired: 5,
    details: {
      clearGoals: 3,
      competitivePositioning: 3,
      resourceAllocation: 3
    }
  },
  structure: {
    current: 3,
    desired: 5,
    details: {
      organizationalDesign: 3,
      reportingLines: 3,
      decisionMaking: 3
    }
  },
  systems: {
    current: 3,
    desired: 5,
    details: {
      processes: 3,
      workflows: 3,
      techInfrastructure: 3
    }
  },
  sharedValues: {
    current: 3,
    desired: 5,
    details: {
      coreBeliefs: 3,
      missionAlignment: 3,
      culture: 3
    }
  },
  style: {
    current: 3,
    desired: 5,
    details: {
      leadershipApproach: 3,
      managementPractices: 3
    }
  },
  staff: {
    current: 3,
    desired: 5,
    details: {
      teamComposition: 3,
      capabilities: 3,
      development: 3
    }
  },
  skills: {
    current: 3,
    desired: 5,
    details: {
      coreCompetencies: 3,
      expertiseGaps: 3
    }
  }
};

const SevenSFramework: React.FC = () => {
  const navigate = useNavigate();
  const [data, setData] = useState<SevenSData>(initialData);
  const [activeTab, setActiveTab] = useState<keyof SevenSData>('strategy');

  useEffect(() => {
    const savedData = localStorage.getItem('sevenSFrameworkData');
    if (savedData) {
      setData(JSON.parse(savedData));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('sevenSFrameworkData', JSON.stringify(data));
  }, [data]);

  const updateScore = (
    dimension: keyof SevenSData,
    type: 'current' | 'desired',
    value: number
  ) => {
    setData(prev => ({
      ...prev,
      [dimension]: {
        ...prev[dimension],
        [type]: value
      }
    }));
  };

  const updateDetailScore = (
    dimension: keyof SevenSData,
    detail: string,
    value: number
  ) => {
    setData(prev => {
      const newData = { ...prev };
      const dimensionData = { ...newData[dimension] };
      dimensionData.details = {
        ...dimensionData.details,
        [detail]: value
      };
      
      // Calculate average for current score
      const detailValues = Object.values(dimensionData.details);
      dimensionData.current = Math.round(
        detailValues.reduce((sum, val) => sum + val, 0) / detailValues.length
      );
      
      newData[dimension] = dimensionData;
      return newData;
    });
  };

  const chartData = {
    labels: [
      'Strategy',
      'Structure',
      'Systems',
      'Shared Values',
      'Style',
      'Staff',
      'Skills'
    ],
    datasets: [
      {
        label: 'Current State',
        data: [
          data.strategy.current,
          data.structure.current,
          data.systems.current,
          data.sharedValues.current,
          data.style.current,
          data.staff.current,
          data.skills.current
        ],
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(59, 130, 246, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(59, 130, 246, 1)'
      },
      {
        label: 'Desired State',
        data: [
          data.strategy.desired,
          data.structure.desired,
          data.systems.desired,
          data.sharedValues.desired,
          data.style.desired,
          data.staff.desired,
          data.skills.desired
        ],
        backgroundColor: 'rgba(34, 197, 94, 0.2)',
        borderColor: 'rgba(34, 197, 94, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(34, 197, 94, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(34, 197, 94, 1)'
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        angleLines: {
          display: true
        },
        suggestedMin: 0,
        suggestedMax: 5,
        ticks: {
          stepSize: 1
        }
      }
    },
    plugins: {
      legend: {
        position: 'bottom' as const
      }
    }
  };

  const calculateGap = (dimension: keyof SevenSData): number => {
    return data[dimension].desired - data[dimension].current;
  };

  const getRecommendations = (dimension: keyof SevenSData): string[] => {
    const gap = calculateGap(dimension);
    const recommendations: string[] = [];

    if (gap <= 0) return ['This dimension is already at or exceeding the desired state.'];

    switch (dimension) {
      case 'strategy':
        if (data.strategy.details.clearGoals < 4) {
          recommendations.push('Develop clearer, more specific strategic goals with measurable outcomes');
        }
        if (data.strategy.details.competitivePositioning < 4) {
          recommendations.push('Conduct competitive analysis and define unique value proposition');
        }
        if (data.strategy.details.resourceAllocation < 4) {
          recommendations.push('Align resource allocation with strategic priorities');
        }
        break;

      case 'structure':
        if (data.structure.details.organizationalDesign < 4) {
          recommendations.push('Review and optimize organizational structure for efficiency');
        }
        if (data.structure.details.reportingLines < 4) {
          recommendations.push('Clarify reporting relationships and accountability');
        }
        if (data.structure.details.decisionMaking < 4) {
          recommendations.push('Streamline decision-making processes and delegation');
        }
        break;

      case 'systems':
        if (data.systems.details.processes < 4) {
          recommendations.push('Document and optimize core business processes');
        }
        if (data.systems.details.workflows < 4) {
          recommendations.push('Implement workflow automation where possible');
        }
        if (data.systems.details.techInfrastructure < 4) {
          recommendations.push('Upgrade technology infrastructure to support growth');
        }
        break;

      case 'sharedValues':
        if (data.sharedValues.details.coreBeliefs < 4) {
          recommendations.push('Define and communicate core organizational values');
        }
        if (data.sharedValues.details.missionAlignment < 4) {
          recommendations.push('Ensure all team members understand and align with mission');
        }
        if (data.sharedValues.details.culture < 4) {
          recommendations.push('Foster a positive, inclusive organizational culture');
        }
        break;

      case 'style':
        if (data.style.details.leadershipApproach < 4) {
          recommendations.push('Develop consistent leadership practices across the organization');
        }
        if (data.style.details.managementPractices < 4) {
          recommendations.push('Implement modern management techniques and regular feedback');
        }
        break;

      case 'staff':
        if (data.staff.details.teamComposition < 4) {
          recommendations.push('Assess team composition and fill critical skill gaps');
        }
        if (data.staff.details.capabilities < 4) {
          recommendations.push('Invest in team capability development and training');
        }
        if (data.staff.details.development < 4) {
          recommendations.push('Create career development paths and growth opportunities');
        }
        break;

      case 'skills':
        if (data.skills.details.coreCompetencies < 4) {
          recommendations.push('Identify and develop core competencies critical to success');
        }
        if (data.skills.details.expertiseGaps < 4) {
          recommendations.push('Address expertise gaps through hiring or partnerships');
        }
        break;
    }

    return recommendations;
  };

  const dimensions = [
    {
      key: 'strategy' as keyof SevenSData,
      label: 'Strategy',
      description: 'Clear goals, competitive positioning, and resource allocation',
      icon: '🎯'
    },
    {
      key: 'structure' as keyof SevenSData,
      label: 'Structure',
      description: 'Organizational design, reporting lines, and decision-making',
      icon: '🏗️'
    },
    {
      key: 'systems' as keyof SevenSData,
      label: 'Systems',
      description: 'Processes, workflows, and technology infrastructure',
      icon: '⚙️'
    },
    {
      key: 'sharedValues' as keyof SevenSData,
      label: 'Shared Values',
      description: 'Core beliefs, mission alignment, and culture',
      icon: '💡'
    },
    {
      key: 'style' as keyof SevenSData,
      label: 'Style',
      description: 'Leadership approach and management practices',
      icon: '👔'
    },
    {
      key: 'staff' as keyof SevenSData,
      label: 'Staff',
      description: 'Team composition, capabilities, and development',
      icon: '👥'
    },
    {
      key: 'skills' as keyof SevenSData,
      label: 'Skills',
      description: 'Core competencies and expertise gaps',
      icon: '🎓'
    }
  ];

  const renderDetailAssessment = (dimension: keyof SevenSData) => {
    const dimensionData = data[dimension];
    const details = dimensionData.details;

    return (
      <div className="detail-assessment">
        {Object.entries(details).map(([key, value]) => (
          <div key={key} className="detail-item">
            <label>{key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</label>
            <div className="score-slider">
              <input
                type="range"
                min="1"
                max="5"
                value={value}
                onChange={(e) => updateDetailScore(dimension, key, parseInt(e.target.value))}
              />
              <span className="score-value">{value}</span>
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="seven-s-framework">
      <h1>McKinsey 7S Framework Assessment</h1>
      <p className="intro">
        Assess your organization across seven key dimensions to identify alignment gaps and areas for improvement.
      </p>

      <div className="framework-container">
        <div className="chart-section">
          <h2>Organizational Alignment Overview</h2>
          <div className="radar-chart">
            <Radar data={chartData} options={chartOptions} />
          </div>
        </div>

        <div className="assessment-section">
          <div className="dimension-tabs">
            {dimensions.map(dim => (
              <button
                key={dim.key}
                className={`tab ${activeTab === dim.key ? 'active' : ''}`}
                onClick={() => setActiveTab(dim.key)}
              >
                <span className="icon">{dim.icon}</span>
                <span className="label">{dim.label}</span>
              </button>
            ))}
          </div>

          <div className="dimension-content">
            <h3>{dimensions.find(d => d.key === activeTab)?.label}</h3>
            <p className="description">
              {dimensions.find(d => d.key === activeTab)?.description}
            </p>

            <div className="scores-section">
              <div className="score-item">
                <label>Current State</label>
                <div className="score-display">
                  <span className="score">{data[activeTab].current}</span>
                  <span className="out-of">/ 5</span>
                </div>
              </div>

              <div className="score-item">
                <label>Desired State</label>
                <div className="score-slider">
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={data[activeTab].desired}
                    onChange={(e) => updateScore(activeTab, 'desired', parseInt(e.target.value))}
                  />
                  <span className="score-value">{data[activeTab].desired}</span>
                </div>
              </div>

              <div className="gap-indicator">
                <label>Gap</label>
                <span className={`gap-value ${calculateGap(activeTab) > 2 ? 'high' : calculateGap(activeTab) > 0 ? 'medium' : 'low'}`}>
                  {calculateGap(activeTab)}
                </span>
              </div>
            </div>

            <h4>Detailed Assessment</h4>
            {renderDetailAssessment(activeTab)}

            <div className="recommendations">
              <h4>Recommendations</h4>
              <ul>
                {getRecommendations(activeTab).map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div className="gap-analysis">
        <h2>Gap Analysis Summary</h2>
        <div className="gap-grid">
          {dimensions.map(dim => {
            const gap = calculateGap(dim.key);
            return (
              <div key={dim.key} className={`gap-card ${gap > 2 ? 'high' : gap > 0 ? 'medium' : 'low'}`}>
                <h4>{dim.label}</h4>
                <div className="gap-info">
                  <div className="scores">
                    <span>Current: {data[dim.key].current}</span>
                    <span>Desired: {data[dim.key].desired}</span>
                  </div>
                  <div className="gap-value">Gap: {gap}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="action-buttons">
        <button className="btn-secondary" onClick={() => setData(initialData)}>
          Reset Assessment
        </button>
        <button className="btn-primary" onClick={() => {
          const report = {
            assessment: data,
            timestamp: new Date().toISOString(),
            recommendations: dimensions.reduce((acc, dim) => ({
              ...acc,
              [dim.key]: getRecommendations(dim.key)
            }), {})
          };
          console.log('7S Framework Report:', report);
          alert('Assessment saved! Check console for detailed report.');
        }}>
          Generate Report
        </button>
        <button className="btn-primary" onClick={() => {
          // Check if assessment is complete
          const allDimensionsAssessed = dimensions.every(dim => {
            const dimensionData = data[dim.key];
            return dimensionData.current > 1 && dimensionData.desired > 1;
          });
          
          if (allDimensionsAssessed) {
            // Save data
            localStorage.setItem('sevenSFrameworkData', JSON.stringify(data));
            // Dispatch phase completion event
            window.dispatchEvent(new CustomEvent('deepDivePhaseComplete', { 
              detail: { phaseId: 'phase3' } 
            }));
            alert('Phase 3 completed! Phase 4 is now unlocked.');
            // Navigate to Phase 4
            setTimeout(() => navigate('/deep-dive/phase4'), 1000);
          } else {
            alert('Please complete assessments for all seven dimensions before marking this phase as complete.');
          }
        }}>
          Complete Phase 3
        </button>
      </div>
    </div>
  );
};

export default SevenSFramework;