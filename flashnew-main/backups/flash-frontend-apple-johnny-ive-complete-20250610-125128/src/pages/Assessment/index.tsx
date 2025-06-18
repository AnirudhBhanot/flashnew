import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { WizardProvider } from '../../features/wizard/WizardProvider';
import CompanyInfo from './CompanyInfo';
import Capital from './Capital';
import Advantage from './Advantage';
import Market from './Market';
import People from './People';
import Review from './Review';

const Assessment: React.FC = () => {
  return (
    <WizardProvider>
      <Routes>
        <Route path="company" element={<CompanyInfo />} />
        <Route path="capital" element={<Capital />} />
        <Route path="advantage" element={<Advantage />} />
        <Route path="market" element={<Market />} />
        <Route path="people" element={<People />} />
        <Route path="review" element={<Review />} />
        <Route path="*" element={<Navigate to="company" replace />} />
      </Routes>
    </WizardProvider>
  );
};

export default Assessment;