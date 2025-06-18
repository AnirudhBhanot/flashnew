"""Base model interface for ML core components"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd

class BaseMLModel(ABC):
    """Base class for all ML models in the system"""
    
    @abstractmethod
    def predict(self, features: pd.DataFrame) -> Dict[str, Any]:
        """Make predictions on input features"""
        pass
    
    @abstractmethod
    def load_model(self, model_path: str) -> bool:
        """Load a trained model from disk"""
        pass
    
    @abstractmethod
    def save_model(self, model_path: str) -> bool:
        """Save the current model to disk"""
        pass