import { useState, useCallback, useEffect } from 'react';

interface ValidationRule {
  required?: boolean;
  min?: number;
  max?: number;
  pattern?: RegExp;
  custom?: (value: any) => string | null;
  message?: string;
}

interface ValidationRules {
  [key: string]: ValidationRule;
}

interface ValidationErrors {
  [key: string]: string;
}

export const useFormValidation = <T extends Record<string, any>>(
  initialData: T,
  rules: ValidationRules,
  realTime: boolean = true
) => {
  const [data, setData] = useState<T>(initialData);
  const [errors, setErrors] = useState<ValidationErrors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const [isValid, setIsValid] = useState(false);

  // Validate a single field
  const validateField = useCallback((field: string, value: any): string | null => {
    const rule = rules[field];
    if (!rule) return null;

    // Required validation
    if (rule.required && (!value || value === '')) {
      return rule.message || `${field} is required`;
    }

    // Min value validation
    if (rule.min !== undefined && typeof value === 'number' && value < rule.min) {
      return rule.message || `${field} must be at least ${rule.min}`;
    }

    // Max value validation
    if (rule.max !== undefined && typeof value === 'number' && value > rule.max) {
      return rule.message || `${field} must be at most ${rule.max}`;
    }

    // Pattern validation
    if (rule.pattern && typeof value === 'string' && !rule.pattern.test(value)) {
      return rule.message || `${field} format is invalid`;
    }

    // Custom validation
    if (rule.custom) {
      return rule.custom(value);
    }

    return null;
  }, [rules]);

  // Validate all fields
  const validateAll = useCallback((): ValidationErrors => {
    const newErrors: ValidationErrors = {};
    
    Object.keys(rules).forEach(field => {
      const error = validateField(field, data[field]);
      if (error) {
        newErrors[field] = error;
      }
    });

    return newErrors;
  }, [data, rules, validateField]);

  // Update field value
  const updateField = useCallback((field: string, value: any) => {
    setData(prev => ({ ...prev, [field]: value }));
    setTouched(prev => ({ ...prev, [field]: true }));

    // Real-time validation
    if (realTime) {
      const error = validateField(field, value);
      setErrors(prev => {
        const newErrors = { ...prev };
        if (error) {
          newErrors[field] = error;
        } else {
          delete newErrors[field];
        }
        return newErrors;
      });
    }
  }, [validateField, realTime]);

  // Check overall validity
  useEffect(() => {
    const hasErrors = Object.keys(errors).length > 0;
    const allRequiredFilled = Object.entries(rules)
      .filter(([_, rule]) => rule.required)
      .every(([field, _]) => data[field] && data[field] !== '');
    
    setIsValid(!hasErrors && allRequiredFilled);
  }, [errors, data, rules]);

  // Submit handler
  const handleSubmit = useCallback((onSubmit: (data: T) => void) => {
    const validationErrors = validateAll();
    
    if (Object.keys(validationErrors).length === 0) {
      onSubmit(data);
    } else {
      setErrors(validationErrors);
      // Mark all fields as touched
      const allTouched = Object.keys(rules).reduce((acc, field) => {
        acc[field] = true;
        return acc;
      }, {} as Record<string, boolean>);
      setTouched(allTouched);
    }
  }, [data, validateAll, rules]);

  return {
    data,
    errors,
    touched,
    isValid,
    updateField,
    handleSubmit,
    validateAll,
    setData,
  };
};

// Common validation rules
export const commonRules = {
  email: {
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    message: 'Please enter a valid email address',
  },
  url: {
    pattern: /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/,
    message: 'Please enter a valid URL',
  },
  percentage: {
    min: 0,
    max: 100,
    message: 'Percentage must be between 0 and 100',
  },
  positiveNumber: {
    min: 0,
    message: 'Value must be positive',
  },
  yearRange: (min: number, max: number) => ({
    min,
    max,
    message: `Year must be between ${min} and ${max}`,
  }),
};