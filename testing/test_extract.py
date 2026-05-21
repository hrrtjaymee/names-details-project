import pandas as pd
import pytest
import os
from pipelines.extract import extract, extract_rows

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'test_data')

def test_extract_return_type():
    files = extract()
    assert isinstance(files, list)

def test_extract_returns_text():
    files = extract()
    assert all(f.endswith('.txt') for f in files)

def test_extract_when_no_files(test_path, monkeypatch):
    monkeypatch.setattr('pipelines.extract.DATA_PATH', test_path)
    with pytest.raises(FileNotFoundError):
        extract()

###########################################
##extract_rows()
@pytest.fixture
def valid_file(temp_path):
    f = temp_path / 'yob2014.txt'
    f.write_text('Emma,F, 23388\nLiam,M,1244\n')
    return str(temp_path), 'yob2014.txt'

@pytest.fixture
def test_extract_empty_file(temp_path):
    f = temp_path / 'yob2026.txt'
    f.write_text('name,gender,count')
    return str(temp_path), 'yob2026.txt'

@pytest.fixture
def test_header_check(temp_path):
    f = temp_path / 'yob2013.txt'
    f.write('name,gender,count\nEmman,M,3800\n')
    return str(temp_path), 'yob2013.txt'

def test_extract_rows_returns_dataframe_and_year(valid_file, monkeypatch):
    path, filename = valid_file
    monkeypatch.setattr('pipelines.extract.DATA_PATH', path)
    data, year = extract_rows(filename)
    assert isinstance(data, pd.DataFrame) 
    assert isinstance(year, int)

def test_extract_rows_empty_files(test_extract_empty_file, monkeypatch):
    path, filename = test_extract_empty_file
    monkeypatch.setattr('pipelines.extract.DATA_PATH', path)
    data, year = extract(filename)
    assert data.empty
    assert year == 0