"""
Data Preprocessing Service
Handles data validation, cleaning, missing value imputation, outlier clipping,
feature engineering, and scaling.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any, Optional
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

from backend.utils.data_generator import FEATURE_COLUMNS, TARGET_COLUMN
from backend.ml.feature_engineering import add_engineered_features, ENGINEERED_FEATURE_NAMES

# Valid numeric bounds for physical features
FEATURE_BOUNDS = {
    "latitude": (-90.0, 90.0),
    "longitude": (-180.0, 180.0),
    "rainfall_24h": (0.0, 1000.0),
    "rainfall_7d": (0.0, 3000.0),
    "rainfall_intensity": (0.0, 200.0),
    "temperature": (-40.0, 60.0),
    "humidity": (0.0, 100.0),
    "elevation": (-100.0, 9000.0),
    "slope": (0.0, 90.0),
    "aspect": (0.0, 360.0),
    "terrain_roughness": (0.0, 2.0),
    "curvature": (-5.0, 5.0),
    "ndvi": (-1.0, 1.0),
    "ndwi": (-1.0, 1.0),
    "soil_moisture": (0.0, 1.0),
    "vegetation_index": (-1.0, 1.0),
    "historical_landslides": (0, 100),
    "previous_landslide": (0, 1),
}


class PreprocessingService:
    def __init__(self, scaler_path: Optional[Path] = None):
        self.scaler: Optional[StandardScaler] = None
        self.scaler_path = scaler_path
        self.all_feature_names = FEATURE_COLUMNS + ENGINEERED_FEATURE_NAMES
        if scaler_path and scaler_path.exists():
            self.load_scaler(scaler_path)

    def validate_and_sanitize_record(self, record: Dict[str, Any]) -> Dict[str, float]:
        """
        Validates individual input record against expected physical bounds and data types,
        replacing missing values with sensible defaults.
        """
        defaults = {
            "latitude": 20.0,
            "longitude": 80.0,
            "rainfall_24h": 10.0,
            "rainfall_7d": 40.0,
            "rainfall_intensity": 2.0,
            "temperature": 25.0,
            "humidity": 65.0,
            "elevation": 500.0,
            "slope": 15.0,
            "aspect": 180.0,
            "terrain_roughness": 0.3,
            "curvature": 0.0,
            "ndvi": 0.5,
            "ndwi": 0.0,
            "soil_moisture": 0.4,
            "vegetation_index": 0.5,
            "historical_landslides": 0,
            "previous_landslide": 0,
        }

        sanitized = {}
        for col in FEATURE_COLUMNS:
            val = record.get(col, defaults[col])
            try:
                num_val = float(val) if val is not None and not np.isnan(float(val)) else defaults[col]
            except (ValueError, TypeError):
                num_val = defaults[col]

            # Clip within physical domain bounds
            low, high = FEATURE_BOUNDS.get(col, (-np.inf, np.inf))
            num_val = max(low, min(high, num_val))
            sanitized[col] = num_val

        return sanitized

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans training/evaluation DataFrame:
        - Drops duplicates
        - Imputes missing numeric values with median
        - Clips outliers to plausible domain limits
        """
        cleaned = df.copy()
        cleaned = cleaned.drop_duplicates()

        # Fill missing values
        for col in FEATURE_COLUMNS:
            if col in cleaned.columns:
                cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
                if cleaned[col].isnull().any():
                    cleaned[col] = cleaned[col].fillna(cleaned[col].median())
                # Clip outliers
                if col in FEATURE_BOUNDS:
                    low, high = FEATURE_BOUNDS[col]
                    cleaned[col] = cleaned[col].clip(lower=low, upper=high)

        if TARGET_COLUMN in cleaned.columns:
            cleaned[TARGET_COLUMN] = cleaned[TARGET_COLUMN].fillna(0).astype(int)

        return cleaned

    def prepare_training_data(
        self,
        df: pd.DataFrame,
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str]]:
        """
        Full training preprocessing pipeline:
        1. Clean data
        2. Feature engineer
        3. Train-test split
        4. Fit and apply StandardScaler
        """
        cleaned_df = self.clean_dataframe(df)
        featured_df = add_engineered_features(cleaned_df)

        X = featured_df[self.all_feature_names]
        y = featured_df[TARGET_COLUMN].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        if self.scaler_path:
            self.save_scaler(self.scaler_path)

        return X_train_scaled, X_test_scaled, y_train, y_test, self.all_feature_names

    def transform_single(self, record: Dict[str, Any]) -> Tuple[np.ndarray, pd.DataFrame]:
        """
        Transforms a single inference record:
        Validates -> Engineers -> Scales -> Returns 1xD array and original feature DataFrame.
        """
        sanitized = self.validate_and_sanitize_record(record)
        engineered = add_engineered_features(sanitized)
        df_row = pd.DataFrame([engineered])[self.all_feature_names]

        if self.scaler is not None:
            scaled_array = self.scaler.transform(df_row)
        else:
            scaled_array = df_row.values

        return scaled_array, df_row

    def save_scaler(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.scaler, path)

    def load_scaler(self, path: Path):
        if path.exists():
            self.scaler = joblib.load(path)
