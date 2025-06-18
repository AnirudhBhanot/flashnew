import React from 'react';
import { AlertCircle } from 'lucide-react';

interface RealisticDisclaimerProps {
  modelAUC?: number;
  className?: string;
}

export const RealisticDisclaimer: React.FC<RealisticDisclaimerProps> = ({ 
  modelAUC = 0.50,
  className = ''
}) => {
  return (
    <div className={`bg-amber-50 border border-amber-200 rounded-lg p-4 ${className}`}>
      <div className="flex items-start space-x-3">
        <AlertCircle className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
        <div className="flex-1">
          <h4 className="text-sm font-semibold text-amber-900 mb-1">
            Important: Prediction Uncertainty
          </h4>
          <p className="text-sm text-amber-800">
            These predictions are based on realistic data showing that early-stage startup success 
            is highly uncertain. Our models achieve approximately {(modelAUC * 100).toFixed(0)}% AUC, 
            meaning predictions are only slightly better than random chance.
          </p>
          <p className="text-xs text-amber-700 mt-2">
            <strong>Why this matters:</strong> Quantitative metrics alone cannot reliably predict 
            startup success. Consider qualitative factors like team execution, market timing, 
            and product-market fit alongside these predictions.
          </p>
        </div>
      </div>
    </div>
  );
};