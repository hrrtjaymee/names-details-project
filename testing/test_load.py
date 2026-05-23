import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from pipelines.load import load, load_names, load_details

@pytest.fixture
def mock_cursor():
    return MagicMock()

@pytest.fixture
def mock_conn(mock_cursor):
    conn = MagicMock()
    conn.cursor.return_value = mock_cursor
    return conn

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'name':['Hazel', 'Bryce'],
        'gender': ['F', 'M'],
        'count': [24123, 323]
    })

@pytest.fixture
def sample_female():
    return pd.Series({'name': 'Hazel', 'gender': 'F', 'count': 12399})

@pytest.fixture
def sample_male():
    return pd.Series({'name': 'Bryce', 'gender': 'M', 'count': 15399})

#TEST load_names

def test_load_names_returns_id(mock_cursor, sample_female):
    mock_cursor.fetchone.return_value = ('a8098c1a-f86e-11da-bd1a-00112444be1e')
    result = load_names(sample_female, mock_cursor)
    assert result == 'a8098c1a-f86e-11da-bd1a-00112444be1e'

def test_load_names_executes_query(mock_cursor, sample_female):
    mock_cursor.fetchone.return_value = ('a8098c1a-f86e-11da-bd1a-00112444be1e')
    load_names(sample_female, mock_cursor)
    assert mock_cursor.execute.called

def test_load_names_passes_correct_values(mock_cursor, sample_female):
    mock_cursor.fetchone.return_value = ('a8098c1a-f86e-11da-bd1a-00112444be1e')
    load_names(sample_female, mock_cursor)
    args = mock_cursor.execute.call_args[0]
    assert ('Hazel', 'F') in args

#TEST load_details()

def test_load_details_execute_query(mock_cursor):
    load_details('a8098c1a-f86e-11da-bd1a-00112444be1e', 1899, mock_cursor, 2014)
    assert mock_cursor.execute.called

def test_load_details_correct_values(mock_cursor):
    name_id = 'a8098c1a-f86e-11da-bd1a-00112444be1e'
    load_details(name_id, 18400, mock_cursor, 2014)
    args = mock_cursor.execute.call_args[0]
    assert (name_id, 2014, 18400) in args

def test_load_commits_on_success(mock_conn, mock_cursor, sample_data):
    mock_cursor.fetchone.return_value = ('a8098c1a-f86e-11da-bd1a-00112444be1e')
    load(sample_data, mock_conn, 2014)
    mock_conn.commit.assert_called_once()

def test_load_skips_rows_on_failure(mock_conn, mock_cursor, sample_data):
    mock_cursor.fetchone.side_effect = [
        ('a8098c1a-f86e-11da-bd1a-00112444be1e'),
        Exception('DB error')
    ]
    load(sample_data, mock_conn, 2014)
    mock_conn.commit.assert_called_once()

def test_load_processes_all_rows(mock_conn, mock_cursor, sample_data):
    mock_cursor.fetchone.return_value = ('a8098c1a-f86e-11da-bd1a-00112444be1e')
    load(sample_data, mock_conn, 2014)
    assert mock_cursor.execute.call_count == 4 # 2 queries * 2 rows

def test_load_skips_invalid_rows(mock_conn, mock_cursor, sample_data):
    mock_cursor.fetchone.side_effect = [
        ('a8098c1a-f86e-11da-bd1a-00112444be1e'),
        Exception('DB error')
    ]

    load(sample_data, mock_conn, 2014)
    mock_conn.commit.assert_called_once()

