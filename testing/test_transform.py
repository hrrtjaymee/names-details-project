import pandas as pd
import pytest
from pipelines.transform import transform, checking_count, checking_gender

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'name': ['Amanda', 'sid', 'Jacob'],
        'gender': ['F', 'm', 'x'],
        'count': [1342, 3252, 6500]
    })

def test_transform_output(sample_data):
    records = transform(sample_data)
    assert isinstance(records, pd.DataFrame)

def test_names_capitalized(sample_data):
    records  = transform(sample_data)
    assert records['name'].str.istitle().all()

def test_count_validity(sample_data):
    records = transform(sample_data)
    assert list(records.columns) == ['name', 'gender', 'count']
    # assert records['count'].dtype == int
    # assert records['count'].all() >= 0

def test_names_are_unique(sample_data):
    records = transform(sample_data)
    assert records.duplicated(subset=['name', 'gender']).sum() == 0

def test_gender_values(sample_data):
    records = transform(sample_data)
    assert records['gender'].isin(['F', 'M']).all()
