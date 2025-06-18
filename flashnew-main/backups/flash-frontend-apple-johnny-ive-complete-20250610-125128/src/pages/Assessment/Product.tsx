import React from 'react';
import { FormProvider, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useWizard } from '../../features/wizard/WizardProvider';
import { PrimaryButton, SecondaryButton } from '../../design-system/buttons/AppleButtons';
import { AssessmentLayout } from '../../components/assessment/AssessmentLayout';
import { motion } from '../../helpers/motion';
import { FormField } from '../../design-system/forms/FormField';

// Schema for product-related metrics
const productSchema = z.object({
  // Engagement metrics
  dailyActiveUsers: z.number().min(0).optional().default(1000),
  monthlyActiveUsers: z.number().min(0).optional().default(10000),
  retentionRate: z.number().min(0).max(100).optional().default(85),
  
  // Product metrics
  productMarketFitScore: z.number().min(1).max(5).optional().default(3.5),
  featureAdoptionRate: z.number().min(0).max(100).optional().default(70),
  userEngagementScore: z.number().min(1).max(5).optional().default(3.5),
  
  // Time metrics
  timeToValueDays: z.number().min(0).optional().default(7),
  productStickiness: z.number().min(0).max(100).optional().default(30),
  activationRate: z.number().min(0).max(100).optional().default(60),
  
  // Business metrics
  customerLifetimeValue: z.number().min(0).optional().default(10000),
  averageDealSize: z.number().min(0).optional().default(5000),
  customerSatisfactionScore: z.number().min(0).max(10).optional().default(8),
  salesCycleDays: z.number().min(0).optional().default(30),
  
  // Financial metrics
  grossMargin: z.number().min(0).max(100).optional().default(70),
  revenueGrowthRate: z.number().min(-100).optional().default(100),
  capitalEfficiencyScore: z.number().min(1).max(5).optional().default(3.5),
});

type ProductFormData = z.infer<typeof productSchema>;

const Product: React.FC = () => {
  const { data, updateData, nextStep, previousStep } = useWizard();
  
  // Initialize form with existing data or defaults
  const methods = useForm<ProductFormData>({
    resolver: zodResolver(productSchema),
    defaultValues: data.product || {
      dailyActiveUsers: 1000,
      monthlyActiveUsers: 10000,
      retentionRate: 85,
      productMarketFitScore: 3.5,
      featureAdoptionRate: 70,
      userEngagementScore: 3.5,
      timeToValueDays: 7,
      productStickiness: 30,
      activationRate: 60,
      customerLifetimeValue: 10000,
      averageDealSize: 5000,
      customerSatisfactionScore: 8,
      salesCycleDays: 30,
      grossMargin: 70,
      revenueGrowthRate: 100,
      capitalEfficiencyScore: 3.5,
    },
  });

  const onSubmit = (formData: ProductFormData) => {
    updateData({ product: formData });
    nextStep();
  };

  return (
    <AssessmentLayout
      title="Product & Business Metrics"
      subtitle="Help us understand your product performance and business metrics"
      progress={83} // Step 5 of 6 = 83%
    >
      <FormProvider {...methods}>
        <form onSubmit={methods.handleSubmit(onSubmit)} className="form-container">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="space-y-8"
          >
            {/* User Engagement Section */}
            <div>
              <h3 className="text-lg font-semibold mb-4">User Engagement</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormField
                  name="dailyActiveUsers"
                  label="Daily Active Users"
                  type="number"
                  placeholder="1000"
                  required
                />
                <FormField
                  name="monthlyActiveUsers"
                  label="Monthly Active Users"
                  type="number"
                  placeholder="10000"
                  required
                />
                <FormField
                  name="retentionRate"
                  label="Monthly Retention Rate (%)"
                  type="number"
                  placeholder="85"
                  min={0}
                  max={100}
                  required
                />
                <FormField
                  name="productStickiness"
                  label="Product Stickiness (DAU/MAU %)"
                  type="number"
                  placeholder="30"
                  min={0}
                  max={100}
                  required
                />
              </div>
            </div>

            {/* Product Metrics Section */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Product Performance</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormField
                  name="productMarketFitScore"
                  label="Product-Market Fit Score (1-5)"
                  type="number"
                  placeholder="3.5"
                  step={0.5}
                  min={1}
                  max={5}
                  required
                />
                <FormField
                  name="featureAdoptionRate"
                  label="Feature Adoption Rate (%)"
                  type="number"
                  placeholder="70"
                  min={0}
                  max={100}
                  required
                />
                <FormField
                  name="userEngagementScore"
                  label="User Engagement Score (1-5)"
                  type="number"
                  placeholder="3.5"
                  step={0.5}
                  min={1}
                  max={5}
                  required
                />
                <FormField
                  name="activationRate"
                  label="User Activation Rate (%)"
                  type="number"
                  placeholder="60"
                  min={0}
                  max={100}
                  required
                />
              </div>
            </div>

            {/* Time Metrics Section */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Time-Based Metrics</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormField
                  name="timeToValueDays"
                  label="Time to Value (Days)"
                  type="number"
                  placeholder="7"
                  min={0}
                  required
                />
                <FormField
                  name="salesCycleDays"
                  label="Sales Cycle (Days)"
                  type="number"
                  placeholder="30"
                  min={0}
                  required
                />
              </div>
            </div>

            {/* Business Metrics Section */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Business Metrics</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormField
                  name="customerLifetimeValue"
                  label="Customer Lifetime Value ($)"
                  type="number"
                  placeholder="10000"
                  min={0}
                  required
                />
                <FormField
                  name="averageDealSize"
                  label="Average Deal Size ($)"
                  type="number"
                  placeholder="5000"
                  min={0}
                  required
                />
                <FormField
                  name="customerSatisfactionScore"
                  label="Customer Satisfaction (0-10)"
                  type="number"
                  placeholder="8"
                  step={0.5}
                  min={0}
                  max={10}
                  required
                />
                <FormField
                  name="capitalEfficiencyScore"
                  label="Capital Efficiency Score (1-5)"
                  type="number"
                  placeholder="3.5"
                  step={0.5}
                  min={1}
                  max={5}
                  required
                />
              </div>
            </div>

            {/* Financial Performance Section */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Financial Performance</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormField
                  name="grossMargin"
                  label="Gross Margin (%)"
                  type="number"
                  placeholder="70"
                  min={0}
                  max={100}
                  required
                />
                <FormField
                  name="revenueGrowthRate"
                  label="Monthly Revenue Growth Rate (%)"
                  type="number"
                  placeholder="100"
                  min={-100}
                  required
                />
              </div>
            </div>
          </motion.div>

          <div className="form-navigation">
            <SecondaryButton onClick={previousStep} type="button">
              Previous
            </SecondaryButton>
            <PrimaryButton type="submit">Continue</PrimaryButton>
          </div>
        </form>
      </FormProvider>
    </AssessmentLayout>
  );
};

export default Product;