// UI Functionality Test Script
// Run this in browser console to test key UI improvements

const testResults = {
  passed: [],
  failed: [],
  warnings: []
};

// Test 1: Check if design system CSS is loaded
function testDesignSystem() {
  console.log('🔍 Testing Design System...');
  
  const rootStyles = getComputedStyle(document.documentElement);
  const requiredVars = [
    '--color-primary',
    '--font-size-base',
    '--spacing-4',
    '--shadow-md'
  ];
  
  let allFound = true;
  requiredVars.forEach(varName => {
    const value = rootStyles.getPropertyValue(varName);
    if (!value) {
      testResults.failed.push(`CSS variable ${varName} not found`);
      allFound = false;
    }
  });
  
  if (allFound) {
    testResults.passed.push('Design system CSS variables loaded');
  }
}

// Test 2: Check component rendering
function testComponents() {
  console.log('🔍 Testing Component Rendering...');
  
  // Check for key components
  const components = [
    { selector: '.score-card', name: 'ScoreCard' },
    { selector: '.score-comparison', name: 'ScoreComparison' },
    { selector: '.score-breakdown', name: 'ScoreBreakdown' }
  ];
  
  components.forEach(comp => {
    const element = document.querySelector(comp.selector);
    if (element) {
      testResults.passed.push(`${comp.name} component found`);
      
      // Check for animations
      const transition = window.getComputedStyle(element).transition;
      if (transition && transition !== 'none') {
        testResults.passed.push(`${comp.name} has animations`);
      }
    } else {
      testResults.warnings.push(`${comp.name} not visible (may need to submit form first)`);
    }
  });
}

// Test 3: Check typography consistency
function testTypography() {
  console.log('🔍 Testing Typography...');
  
  const elements = document.querySelectorAll('h1, h2, h3, p, .button');
  let hardcodedFonts = 0;
  
  elements.forEach(el => {
    const fontSize = window.getComputedStyle(el).fontSize;
    // Check if it's a hardcoded pixel value
    if (fontSize && !fontSize.includes('rem') && !fontSize.includes('var')) {
      hardcodedFonts++;
    }
  });
  
  if (hardcodedFonts === 0) {
    testResults.passed.push('All typography uses design system');
  } else {
    testResults.warnings.push(`Found ${hardcodedFonts} elements with hardcoded font sizes`);
  }
}

// Test 4: Check responsive behavior
function testResponsive() {
  console.log('🔍 Testing Responsive Design...');
  
  const viewportWidth = window.innerWidth;
  
  if (viewportWidth <= 768) {
    testResults.passed.push('Mobile layout detected');
  } else if (viewportWidth <= 1024) {
    testResults.passed.push('Tablet layout detected');
  } else {
    testResults.passed.push('Desktop layout detected');
  }
  
  // Check for horizontal scroll
  if (document.documentElement.scrollWidth > viewportWidth) {
    testResults.failed.push('Horizontal scroll detected - responsive issue');
  } else {
    testResults.passed.push('No horizontal scroll - responsive working');
  }
}

// Test 5: Check API connectivity
async function testAPI() {
  console.log('🔍 Testing API Connection...');
  
  try {
    const response = await fetch('http://localhost:8001/health');
    const data = await response.json();
    
    if (data.status === 'healthy') {
      testResults.passed.push('API connection successful');
      testResults.passed.push(`Models loaded: ${data.models_loaded}`);
    } else {
      testResults.failed.push('API unhealthy');
    }
  } catch (error) {
    testResults.failed.push(`API connection failed: ${error.message}`);
  }
}

// Test 6: Check for console errors
function testConsoleErrors() {
  console.log('🔍 Checking for Console Errors...');
  
  // This is a simple check - in real testing you'd use a more sophisticated approach
  const originalError = console.error;
  let errorCount = 0;
  
  console.error = function(...args) {
    errorCount++;
    originalError.apply(console, args);
  };
  
  // Restore after a moment
  setTimeout(() => {
    console.error = originalError;
    if (errorCount === 0) {
      testResults.passed.push('No console errors detected');
    } else {
      testResults.failed.push(`${errorCount} console errors detected`);
    }
  }, 100);
}

// Test 7: Check color contrast
function testColorContrast() {
  console.log('🔍 Testing Color Contrast...');
  
  const textElements = document.querySelectorAll('p, span, div, h1, h2, h3, h4, h5, h6');
  let lowContrastCount = 0;
  
  textElements.forEach(el => {
    const styles = window.getComputedStyle(el);
    const color = styles.color;
    const bgColor = styles.backgroundColor;
    
    // Simple check - in production you'd calculate actual contrast ratio
    if (color && bgColor && color === bgColor) {
      lowContrastCount++;
    }
  });
  
  if (lowContrastCount === 0) {
    testResults.passed.push('No obvious contrast issues found');
  } else {
    testResults.failed.push(`${lowContrastCount} potential contrast issues`);
  }
}

// Run all tests
async function runAllTests() {
  console.log('🚀 Starting UI Tests...\n');
  
  testDesignSystem();
  testComponents();
  testTypography();
  testResponsive();
  await testAPI();
  testConsoleErrors();
  testColorContrast();
  
  // Wait for async tests to complete
  setTimeout(() => {
    console.log('\n📊 Test Results:');
    console.log('================\n');
    
    console.log(`✅ PASSED (${testResults.passed.length}):`);
    testResults.passed.forEach(test => console.log(`   ✓ ${test}`));
    
    if (testResults.warnings.length > 0) {
      console.log(`\n⚠️  WARNINGS (${testResults.warnings.length}):`);
      testResults.warnings.forEach(test => console.log(`   ⚠ ${test}`));
    }
    
    if (testResults.failed.length > 0) {
      console.log(`\n❌ FAILED (${testResults.failed.length}):`);
      testResults.failed.forEach(test => console.log(`   ✗ ${test}`));
    }
    
    console.log('\n================');
    console.log(`Total: ${testResults.passed.length} passed, ${testResults.warnings.length} warnings, ${testResults.failed.length} failed`);
    
    // Return results for programmatic access
    return testResults;
  }, 500);
}

// Auto-run tests
runAllTests();

// Export for manual testing
window.uiTests = {
  runAll: runAllTests,
  results: testResults,
  tests: {
    designSystem: testDesignSystem,
    components: testComponents,
    typography: testTypography,
    responsive: testResponsive,
    api: testAPI,
    console: testConsoleErrors,
    contrast: testColorContrast
  }
};