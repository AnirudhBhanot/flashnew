import { useState, useCallback, useRef, useEffect } from 'react';

interface ApiCallOptions<T = unknown> {
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
  retryCount?: number;
  retryDelay?: number;
}

interface ApiCallState<T, TArgs extends unknown[]> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  execute: (...args: TArgs) => Promise<T | undefined>;
  reset: () => void;
  retry: () => void;
}

export function useApiCall<T = unknown, TArgs extends unknown[] = unknown[]>(
  apiFunction: (...args: TArgs) => Promise<T>,
  options: ApiCallOptions<T> = {}
): ApiCallState<T, TArgs> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const mountedRef = useRef(true);
  const lastArgsRef = useRef<TArgs>([] as unknown as TArgs);  
  const retryCountRef = useRef(0);
  
  const { onSuccess, onError, retryCount = 0, retryDelay = 1000 } = options;
  
  useEffect(() => {
    return () => {
      mountedRef.current = false;
    };
  }, []);
  
  const execute = useCallback(async (...args: TArgs): Promise<T | undefined> => {
    lastArgsRef.current = args;
    retryCountRef.current = 0;
    
    const attemptApiCall = async (): Promise<T | undefined> => {
      try {
        setLoading(true);
        setError(null);
        
        const result = await apiFunction(...args);
        
        if (mountedRef.current) {
          setData(result);
          setLoading(false);
          onSuccess?.(result);
          return result;
        }
      } catch (err) {
        if (mountedRef.current) {
          const error = err instanceof Error ? err : new Error(String(err));
          
          // Check if we should retry
          if (retryCountRef.current < retryCount) {
            retryCountRef.current++;
            await new Promise(resolve => setTimeout(resolve, retryDelay));
            return attemptApiCall();
          }
          
          setError(error);
          setLoading(false);
          onError?.(error);
        }
      }
    };
    
    return attemptApiCall();
  }, [apiFunction, onSuccess, onError, retryCount, retryDelay]);
  
  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
    retryCountRef.current = 0;
  }, []);
  
  const retry = useCallback(() => {
    if (lastArgsRef.current.length > 0) {
      execute(...lastArgsRef.current);
    }
  }, [execute]);
  
  return { data, loading, error, execute, reset, retry };
}

// Hook for handling form submissions with API calls
interface FormSubmitOptions<T, TResponse, TApiData = T> extends ApiCallOptions<TResponse> {
  validate?: (data: T) => boolean | string;
  transform?: (data: T) => TApiData;
}

export function useFormSubmit<TForm = unknown, TResponse = unknown, TApiData = TForm>(
  apiFunction: (data: TApiData) => Promise<TResponse>,
  options: FormSubmitOptions<TForm, TResponse, TApiData> = {}
) {
  const [submitting, setSubmitting] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  
  const apiCall = useApiCall<TResponse, [TApiData]>(apiFunction, {
    ...options,
    onSuccess: (data) => {
      setSubmitting(false);
      options.onSuccess?.(data);
    },
    onError: (error) => {
      setSubmitting(false);
      options.onError?.(error);
    }
  });
  
  const handleSubmit = useCallback(async (formData: TForm) => {
    // Validate
    if (options.validate) {
      const validationResult = options.validate(formData);
      if (validationResult !== true) {
        setValidationError(typeof validationResult === 'string' ? validationResult : 'Validation failed');
        return;
      }
    }
    
    setValidationError(null);
    setSubmitting(true);
    
    // Transform data if needed
    const dataToSubmit = options.transform ? options.transform(formData) : formData as unknown as TApiData;
    
    // Execute API call
    await apiCall.execute(dataToSubmit);
  }, [apiCall, options]);
  
  return {
    ...apiCall,
    submitting,
    validationError,
    handleSubmit,
    clearValidationError: () => setValidationError(null)
  };
}