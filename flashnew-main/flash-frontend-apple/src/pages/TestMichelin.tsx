import React from 'react';
import MichelinAnalysis from '../components/MichelinAnalysis';

const TestMichelin: React.FC = () => {
  return (
    <div style={{ padding: '40px', background: '#f5f5f7', minHeight: '100vh' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '40px' }}>Michelin-Style Framework Analysis Test</h1>
      <MichelinAnalysis />
    </div>
  );
};

export default TestMichelin;