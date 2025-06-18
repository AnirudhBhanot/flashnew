import React from 'react';
import { InvestmentMemo } from './InvestmentMemo';
import './PrintInvestmentMemo.css';

interface PrintInvestmentMemoProps {
  data: any;
}

export const PrintInvestmentMemo: React.FC<PrintInvestmentMemoProps> = ({ data }) => {
  return (
    <div className="print-investment-memo">
      <InvestmentMemo data={data} />
    </div>
  );
};