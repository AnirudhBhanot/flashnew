"""
FLASH ML Core Package
Advanced machine learning models for startup evaluation
"""

__version__ = "2.0.0"

# Import key classes for easy access
from .models.dna_analyzer import DNAPatternAnalyzer
# from .serving.model_loader import ModelLoader, AdvancedModelOrchestrator

__all__ = [
    'DNAPatternAnalyzer'
]