import pytest
import pandas as pd
from backend.utils.data_generator import (
    generate_synthetic_dataset,
    generate_single_demo_record,
    FEATURE_COLUMNS,
    TARGET_COLUMN
)


def test_synthetic_dataset_generation():
    df = generate_synthetic_dataset(n_samples=50, random_seed=123)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 50
    for col in FEATURE_COLUMNS:
        assert col in df.columns
    assert TARGET_COLUMN in df.columns
    assert set(df[TARGET_COLUMN].unique()).issubset({0, 1})


def test_single_demo_record_generation():
    record = generate_single_demo_record("high")
    assert isinstance(record, dict)
    assert "rainfall_24h" in record
    assert "slope" in record
    assert "soil_moisture" in record
    assert record["rainfall_24h"] > 0
    assert record["slope"] > 0


def test_demo_record_hazard_profiles():
    profiles = ["low", "moderate", "high", "critical", "random"]
    for prof in profiles:
        rec = generate_single_demo_record(prof)
        assert isinstance(rec, dict)
        assert rec["slope"] >= 0
