import { renderHook, act, waitFor } from '@testing-library/react';
import { useApiCall, useFormSubmit } from '../useApiCall';

describe('useApiCall', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should initialize with correct default state', () => {
    const mockApiFunction = jest.fn();
    const { result } = renderHook(() => useApiCall(mockApiFunction));

    expect(result.current.data).toBeNull();
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(typeof result.current.execute).toBe('function');
    expect(typeof result.current.reset).toBe('function');
    expect(typeof result.current.retry).toBe('function');
  });

  it('should handle successful API call', async () => {
    const mockData = { id: 1, name: 'Test' };
    const mockApiFunction = jest.fn().mockResolvedValue(mockData);
    const onSuccess = jest.fn();

    const { result } = renderHook(() => 
      useApiCall(mockApiFunction, { onSuccess })
    );

    await act(async () => {
      await result.current.execute('arg1', 'arg2');
    });

    expect(mockApiFunction).toHaveBeenCalledWith('arg1', 'arg2');
    expect(result.current.data).toEqual(mockData);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(onSuccess).toHaveBeenCalledWith(mockData);
  });

  it('should handle API call error', async () => {
    const mockError = new Error('API Error');
    const mockApiFunction = jest.fn().mockRejectedValue(mockError);
    const onError = jest.fn();

    const { result } = renderHook(() => 
      useApiCall(mockApiFunction, { onError })
    );

    await act(async () => {
      await result.current.execute();
    });

    expect(result.current.data).toBeNull();
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toEqual(mockError);
    expect(onError).toHaveBeenCalledWith(mockError);
  });

  it('should set loading state during API call', async () => {
    const mockApiFunction = jest.fn(() => 
      new Promise(resolve => setTimeout(() => resolve({ data: 'test' }), 100))
    );

    const { result } = renderHook(() => useApiCall(mockApiFunction));

    act(() => {
      result.current.execute();
    });

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });
  });

  it('should reset state correctly', async () => {
    const mockData = { id: 1 };
    const mockApiFunction = jest.fn().mockResolvedValue(mockData);

    const { result } = renderHook(() => useApiCall(mockApiFunction));

    await act(async () => {
      await result.current.execute();
    });

    expect(result.current.data).toEqual(mockData);

    act(() => {
      result.current.reset();
    });

    expect(result.current.data).toBeNull();
    expect(result.current.error).toBeNull();
    expect(result.current.loading).toBe(false);
  });

  it('should retry last API call', async () => {
    const mockApiFunction = jest.fn()
      .mockRejectedValueOnce(new Error('First attempt'))
      .mockResolvedValueOnce({ success: true });

    const { result } = renderHook(() => useApiCall(mockApiFunction));

    await act(async () => {
      await result.current.execute('test');
    });

    expect(result.current.error).toBeTruthy();
    expect(mockApiFunction).toHaveBeenCalledTimes(1);

    await act(async () => {
      await result.current.retry();
    });

    expect(result.current.data).toEqual({ success: true });
    expect(result.current.error).toBeNull();
    expect(mockApiFunction).toHaveBeenCalledTimes(2);
    expect(mockApiFunction).toHaveBeenCalledWith('test');
  });

  it('should handle retry with retryCount option', async () => {
    const mockApiFunction = jest.fn()
      .mockRejectedValueOnce(new Error('Attempt 1'))
      .mockRejectedValueOnce(new Error('Attempt 2'))
      .mockResolvedValueOnce({ success: true });

    const { result } = renderHook(() => 
      useApiCall(mockApiFunction, { retryCount: 2, retryDelay: 10 })
    );

    await act(async () => {
      await result.current.execute();
    });

    expect(result.current.data).toEqual({ success: true });
    expect(mockApiFunction).toHaveBeenCalledTimes(3);
  });
});

describe('useFormSubmit', () => {
  it('should handle form submission with validation', async () => {
    const mockApiFunction = jest.fn().mockResolvedValue({ id: 1 });
    const validate = jest.fn().mockReturnValue(true);
    const transform = jest.fn(data => ({ ...data, transformed: true }));

    const { result } = renderHook(() => 
      useFormSubmit(mockApiFunction, { validate, transform })
    );

    const formData = { name: 'Test' };

    await act(async () => {
      await result.current.handleSubmit(formData);
    });

    expect(validate).toHaveBeenCalledWith(formData);
    expect(transform).toHaveBeenCalledWith(formData);
    expect(mockApiFunction).toHaveBeenCalledWith({ name: 'Test', transformed: true });
    expect(result.current.data).toEqual({ id: 1 });
    expect(result.current.submitting).toBe(false);
  });

  it('should handle validation failure', async () => {
    const mockApiFunction = jest.fn();
    const validate = jest.fn().mockReturnValue('Validation error message');

    const { result } = renderHook(() => 
      useFormSubmit(mockApiFunction, { validate })
    );

    await act(async () => {
      await result.current.handleSubmit({ name: 'Test' });
    });

    expect(result.current.validationError).toBe('Validation error message');
    expect(mockApiFunction).not.toHaveBeenCalled();
    expect(result.current.submitting).toBe(false);
  });

  it('should clear validation error', () => {
    const mockApiFunction = jest.fn();
    const { result } = renderHook(() => useFormSubmit(mockApiFunction));

    act(() => {
      result.current.clearValidationError();
    });

    expect(result.current.validationError).toBeNull();
  });
});