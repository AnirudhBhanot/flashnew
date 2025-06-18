import { useEffect, useRef, useState } from 'react';

interface ScrollAnimationOptions {
  threshold?: number;
  rootMargin?: string;
  animateOnce?: boolean;
}

export const useScrollAnimation = (
  options: ScrollAnimationOptions = {}
): [React.RefObject<HTMLDivElement | null>, boolean] => {
  const {
    threshold = 0.1,
    rootMargin = '0px',
    animateOnce = true
  } = options;

  const ref = useRef<HTMLDivElement>(null);
  const [isInView, setIsInView] = useState(false);
  const [hasAnimated, setHasAnimated] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    // Skip if already animated and animateOnce is true
    if (animateOnce && hasAnimated) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        const inView = entry.isIntersecting;
        setIsInView(inView);
        
        if (inView && animateOnce) {
          setHasAnimated(true);
        }
      },
      {
        threshold,
        rootMargin
      }
    );

    observer.observe(element);

    return () => {
      observer.unobserve(element);
    };
  }, [threshold, rootMargin, animateOnce, hasAnimated]);

  return [ref, isInView];
};

// Hook for stagger animations
export const useStaggerAnimation = (
  itemCount: number,
  baseDelay: number = 50
) => {
  const [isVisible, setIsVisible] = useState(false);

  const getDelay = (index: number) => {
    return isVisible ? index * baseDelay : 0;
  };

  const triggerAnimation = () => {
    setIsVisible(true);
  };

  return { getDelay, triggerAnimation, isVisible };
};

// Hook for magnetic hover effect
export const useMagneticHover = () => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = element.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      
      const distance = Math.sqrt(x * x + y * y);
      const maxDistance = Math.max(rect.width, rect.height) / 2;
      
      if (distance < maxDistance * 1.5) {
        const strength = 1 - distance / (maxDistance * 1.5);
        const translateX = x * strength * 0.1;
        const translateY = y * strength * 0.1;
        
        element.style.transform = `translate(${translateX}px, ${translateY}px)`;
      }
    };

    const handleMouseLeave = () => {
      element.style.transform = '';
    };

    element.addEventListener('mousemove', handleMouseMove);
    element.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      element.removeEventListener('mousemove', handleMouseMove);
      element.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  return ref;
};

// Hook for number counter animation
export const useCountAnimation = (
  end: number,
  duration: number = 1000,
  start: number = 0
) => {
  const [count, setCount] = useState(start);
  const countRef = useRef(start);
  
  useEffect(() => {
    const startTime = Date.now();
    const endTime = startTime + duration;
    
    const updateCount = () => {
      const now = Date.now();
      const progress = Math.min((now - startTime) / duration, 1);
      
      // Easing function for smooth animation
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      const currentCount = start + (end - start) * easeOutQuart;
      
      countRef.current = currentCount;
      setCount(Math.floor(currentCount));
      
      if (progress < 1) {
        requestAnimationFrame(updateCount);
      } else {
        setCount(end);
      }
    };
    
    updateCount();
  }, [end, duration, start]);
  
  return count;
};