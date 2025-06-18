# FLASH Assessment Wizard - Apple Design Implementation

## Wizard Architecture

### Flow Overview
```
Landing → Company Info → Capital → Advantage → Market → People → Review → Analysis → Results
```

### Navigation Patterns

#### 1. Segmented Progress Bar
```jsx
<ProgressBar
  segments={['Company', 'Capital', 'Advantage', 'Market', 'People']}
  current={currentStep}
  completed={completedSteps}
/>
```

#### 2. Gesture-Based Navigation
- Swipe right to go back
- Swipe left to continue (when valid)
- Tap progress bar to jump (completed sections only)
- Keyboard: Tab/Shift+Tab, Enter to continue

### Page Specifications

#### Landing Page

```jsx
<LandingPage>
  <NavigationBar transparent>
    <NavTitle>FLASH</NavTitle>
    <NavActions>
      <Button variant="text">About</Button>
      <Button variant="text">Sign In</Button>
    </NavActions>
  </NavigationBar>
  
  <Hero>
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease: [0.2, 0, 0, 1] }}
    >
      <LargeTitle>
        Know Your Startup's
        <GradientText>True Potential</GradientText>
      </LargeTitle>
      
      <Subtitle>
        Get an honest assessment powered by machine learning
        and validated by analyzing 100,000+ startups
      </Subtitle>
      
      <ButtonGroup>
        <Button variant="primary" size="large">
          Begin Assessment
          <Icon name="arrow.right" />
        </Button>
        
        <Button variant="secondary" size="large">
          <Icon name="play.circle" />
          Watch Demo
        </Button>
      </ButtonGroup>
    </motion.div>
    
    <HeroVisual>
      {/* Animated 3D visualization of interconnected nodes */}
      <Canvas>
        <StartupNetworkVisualization />
      </Canvas>
    </HeroVisual>
  </Hero>
  
  <Features>
    <Container>
      <SectionTitle>Why FLASH is Different</SectionTitle>
      
      <FeatureGrid>
        <FeatureCard
          icon="brain"
          title="Honest Predictions"
          description="No sugar-coating. Real probabilities based on real data."
          delay={0.1}
        />
        
        <FeatureCard
          icon="chart.line.uptrend"
          title="Pattern Recognition"
          description="Identifies which of 50+ success patterns match your startup."
          delay={0.2}
        />
        
        <FeatureCard
          icon="building.2"
          title="Industry Specific"
          description="Tailored insights for SaaS, FinTech, HealthTech, and more."
          delay={0.3}
        />
        
        <FeatureCard
          icon="sparkles"
          title="Actionable Insights"
          description="Get specific recommendations, not generic advice."
          delay={0.4}
        />
      </FeatureGrid>
    </Container>
  </Features>
  
  <Trust>
    <Container>
      <TrustLogos>
        {/* Grayscale logos with hover color */}
      </TrustLogos>
      
      <Testimonial>
        <Quote>
          "FLASH gave us insights we couldn't see ourselves. 
          The pattern matching identified we were following the 
          'Technical Innovation' path before we realized it."
        </Quote>
        <Attribution>
          <Avatar src="/founders/1.jpg" />
          <div>
            <Name>Sarah Chen</Name>
            <Title>Founder, TechCo</Title>
          </div>
        </Attribution>
      </Testimonial>
    </Container>
  </Trust>
  
  <CTA>
    <Container>
      <CTACard>
        <Title>Ready to see the truth?</Title>
        <Subtitle>
          Takes 5 minutes. No signup required.
        </Subtitle>
        <Button variant="primary" size="large">
          Start Free Assessment
        </Button>
      </CTACard>
    </Container>
  </CTA>
</LandingPage>
```

#### Company Information (Step 1)

```jsx
<WizardPage step={1} title="Tell us about your company">
  <WizardContent>
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
    >
      <FormSection>
        <TextField
          label="Company Name"
          placeholder="Acme Inc."
          value={companyName}
          onChange={setCompanyName}
          autoFocus
        />
        
        <Select
          label="Industry"
          placeholder="Select your industry"
          value={industry}
          onChange={setIndustry}
        >
          <Option value="saas">SaaS</Option>
          <Option value="fintech">FinTech</Option>
          <Option value="healthtech">HealthTech</Option>
          {/* ... more options */}
        </Select>
        
        <Select
          label="Stage"
          placeholder="Current funding stage"
          value={stage}
          onChange={setStage}
          helper="This helps us provide stage-appropriate insights"
        >
          <Option value="pre_seed">Pre-seed</Option>
          <Option value="seed">Seed</Option>
          <Option value="series_a">Series A</Option>
          <Option value="series_b">Series B</Option>
          <Option value="series_c">Series C+</Option>
        </Select>
        
        <DatePicker
          label="Founded"
          placeholder="When was your company founded?"
          value={foundedDate}
          onChange={setFoundedDate}
          max={new Date()}
        />
      </FormSection>
    </motion.div>
  </WizardContent>
  
  <WizardActions>
    <Button variant="text" onClick={handleBack}>
      Back
    </Button>
    <Button 
      variant="primary" 
      onClick={handleContinue}
      disabled={!isValid}
    >
      Continue
    </Button>
  </WizardActions>
</WizardPage>
```

#### Capital Assessment (Step 2)

```jsx
<WizardPage step={2} title="Capital & Financials">
  <WizardContent>
    <InfoCard>
      <Icon name="info.circle" />
      <Text>
        Your financial information is never stored and is only used 
        for this assessment.
      </Text>
    </InfoCard>
    
    <FormSection>
      <CurrencyField
        label="Total Funding Raised"
        placeholder="0"
        value={totalFunding}
        onChange={setTotalFunding}
        currency="USD"
        helper="Include all rounds: pre-seed, seed, Series A, etc."
      />
      
      <NumberField
        label="Monthly Burn Rate"
        placeholder="0"
        value={burnRate}
        onChange={setBurnRate}
        prefix="$"
        suffix="/month"
        helper="Average monthly expenses minus revenue"
      />
      
      <NumberField
        label="Runway"
        placeholder="0"
        value={runway}
        onChange={setRunway}
        suffix="months"
        helper="How many months until you need more funding?"
      />
      
      <CurrencyField
        label="Annual Revenue Run Rate"
        placeholder="0"
        value={arr}
        onChange={setARR}
        helper="Current MRR × 12"
      />
      
      <ToggleSection
        label="Show advanced metrics"
        defaultOpen={false}
      >
        <PercentageField
          label="Gross Margin"
          value={grossMargin}
          onChange={setGrossMargin}
        />
        
        <RatioField
          label="LTV:CAC Ratio"
          value={ltvCac}
          onChange={setLtvCac}
          placeholder="3:1"
        />
      </ToggleSection>
    </FormSection>
  </WizardContent>
</WizardPage>
```

#### Advantage Assessment (Step 3)

```jsx
<WizardPage step={3} title="Competitive Advantage">
  <WizardContent>
    <FormSection>
      <ScaleSelector
        label="How strong is your competitive moat?"
        value={moatStrength}
        onChange={setMoatStrength}
        min={1}
        max={10}
        labels={{
          1: "None",
          5: "Moderate",
          10: "Unbeatable"
        }}
      />
      
      <MultiSelect
        label="What gives you an edge?"
        placeholder="Select all that apply"
        value={advantages}
        onChange={setAdvantages}
      >
        <Option value="patents">Patents/IP</Option>
        <Option value="network_effects">Network Effects</Option>
        <Option value="brand">Strong Brand</Option>
        <Option value="data">Proprietary Data</Option>
        <Option value="team">Expert Team</Option>
        <Option value="partnerships">Key Partnerships</Option>
        <Option value="first_mover">First Mover</Option>
        <Option value="cost">Cost Advantage</Option>
      </MultiSelect>
      
      <TextArea
        label="Describe your unique advantage"
        placeholder="What makes you different from competitors?"
        value={uniqueAdvantage}
        onChange={setUniqueAdvantage}
        rows={4}
        maxLength={500}
        showCount
      />
      
      <BinaryChoice
        label="Do you have patents?"
        value={hasPatents}
        onChange={setHasPatents}
      />
      
      {hasPatents && (
        <NumberField
          label="Number of Patents"
          value={patentCount}
          onChange={setPatentCount}
          min={1}
        />
      )}
    </FormSection>
  </WizardContent>
</WizardPage>
```

#### Market Assessment (Step 4)

```jsx
<WizardPage step={4} title="Market Opportunity">
  <WizardContent>
    <FormSection>
      <CurrencyField
        label="Total Addressable Market (TAM)"
        placeholder="0"
        value={tam}
        onChange={setTAM}
        suffix="billion"
        helper="The total market demand for your product"
      />
      
      <PercentageField
        label="Serviceable Addressable Market"
        placeholder="0"
        value={samPercentage}
        onChange={setSAMPercentage}
        helper="What % of TAM can you realistically serve?"
      />
      
      <PercentageField
        label="Year-over-Year Market Growth"
        placeholder="0"
        value={marketGrowth}
        onChange={setMarketGrowth}
        helper="How fast is your market growing?"
      />
      
      <ScaleSelector
        label="Market Competition"
        value={competition}
        onChange={setCompetition}
        min={1}
        max={10}
        labels={{
          1: "Blue Ocean",
          5: "Moderate",
          10: "Red Ocean"
        }}
      />
      
      <NumberField
        label="Customer Acquisition Cost"
        placeholder="0"
        value={cac}
        onChange={setCAC}
        prefix="$"
        helper="Average cost to acquire one customer"
      />
      
      <NumberField
        label="Average Revenue Per User"
        placeholder="0"
        value={arpu}
        onChange={setARPU}
        prefix="$"
        suffix="/month"
      />
    </FormSection>
  </WizardContent>
</WizardPage>
```

#### People Assessment (Step 5)

```jsx
<WizardPage step={5} title="Team & Leadership">
  <WizardContent>
    <FormSection>
      <NumberField
        label="Full-Time Team Size"
        placeholder="0"
        value={teamSize}
        onChange={setTeamSize}
        helper="Excluding contractors and part-time"
      />
      
      <NumberField
        label="Technical Team Members"
        placeholder="0"
        value={techTeam}
        onChange={setTechTeam}
        max={teamSize}
      />
      
      <NumberField
        label="Average Years of Experience"
        placeholder="0"
        value={avgExperience}
        onChange={setAvgExperience}
        suffix="years"
        helper="Average across all team members"
      />
      
      <MultiSelect
        label="Founder Backgrounds"
        placeholder="Select all that apply"
        value={founderBackgrounds}
        onChange={setFounderBackgrounds}
      >
        <Option value="serial_entrepreneur">Serial Entrepreneur</Option>
        <Option value="industry_expert">Industry Expert</Option>
        <Option value="technical_expert">Technical Expert</Option>
        <Option value="sales_marketing">Sales/Marketing Expert</Option>
        <Option value="first_time">First-Time Founder</Option>
      </MultiSelect>
      
      <BinaryChoice
        label="Have the founders worked together before?"
        value={foundersWorkedTogether}
        onChange={setFoundersWorkedTogether}
      />
      
      <ScaleSelector
        label="Team Culture Strength"
        value={cultureStrength}
        onChange={setCultureStrength}
        min={1}
        max={10}
        labels={{
          1: "Struggling",
          5: "Developing",
          10: "Exceptional"
        }}
      />
    </FormSection>
  </WizardContent>
</WizardPage>
```

#### Review Page (Step 6)

```jsx
<WizardPage step={6} title="Review Your Information">
  <WizardContent>
    <ReviewSections>
      {sections.map((section, index) => (
        <ReviewCard
          key={section.id}
          delay={index * 0.1}
          onClick={() => navigateToSection(section.id)}
        >
          <ReviewHeader>
            <Icon name={section.icon} />
            <Title>{section.title}</Title>
            <Button variant="text" size="small">
              Edit
            </Button>
          </ReviewHeader>
          
          <ReviewContent>
            {section.fields.map(field => (
              <ReviewField key={field.key}>
                <Label>{field.label}</Label>
                <Value>{formatValue(field.value, field.type)}</Value>
              </ReviewField>
            ))}
          </ReviewContent>
        </ReviewCard>
      ))}
    </ReviewSections>
    
    <Disclaimer>
      <Icon name="lock.shield" />
      <Text>
        Your data is processed locally and never stored. 
        The analysis is for informational purposes only.
      </Text>
    </Disclaimer>
  </WizardContent>
  
  <WizardActions>
    <Button variant="text" onClick={handleBack}>
      Back
    </Button>
    <Button 
      variant="primary" 
      onClick={handleAnalyze}
      size="large"
    >
      Analyze My Startup
      <Icon name="arrow.right" />
    </Button>
  </WizardActions>
</WizardPage>
```

### Animations & Transitions

#### Page Transitions
```jsx
const pageTransition = {
  initial: { opacity: 0, x: 60 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -60 },
  transition: {
    duration: 0.4,
    ease: [0.2, 0, 0, 1] // Apple's emphasized easing
  }
};
```

#### Form Field Animations
```jsx
const fieldAnimation = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: {
    duration: 0.3,
    ease: "easeOut"
  }
};
```

#### Progress Bar Animation
```jsx
const progressAnimation = {
  initial: { scaleX: 0 },
  animate: { scaleX: progress },
  transition: {
    duration: 0.6,
    ease: [0.2, 0, 0, 1]
  }
};
```

### Interaction Details

#### Keyboard Navigation
- Tab/Shift+Tab: Navigate fields
- Enter: Submit/Continue (when valid)
- Escape: Cancel/Go back
- Number keys 1-5: Jump to sections (when unlocked)

#### Touch Gestures
- Swipe left/right: Navigate pages
- Pull down: Cancel wizard
- Long press: Show tooltips
- Pinch: Zoom charts (results page)

#### Validation & Feedback
- Real-time validation as user types
- Shake animation on invalid submission
- Success haptic on field completion
- Error messages appear below fields
- Progress saves automatically

### Responsive Behavior

#### Mobile (< 430px)
- Single column layout
- Full-screen wizard pages
- Bottom sheet for complex inputs
- Simplified navigation (no jumps)

#### Tablet (430px - 1024px)
- Wider form fields
- Side-by-side layout for related fields
- Floating wizard container
- Progress bar stays visible

#### Desktop (> 1024px)
- Maximum content width: 680px
- Sidebar with all sections
- Keyboard shortcuts visible
- Enhanced hover states

This wizard design follows Apple's principles while making the complex process of startup assessment feel simple, intuitive, and even delightful.