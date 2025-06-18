import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, useScroll, useTransform } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import useAssessmentStore from '../../store/assessmentStore';
import { Button, Icon } from '../../design-system/components';
import { GaugeChart, RadarChart, ScoreBarChart } from '../../components/charts';
import { EnhancedInsights } from '../../components/EnhancedInsights';
import { EnhancedAnalysis } from '../../components/EnhancedAnalysis';
import { LLMRecommendations } from '../../components/LLMRecommendations';
import { DeepDiveAnalysis } from '../../components/DeepDiveAnalysis';
import { ComparativeAnalysis } from '../../components/ComparativeAnalysis';
import { WhatIfAnalysis } from '../../components/WhatIfAnalysis';
import { MarketInsights } from '../../components/MarketInsights';
import { CompetitorAnalysis } from '../../components/CompetitorAnalysis';
import styles from './ResultsV2.module.scss';

const ResultsV2: React.FC = () => {
  const navigate = useNavigate();
  const { results, resetAssessment, data } = useAssessmentStore();
  const [activeSection, setActiveSection] = useState(0);
  const [sidebarVisible, setSidebarVisible] = useState(() => {
    // Check localStorage and screen size
    const savedPreference = localStorage.getItem('sidebarVisible');
    const isMobile = window.innerWidth < 1024;
    return isMobile ? false : savedPreference === null ? true : savedPreference === 'true';
  });
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ container: containerRef });
  
  // Transform scroll progress to section index
  const sectionProgress = useTransform(scrollYProgress, [0, 1], [0, 11]);
  
  // Track active section based on scroll position
  useEffect(() => {
    const handleScroll = () => {
      const sections = document.querySelectorAll('[id^="section-"]');
      const scrollPosition = window.scrollY + window.innerHeight / 2;
      
      sections.forEach((section, index) => {
        const rect = section.getBoundingClientRect();
        const top = rect.top + window.scrollY;
        const bottom = top + rect.height;
        
        if (scrollPosition >= top && scrollPosition <= bottom) {
          setActiveSection(index);
        }
      });
    };
    
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Initial check
    
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      const isMobile = window.innerWidth < 1024;
      if (isMobile && sidebarVisible) {
        setSidebarVisible(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [sidebarVisible]);

  useEffect(() => {
    if (!results) {
      navigate('/');
    }
  }, [results, navigate]);

  if (!results) return null;

  // Ensure scores exist with default values
  const scores = results.scores || {
    capital: 0,
    advantage: 0,
    market: 0,
    people: 0
  };

  const sections = [
    { id: 'hero', title: 'Overview', icon: 'chart.bar' },
    { id: 'score', title: 'Success Score', icon: 'speedometer' },
    { id: 'camp', title: 'CAMP Analysis', icon: 'chart.pie' },
    { id: 'insights', title: 'Key Insights', icon: 'lightbulb' },
    { id: 'deepdive', title: 'Deep Dive', icon: 'magnifyingglass' },
    { id: 'comparative', title: 'Benchmarks', icon: 'chart.bar.xaxis' },
    { id: 'recommendations', title: 'AI Recommendations', icon: 'brain' },
    { id: 'whatif', title: 'What-If Analysis', icon: 'arrow.triangle.branch' },
    { id: 'market', title: 'Market Intelligence', icon: 'globe' },
    { id: 'competitors', title: 'Competition', icon: 'person.2' },
    { id: 'actions', title: 'Next Steps', icon: 'arrow.right.circle' }
  ];

  const successProbability = Math.round((results.successProbability || 0) * 100);
  
  const getScoreColor = (score: number) => {
    if (score >= 0.8) return styles.excellent;
    if (score >= 0.6) return styles.good;
    if (score >= 0.4) return styles.fair;
    return styles.poor;
  };
  
  const getVerdict = () => {
    if (successProbability >= 70) return 'STRONG BUY';
    if (successProbability >= 50) return 'CONDITIONAL';
    return 'HIGH RISK';
  };

  const scrollToSection = (index: number) => {
    setActiveSection(index);
    const element = document.getElementById(`section-${index}`);
    element?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const toggleSidebar = () => {
    const newValue = !sidebarVisible;
    setSidebarVisible(newValue);
    localStorage.setItem('sidebarVisible', String(newValue));
  };

  return (
    <div className={styles.container}>
      {/* Fixed Navigation */}
      <nav className={styles.nav}>
        <div className={styles.navLeft}>
          <Button 
            variant="text" 
            size="small" 
            icon={<Icon name="chevron.left" />} 
            iconPosition="left"
            onClick={() => navigate('/')}
            className={styles.backButton}
          >
            Back
          </Button>
          
          <Button
            variant="text"
            size="small"
            icon={<Icon name={sidebarVisible ? "sidebar.left" : "sidebar.right"} />}
            onClick={toggleSidebar}
            className={styles.sidebarToggle}
            aria-label={sidebarVisible ? "Hide sidebar" : "Show sidebar"}
          >
            {sidebarVisible ? "Hide" : "Menu"}
          </Button>
        </div>
        
        <div className={styles.navProgress}>
          <div className={styles.progressBar}>
            <motion.div 
              className={styles.progressFill}
              style={{ width: `${(activeSection / (sections.length - 1)) * 100}%` }}
            />
          </div>
        </div>

        <div className={styles.navActions}>
          <Button
            variant="secondary"
            size="small"
            icon={<Icon name="square.and.arrow.down" />}
            onClick={() => {
              const report = { assessmentDate: new Date().toISOString(), results };
              const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = `flash-assessment-${new Date().toISOString().split('T')[0]}.json`;
              a.click();
              URL.revokeObjectURL(url);
            }}
          >
            Export
          </Button>
        </div>
      </nav>

      {/* Side Navigation */}
      <div className={`${styles.sideNav} ${sidebarVisible ? styles.visible : ''}`}>
        {sections.map((section, index) => (
          <motion.button
            key={section.id}
            className={`${styles.navItem} ${activeSection === index ? styles.active : ''}`}
            onClick={() => scrollToSection(index)}
            whileHover={{ x: 4 }}
            whileTap={{ scale: 0.95 }}
          >
            <Icon name={section.icon} size={20} />
            <span>{section.title}</span>
          </motion.button>
        ))}
      </div>

      {/* Main Content */}
      <div className={styles.content} ref={containerRef}>
        {/* Hero Section */}
        <section id="section-0" className={styles.section}>
          <motion.div 
            className={styles.hero}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
          >
            <h1 className={styles.heroTitle}>
              Your startup has been analyzed
            </h1>
            <p className={styles.heroSubtitle}>
              We've evaluated {data.companyInfo?.companyName || 'your startup'} across multiple dimensions
              using advanced AI and industry benchmarks.
            </p>
            <motion.div 
              className={styles.scrollHint}
              animate={{ y: [0, 10, 0] }}
              transition={{ repeat: Infinity, duration: 2 }}
            >
              <Icon name="chevron.down" size={24} />
              <span>Scroll to explore</span>
            </motion.div>
          </motion.div>
        </section>

        {/* Success Score Section */}
        <section id="section-1" className={`${styles.section} ${styles.scoreSection}`}>
          <motion.div 
            className={styles.scoreContent}
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <div className={styles.scoreLeft}>
              <h2 className={styles.sectionTitle}>Success Probability</h2>
              <p className={styles.sectionDescription}>
                Based on our analysis of thousands of startups, your venture has a strong foundation for growth and success.
              </p>
              <motion.div 
                className={styles.bigScore}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.3 }}
              >
                <span className={getScoreColor(results.successProbability || 0)}>
                  {successProbability}%
                </span>
                <span className={styles.scoreLabel}>chance of success</span>
              </motion.div>
              
              <div className={styles.verdict}>
                <span className={styles.verdictLabel}>Investment Verdict</span>
                <span className={`${styles.verdictValue} ${getScoreColor(results.successProbability || 0)}`}>
                  {getVerdict()}
                </span>
              </div>

              <div className={styles.confidence}>
                <Icon name="info.circle" size={16} />
                <span>Confidence: {results.confidence || 'Moderate'}</span>
              </div>
            </div>
            
            <div className={styles.scoreRight}>
              <GaugeChart 
                value={results.successProbability || 0}
                size={400}
                label="Overall Assessment"
              />
            </div>
          </motion.div>
        </section>

        {/* CAMP Analysis Section */}
        <section id="section-2" className={`${styles.section} ${styles.campSection}`}>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className={styles.campContent}
          >
            <h2 className={styles.sectionTitle}>CAMP Framework Analysis</h2>
            <p className={styles.sectionDescription}>
              Your startup's performance across our four key pillars
            </p>
            
            {/* Debug info - remove after fixing */}
            {(scores.capital === 0 && scores.advantage === 0 && scores.market === 0 && scores.people === 0) && (
              <div style={{ background: '#fee', padding: '10px', borderRadius: '8px', marginBottom: '20px' }}>
                <p>Debug: All scores are 0</p>
                <p>Scores object: {JSON.stringify(scores)}</p>
                <p>Results object keys: {Object.keys(results).join(', ')}</p>
              </div>
            )}
            
            <div className={styles.campGrid}>
              <div className={styles.radarChart}>
                <RadarChart
                  data={[
                    { axis: 'Capital', value: scores.capital, fullName: 'Capital Efficiency' },
                    { axis: 'Advantage', value: scores.advantage, fullName: 'Competitive Advantage' },
                    { axis: 'Market', value: scores.market, fullName: 'Market Opportunity' },
                    { axis: 'People', value: scores.people, fullName: 'Team & Leadership' }
                  ]}
                  size={500}
                />
              </div>
              
              <div className={styles.scoreCards}>
                {Object.entries(scores).map(([key, value], index) => (
                  <motion.div
                    key={key}
                    className={styles.scoreCard}
                    initial={{ opacity: 0, x: 50 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <div className={styles.scoreCardHeader}>
                      <h3>{key.charAt(0).toUpperCase() + key.slice(1)}</h3>
                      <span className={getScoreColor(value)}>{Math.round(value * 100)}%</span>
                    </div>
                    <div className={styles.scoreCardBar}>
                      <motion.div 
                        className={styles.scoreCardFill}
                        initial={{ width: 0 }}
                        whileInView={{ width: `${value * 100}%` }}
                        viewport={{ once: true }}
                        transition={{ duration: 1, delay: 0.5 + index * 0.1 }}
                        style={{ background: `var(--apple-${value >= 0.7 ? 'green' : value >= 0.5 ? 'blue' : 'orange'})` }}
                      />
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        </section>

        {/* Key Insights */}
        <section id="section-3" className={`${styles.section} ${styles.insightsWrapper}`}>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className={styles.componentWrapper}
          >
            <h2 className={styles.sectionTitle}>Key Insights</h2>
            <EnhancedInsights 
              scores={scores}
              probability={results.successProbability || 0}
            />
          </motion.div>
        </section>

        {/* Deep Dive */}
        <section id="section-4" className={`${styles.section} ${styles.deepDiveWrapper}`}>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className={styles.componentWrapper}
          >
            <h2 className={styles.sectionTitle}>Deep Dive Analysis</h2>
            <DeepDiveAnalysis 
              scores={scores}
              assessmentData={data}
              insights={results.insights}
            />
          </motion.div>
        </section>

        {/* Comparative Analysis */}
        <section id="section-5" className={`${styles.section} ${styles.analysisWrapper}`}>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className={styles.componentWrapper}
          >
            <h2 className={styles.sectionTitle}>Comparative Analysis</h2>
            <ComparativeAnalysis 
              scores={scores}
              assessmentData={data}
              successProbability={results.successProbability || 0}
            />
          </motion.div>
        </section>

        {/* LLM Recommendations */}
        <section id="section-6" className={`${styles.section} ${styles.recommendationsWrapper}`}>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className={styles.componentWrapper}
          >
            <h2 className={styles.sectionTitle}>AI-Powered Recommendations</h2>
            <LLMRecommendations 
              assessmentData={data}
              basicResults={results}
            />
          </motion.div>
        </section>

        {/* What-If Analysis */}
        <section id="section-7" className={`${styles.section} ${styles.analysisWrapper}`}>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className={styles.componentWrapper}
          >
            <h2 className={styles.sectionTitle}>What-If Scenario Analysis</h2>
            <WhatIfAnalysis />
          </motion.div>
        </section>

        {/* Market Insights */}
        <section id="section-8" className={`${styles.section} ${styles.analysisWrapper}`}>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className={styles.componentWrapper}
          >
            <h2 className={styles.sectionTitle}>Market Intelligence</h2>
            <MarketInsights />
          </motion.div>
        </section>

        {/* Competitor Analysis */}
        <section id="section-9" className={`${styles.section} ${styles.analysisWrapper}`}>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className={styles.componentWrapper}
          >
            <h2 className={styles.sectionTitle}>Competitive Landscape</h2>
            <CompetitorAnalysis />
          </motion.div>
        </section>

        {/* Next Steps */}
        <section id="section-10" className={`${styles.section} ${styles.actionsSection}`}>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className={styles.actionsContent}
          >
            <h2 className={styles.sectionTitle}>What's Next?</h2>
            <p className={styles.sectionDescription}>
              Take action on your assessment results
            </p>
            
            <div className={styles.actionCards}>
              <motion.div 
                className={styles.actionCard}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Icon name="calendar" size={48} />
                <h3>Schedule Consultation</h3>
                <p>Discuss your results with our startup experts</p>
                <Button variant="primary" size="large">Book Now</Button>
              </motion.div>
              
              <motion.div 
                className={styles.actionCard}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Icon name="doc.text" size={48} />
                <h3>Detailed Report</h3>
                <p>Get a comprehensive PDF report of your analysis</p>
                <Button variant="primary" size="large">Generate PDF</Button>
              </motion.div>
              
              <motion.div 
                className={styles.actionCard}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Icon name="arrow.clockwise" size={48} />
                <h3>New Assessment</h3>
                <p>Run another analysis with updated data</p>
                <Button 
                  variant="secondary" 
                  size="large"
                  onClick={() => {
                    resetAssessment();
                    navigate('/');
                  }}
                >
                  Start Over
                </Button>
              </motion.div>
            </div>
          </motion.div>
        </section>
      </div>
    </div>
  );
};

export default ResultsV2;