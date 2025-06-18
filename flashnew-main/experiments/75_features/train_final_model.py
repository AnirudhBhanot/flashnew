#!/usr/bin/env python3
"""
Train final model with all features
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score
from catboost import CatBoostClassifier
import joblib
import json
import warnings
warnings.filterwarnings('ignore')

def main():
    print('='*60)
    print('FINAL MODEL TRAINING - ALL FEATURES')
    print('='*60)
    
    # Load complete dataset
    print('\nLoading complete dataset...')
    df = pd.read_csv('data/final_100k_dataset_complete.csv')
    print(f'Loaded {len(df)} records with {df.shape[1]} columns')
    
    # Remove text columns and problematic feature names
    exclude_cols = [
        'success', 'startup_id', 'startup_name', 
        'tagline', 'problem', 'solution', 'market', 
        'traction', 'team', 'ask', 'full_summary'
    ]
    
    # Also remove columns with special characters in names
    for col in df.columns:
        if any(char in col for char in ['$', '(', ')', '[', ']', '|']):
            exclude_cols.append(col)
    
    # Prepare features
    feature_cols = [c for c in df.columns if c not in exclude_cols]
    X = df[feature_cols]
    y = df['success']
    
    # Handle NaN values
    numeric_cols = X.select_dtypes(['float64', 'int64']).columns
    X[numeric_cols] = X[numeric_cols].fillna(X[numeric_cols].median())
    
    # Get categorical columns
    cat_features = X.select_dtypes(['object']).columns.tolist()
    
    print(f'\nFeature summary:')
    print(f'  Total features: {len(feature_cols)}')
    print(f'  Numeric features: {len(numeric_cols)}')
    print(f'  Categorical features: {len(cat_features)}')
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f'\nDataset splits:')
    print(f'  Train: {len(y_train)} ({y_train.mean():.1%} positive)')
    print(f'  Test: {len(y_test)} ({y_test.mean():.1%} positive)')
    
    # Train CatBoost with optimal parameters
    print('\nTraining CatBoost model...')
    model = CatBoostClassifier(
        iterations=1500,
        learning_rate=0.03,
        depth=7,
        l2_leaf_reg=3,
        bagging_temperature=0.7,
        random_strength=0.5,
        border_count=128,
        grow_policy='Lossguide',
        max_leaves=64,
        min_data_in_leaf=50,
        random_state=42,
        verbose=False
    )
    
    model.fit(
        X_train, y_train,
        cat_features=cat_features,
        eval_set=(X_test, y_test),
        early_stopping_rounds=100,
        verbose=200
    )
    
    # Evaluate
    train_pred = model.predict_proba(X_train)[:, 1]
    test_pred = model.predict_proba(X_test)[:, 1]
    
    train_auc = roc_auc_score(y_train, train_pred)
    test_auc = roc_auc_score(y_test, test_pred)
    test_acc = accuracy_score(y_test, (test_pred > 0.5).astype(int))
    test_f1 = f1_score(y_test, (test_pred > 0.5).astype(int))
    
    print(f'\n' + '='*60)
    print('RESULTS')
    print('='*60)
    print(f'Train AUC: {train_auc:.4f}')
    print(f'Test AUC: {test_auc:.4f}')
    print(f'Test Accuracy: {test_acc:.4f}')
    print(f'Test F1: {test_f1:.4f}')
    
    print(f'\nComparison:')
    print(f'  Baseline (45 features): 77.30% AUC')
    print(f'  Simple ensemble (75 features): 77.50% AUC')
    print(f'  With clustering: 77.69% AUC')
    print(f'  With all features: {test_auc*100:.2f}% AUC')
    print(f'  Total improvement: +{(test_auc - 0.773)*100:.2f} percentage points')
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns[model.feature_importances_ > 0],
        'importance': model.feature_importances_[model.feature_importances_ > 0]
    }).sort_values('importance', ascending=False)
    
    print(f'\nTop 20 most important features:')
    for idx, row in feature_importance.head(20).iterrows():
        print(f'  {row.feature:40s} {row.importance:6.2f}')
    
    # Save model and results
    print('\nSaving model and results...')
    joblib.dump(model, 'models/final_model_all_features.pkl')
    
    results = {
        'feature_count': len(feature_cols),
        'train_auc': float(train_auc),
        'test_auc': float(test_auc),
        'test_accuracy': float(test_acc),
        'test_f1': float(test_f1),
        'improvements': {
            'vs_baseline': float((test_auc - 0.773) * 100),
            'vs_75_features': float((test_auc - 0.775) * 100),
            'vs_clustering': float((test_auc - 0.7769) * 100)
        },
        'top_features': feature_importance.head(20).to_dict('records')
    }
    
    with open('models/final_model_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print('Model and results saved!')
    print('='*60)

if __name__ == "__main__":
    main()