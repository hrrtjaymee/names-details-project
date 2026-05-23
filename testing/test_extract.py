import pandas as pd
import pytest
import os
from pipelines.extract import extract, extract_rows

def test_extract_return_type():
    files = extract()
    assert isinstance(files, list)

def test_extract_returns_text():
    files = extract()
    assert all(f.endswith('.txt') for f in files)

def test_extract_when_no_files(tmp_path, monkeypatch):
    monkeypatch.setattr('pipelines.extract.DATA_PATH', tmp_path)
    with pytest.raises(FileNotFoundError):
        extract()

###########################################
##extract_rows()
@pytest.fixture
def valid_file(tmp_path):
    f = tmp_path / 'yob2014.txt'
    f.write_text('Emma,F, 23388\nLiam,M,1244\n')
    return str(tmp_path), 'yob2014.txt'

@pytest.fixture
def empty_file(tmp_path):
    f = tmp_path / 'yob2026.txt'
    f.write_text('')
    return str(tmp_path), 'yob2026.txt'

@pytest.fixture
def with_header_no_data(tmp_path):
    f = tmp_path / 'yob2013.txt'
    f.write_text('name,gender,count\n')
    return str(tmp_path), 'yob2013.txt'

@pytest.fixture
def header_check(tmp_path):
    f = tmp_path / 'yob2013.txt'
    f.write_text('name,gender,count\nEmman,M,3800\n')
    return str(tmp_path), 'yob2013.txt'

def test_extract_rows_returns_dataframe_and_year(valid_file, monkeypatch):
    path, filename = valid_file
    monkeypatch.setattr('pipelines.extract.DATA_PATH', path)
    data, year = extract_rows(filename)
    assert isinstance(data, pd.DataFrame) 
    assert isinstance(year, int)

def test_extract_rows_empty_files(empty_file, monkeypatch):
    path, filename = empty_file
    monkeypatch.setattr('pipelines.extract.DATA_PATH', path)
    data, year = extract_rows(filename)
    assert data.empty
    assert year == 0

def test_extract_rows_skips_header_row(header_check, monkeypatch):
    path, filename = header_check
    monkeypatch.setattr('pipelines.extract.DATA_PATH', path)
    data, year =  extract_rows(filename)
    assert 'name' not in data['name'].values
    assert len(data) == 1

def test_extract_rows_with_header_no_data(with_header_no_data, monkeypatch):
    path, filename = with_header_no_data
    monkeypatch.setattr('pipelines.extract.DATA_PATH', path)
    data, year = extract_rows(filename)
    assert isinstance(data, pd.DataFrame)
    assert year == 0