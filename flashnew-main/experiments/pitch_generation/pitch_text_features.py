#!/usr/bin/env python3
"""
Extract features from pitch deck text using NLP techniques
"""
import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import warnings
warnings.filterwarnings('ignore')

class PitchTextFeatureExtractor:
    def __init__(self):
        self.vectorizer = None
        self.svd = None
        
        # Key phrases that indicate quality
        self.success_indicators = [
            r'\$[\d\.]+[MBK]?\s*(ARR|MRR|revenue)',
            r'\d+%\s*(growth|retention|margin)',
            r'\d+\s*(customers|users|clients)',
            r'patent|proprietary\stechnology',
            r'series\s[A-D]|successful\sexit',
            r'product-market\sfit',
            r'\d+x\s*(improvement|return|ROI)',
        ]
        
        self.failure_indicators = [
            r'revolutionary|disrupt|paradigm\sshift',
            r'unlimited|massive\spotential',
            r'blockchain|AI|machine\slearning(?!\s*to\s*\w+)',  # Without specific use
            r'passionate|dedicated|changing\sthe\sworld',
            r'preparing|planning|expecting',
            r'various|multiple|several(?!\s*\d+)',
            r'accelerate\sgrowth|dominate',
        ]
        
        self.clarity_indicators = [
            r'we\shelp\s\w+\sachieve',
            r'by\sreducing|by\sautomating|by\simplifying',
            r'costs?\s\$\d+|saves?\s\d+\shours',
            r'specifically|exactly|precisely',
            r'our\splatform|our\ssolution|our\sproduct',
        ]
    
    def extract_text_features(self, df):
        """Extract various text-based features from pitch summaries"""
        
        print("Extracting text features from pitch decks...")
        
        # Get the pitch text
        pitch_text = df['full_summary'].fillna('')
        
        # 1. Basic text statistics
        text_features = pd.DataFrame()
        text_features['pitch_length'] = pitch_text.str.len()
        text_features['pitch_word_count'] = pitch_text.str.split().str.len()
        text_features['pitch_sentence_count'] = pitch_text.str.count(r'[.!?]+')
        text_features['avg_words_per_sentence'] = (
            text_features['pitch_word_count'] / 
            (text_features['pitch_sentence_count'] + 1)
        )
        
        # 2. Success/failure indicator counts
        for pattern in self.success_indicators:
            col_name = f"has_{pattern[:20].replace(' ', '_').replace('\\', '')}"
            text_features[col_name] = pitch_text.str.contains(pattern, regex=True).astype(int)
        
        text_features['success_indicator_count'] = text_features[[
            col for col in text_features.columns if col.startswith('has_')
        ]].sum(axis=1)
        
        # Count failure indicators
        failure_count = 0
        for pattern in self.failure_indicators:
            failure_count += pitch_text.str.contains(pattern, regex=True).astype(int)
        text_features['failure_indicator_count'] = failure_count
        
        # 3. Clarity and specificity scores
        clarity_count = 0
        for pattern in self.clarity_indicators:
            clarity_count += pitch_text.str.contains(pattern, regex=True).astype(int)
        text_features['clarity_score'] = clarity_count
        
        # 4. Sentiment and confidence
        text_features['uses_numbers'] = pitch_text.str.contains(r'\d+').astype(int)
        text_features['uses_metrics'] = pitch_text.str.contains(
            r'ARR|MRR|CAC|LTV|ROI|growth\srate|retention|churn', 
            case=False
        ).astype(int)
        
        # 5. Section completeness
        sections = ['TAGLINE', 'PROBLEM', 'SOLUTION', 'MARKET', 'TRACTION', 'TEAM', 'ASK']
        for section in sections:
            text_features[f'has_{section.lower()}'] = pitch_text.str.contains(
                f'\\[{section}\\]', regex=True
            ).astype(int)
        
        text_features['section_completeness'] = text_features[[
            f'has_{s.lower()}' for s in sections
        ]].sum(axis=1) / len(sections)
        
        # 6. Red flags detection
        text_features['has_red_flags'] = pitch_text.str.contains(
            r'\[RED FLAGS\]', regex=True
        ).astype(int)
        text_features['has_strengths'] = pitch_text.str.contains(
            r'\[STRENGTHS\]', regex=True
        ).astype(int)
        
        # 7. Specific metric extraction
        # Extract ARR if mentioned
        arr_matches = pitch_text.str.extract(r'\$(\d+\.?\d*)[MK]?\s*ARR')
        text_features['mentioned_arr'] = pd.to_numeric(arr_matches[0], errors='coerce').fillna(0)
        
        # Extract growth rate if mentioned
        growth_matches = pitch_text.str.extract(r'(\d+)%\s*(?:YoY\s*)?growth')
        text_features['mentioned_growth_rate'] = pd.to_numeric(growth_matches[0], errors='coerce').fillna(0)
        
        # Extract customer count if mentioned
        customer_matches = pitch_text.str.extract(r'(\d+)\s*(?:enterprise\s*)?customers')
        text_features['mentioned_customers'] = pd.to_numeric(customer_matches[0], errors='coerce').fillna(0)
        
        # 8. Language quality score
        text_features['language_quality_score'] = (
            text_features['clarity_score'] * 2 +
            text_features['success_indicator_count'] -
            text_features['failure_indicator_count'] +
            text_features['uses_metrics'] * 2 +
            text_features['section_completeness'] * 5
        ) / 10
        
        # 9. TF-IDF features (top terms)
        print("Computing TF-IDF features...")
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=0.01,
            max_df=0.95
        )
        
        tfidf_matrix = self.vectorizer.fit_transform(pitch_text)
        
        # Reduce dimensionality with SVD
        self.svd = TruncatedSVD(n_components=10, random_state=42)
        tfidf_reduced = self.svd.fit_transform(tfidf_matrix)
        
        # Add as features
        for i in range(10):
            text_features[f'pitch_topic_{i}'] = tfidf_reduced[:, i]
        
        # 10. Consistency check with actual metrics
        text_features['arr_consistency'] = np.where(
            (text_features['mentioned_arr'] > 0) & (df['annual_revenue_run_rate'] > 0),
            1 - np.abs(text_features['mentioned_arr'] - df['annual_revenue_run_rate'] / 1e6) / 
            (df['annual_revenue_run_rate'] / 1e6 + 1),
            0.5
        )
        
        print(f"Extracted {len(text_features.columns)} text features")
        
        return text_features
    
    def get_feature_importance_hints(self):
        """Return expected important features"""
        return {
            'language_quality_score': 'Overall pitch quality',
            'success_indicator_count': 'Number of positive signals',
            'failure_indicator_count': 'Number of red flags',
            'clarity_score': 'How clearly the pitch communicates',
            'uses_metrics': 'Whether concrete metrics are mentioned',
            'arr_consistency': 'Consistency between claims and data',
            'pitch_topic_0': 'Main topic from text analysis'
        }

def main():
    print("="*60)
    print("Pitch Text Feature Extraction")
    print("="*60)
    
    # Load data with pitches
    print("\nLoading data with pitch decks...")
    df = pd.read_csv('data/final_100k_dataset_with_pitches.csv')
    print(f"Loaded {len(df)} startups with pitch decks")
    
    # Extract text features
    extractor = PitchTextFeatureExtractor()
    text_features = extractor.extract_text_features(df)
    
    # Combine with original data
    df_final = pd.concat([df, text_features], axis=1)
    
    # Save final dataset
    output_path = 'data/final_100k_dataset_complete.csv'
    df_final.to_csv(output_path, index=False)
    print(f"\nSaved complete dataset to {output_path}")
    
    # Show feature statistics
    print("\n" + "="*60)
    print("Text Feature Statistics")
    print("="*60)
    
    print("\nFeature correlations with success:")
    correlations = {}
    for col in text_features.columns:
        if text_features[col].dtype in ['int64', 'float64']:
            corr = text_features[col].corr(df['success'])
            correlations[col] = corr
    
    # Sort by absolute correlation
    sorted_corrs = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
    
    print("\nTop 15 most predictive text features:")
    for feat, corr in sorted_corrs[:15]:
        print(f"  {feat:35s} {corr:+.4f}")
    
    print("\n" + "="*60)
    print(f"Total features in final dataset: {df_final.shape[1]}")
    print("  - Original features: 80")
    print("  - Cluster features: 22")
    print(f"  - Text features: {len(text_features.columns)}")
    print("  - Pitch content: 8")
    print("="*60)

if __name__ == "__main__":
    main()