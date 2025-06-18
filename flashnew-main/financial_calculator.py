"""
Financial Calculator for FLASH
Calculates key financial metrics that should be computed backend-side
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class FinancialCalculator:
    """Calculate financial metrics from startup data"""
    
    @staticmethod
    def calculate_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate all financial metrics"""
        metrics = {}
        
        # Calculate LTV if we have the components
        ltv = FinancialCalculator.calculate_ltv(data)
        if ltv is not None:
            metrics['ltv'] = ltv
        
        # Calculate CAC if we have the components
        cac = FinancialCalculator.calculate_cac(data)
        if cac is not None:
            metrics['cac'] = cac
        
        # Calculate LTV/CAC ratio
        if ltv is not None and cac is not None and cac > 0:
            metrics['ltv_cac_ratio'] = ltv / cac
        elif 'ltv_cac_ratio' not in data:
            metrics['ltv_cac_ratio'] = 3.0  # Industry standard default
        
        # Calculate runway
        runway = FinancialCalculator.calculate_runway(data)
        if runway is not None:
            metrics['runway_months'] = runway
        
        # Calculate burn multiple
        burn_multiple = FinancialCalculator.calculate_burn_multiple(data)
        if burn_multiple is not None:
            metrics['burn_multiple'] = burn_multiple
        
        # Calculate gross margin if we have revenue and COGS data
        gross_margin = FinancialCalculator.calculate_gross_margin(data)
        if gross_margin is not None:
            metrics['gross_margin_percent'] = gross_margin
        
        # Add any missing required financial metrics with sensible defaults
        if 'annual_revenue_run_rate' not in data and 'monthly_revenue' in data:
            metrics['annual_revenue_run_rate'] = data['monthly_revenue'] * 12
        
        return metrics
    
    @staticmethod
    def calculate_ltv(data: Dict[str, Any]) -> Optional[float]:
        """Calculate Customer Lifetime Value"""
        try:
            # Method 1: Using ARPU and churn
            if 'arpu' in data and 'monthly_churn_rate' in data:
                arpu = float(data['arpu'])
                churn = float(data['monthly_churn_rate'])
                if churn > 0:
                    return arpu / churn
            
            # Method 2: Using revenue per customer and retention
            if 'average_revenue_per_customer' in data and 'customer_retention_rate' in data:
                arpc = float(data['average_revenue_per_customer'])
                retention = float(data['customer_retention_rate'])
                if retention < 1:
                    churn = 1 - retention
                    if churn > 0:
                        return arpc / churn
            
            # Method 3: If LTV is already provided
            if 'ltv' in data:
                return float(data['ltv'])
            
        except (ValueError, TypeError, ZeroDivisionError) as e:
            logger.warning(f"Error calculating LTV: {e}")
        
        return None
    
    @staticmethod
    def calculate_cac(data: Dict[str, Any]) -> Optional[float]:
        """Calculate Customer Acquisition Cost"""
        try:
            # Method 1: Direct CAC
            if 'customer_acquisition_cost' in data:
                return float(data['customer_acquisition_cost'])
            
            # Method 2: Sales & Marketing spend / New customers
            if 'monthly_sales_marketing_spend' in data and 'new_customers_monthly' in data:
                spend = float(data['monthly_sales_marketing_spend'])
                new_customers = float(data['new_customers_monthly'])
                if new_customers > 0:
                    return spend / new_customers
            
            # Method 3: If CAC is already provided
            if 'cac' in data:
                return float(data['cac'])
            
        except (ValueError, TypeError, ZeroDivisionError) as e:
            logger.warning(f"Error calculating CAC: {e}")
        
        return None
    
    @staticmethod
    def calculate_runway(data: Dict[str, Any]) -> Optional[float]:
        """Calculate runway in months"""
        try:
            # Use provided runway if available
            if 'runway_months' in data and data['runway_months'] is not None:
                return float(data['runway_months'])
            
            # Calculate from cash and burn
            if 'cash_on_hand_usd' in data and 'monthly_burn_usd' in data:
                cash = float(data['cash_on_hand_usd'])
                burn = float(data['monthly_burn_usd'])
                
                if burn > 0:
                    runway = cash / burn
                    # Cap at 120 months (10 years) for reasonableness
                    return min(runway, 120)
                elif burn == 0 and cash > 0:
                    # Profitable or break-even with cash
                    return 120
            
        except (ValueError, TypeError, ZeroDivisionError) as e:
            logger.warning(f"Error calculating runway: {e}")
        
        return None
    
    @staticmethod
    def calculate_burn_multiple(data: Dict[str, Any]) -> Optional[float]:
        """Calculate burn multiple (Net Burn / Net New ARR)"""
        try:
            # Use provided burn multiple if available
            if 'burn_multiple' in data and data['burn_multiple'] is not None:
                return float(data['burn_multiple'])
            
            # Calculate from components
            net_burn = None
            net_new_arr = None
            
            # Calculate net burn
            if 'monthly_burn_usd' in data and 'monthly_revenue' in data:
                gross_burn = float(data['monthly_burn_usd'])
                revenue = float(data.get('monthly_revenue', 0))
                net_burn = gross_burn - revenue
            elif 'net_burn_monthly' in data:
                net_burn = float(data['net_burn_monthly'])
            
            # Calculate net new ARR
            if 'revenue_growth_rate_percent' in data and 'annual_revenue_run_rate' in data:
                growth_rate = float(data['revenue_growth_rate_percent']) / 100
                current_arr = float(data['annual_revenue_run_rate'])
                # Monthly new ARR = (Annual growth rate / 12) * Current ARR
                net_new_arr = (growth_rate / 12) * current_arr
            elif 'net_new_arr_monthly' in data:
                net_new_arr = float(data['net_new_arr_monthly'])
            
            # Calculate burn multiple
            if net_burn is not None and net_new_arr is not None and net_new_arr > 0:
                burn_multiple = net_burn / net_new_arr
                # Cap at reasonable range
                return max(0, min(burn_multiple, 20))
            
        except (ValueError, TypeError, ZeroDivisionError) as e:
            logger.warning(f"Error calculating burn multiple: {e}")
        
        return None
    
    @staticmethod
    def calculate_gross_margin(data: Dict[str, Any]) -> Optional[float]:
        """Calculate gross margin percentage"""
        try:
            # Use provided gross margin if available
            if 'gross_margin_percent' in data and data['gross_margin_percent'] is not None:
                return float(data['gross_margin_percent'])
            
            # Calculate from revenue and COGS
            if 'monthly_revenue' in data and 'monthly_cogs' in data:
                revenue = float(data['monthly_revenue'])
                cogs = float(data['monthly_cogs'])
                if revenue > 0:
                    gross_margin = ((revenue - cogs) / revenue) * 100
                    return max(0, min(gross_margin, 100))
            
            # Alternative calculation
            if 'annual_revenue' in data and 'annual_cogs' in data:
                revenue = float(data['annual_revenue'])
                cogs = float(data['annual_cogs'])
                if revenue > 0:
                    gross_margin = ((revenue - cogs) / revenue) * 100
                    return max(0, min(gross_margin, 100))
            
        except (ValueError, TypeError, ZeroDivisionError) as e:
            logger.warning(f"Error calculating gross margin: {e}")
        
        return None
    
    @staticmethod
    def apply_calculated_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply calculated metrics to the data, preserving existing values"""
        # Make a copy to avoid modifying the original
        enhanced_data = data.copy()
        
        # Calculate metrics
        calculated = FinancialCalculator.calculate_metrics(data)
        
        # Only add calculated values if they don't already exist
        for key, value in calculated.items():
            if key not in enhanced_data or enhanced_data[key] is None:
                enhanced_data[key] = value
                logger.info(f"Calculated {key}: {value}")
        
        return enhanced_data