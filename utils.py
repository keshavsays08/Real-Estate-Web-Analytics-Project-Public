# utils.py
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class CastToStr(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        return pd.DataFrame(X).astype(str)