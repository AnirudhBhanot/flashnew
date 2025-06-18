// Test stage mapping logic
const testStages = [
  'pre_seed',
  'Pre-seed', 
  'Pre Seed',
  'series_a',
  'Series A',
  'Series A+'
];

testStages.forEach(stage => {
  const stageKey = stage.toLowerCase().replace(/\s+/g, '_').replace('-', '_');
  console.log(`"${stage}" -> "${stageKey}"`);
});