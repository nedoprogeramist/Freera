import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from main import app, NewIssue, IssueStatus

@pytest.fixture
def mock_db_connection():
    with patch('main.asyncpg.connect', new_callable=AsyncMock) as mock_connect:
        mock_conn = AsyncMock()
        mock_connect.return_value = mock_conn
        
        mock_conn.execute = AsyncMock()
        mock_conn.fetchrow = AsyncMock()
        
        yield mock_conn

@pytest.fixture
def client(mock_db_connection):
    app.state.conn = mock_db_connection
    return TestClient(app)

def test_create_new_issue(client, mock_db_connection):
    test_issue = {
        "id": 1,
        "key": "DPO-1",
        "name": "Test Issue",
        "status": "todo",
        "description": "Test description"
    }
    
    mock_db_connection.fetchrow.return_value = {
        "id": 1,
        "key": "DPO-1",
        "name": "Test Issue",
        "status": "todo",
        "description": "Test description"
    }
    
    response = client.post("/issue", json=test_issue)
    
    assert response.status_code == 200
    assert response.json()["id"] == 1
    
    mock_db_connection.execute.assert_called_once_with(
        '''
        INSERT INTO issue(key, name, status, description)
        VALUES($1, $2, $3, $4)
        RETURNING id, key, name, status, description
        ''',
        "DPO-1", "Test Issue", "todo", "Test description"
    )

def test_get_issue_by_id(client, mock_db_connection):
    mock_db_connection.fetchrow.return_value = {
        "id": 1,
        "key": "DPO-1",
        "name": "Test Issue",
        "status": "todo",
        "description": "Test description"
    }
    
    response = client.get("/issue/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == 1
    
    mock_db_connection.fetchrow.assert_called_once_with(
        'SELECT id, key, name, status, description FROM issue WHERE id = $1',
        1
    )

def test_get_issue_by_key(client, mock_db_connection):
    mock_db_connection.fetchrow.return_value = {
        "id": 1,
        "key": "DPO-1",
        "name": "Test Issue",
        "status": "todo",
        "description": "Test description"
    }
    
    response = client.get("/issue/key/DPO-1")
    
    assert response.status_code == 200
    assert response.json()["key"] == "TEST-1"
    
    mock_db_connection.fetchrow.assert_called_once_with(
        'SELECT id, key, name, status, description FROM issue WHERE key = $1',
        "TEST-1"
    )

def test_not_found(client, mock_db_connection):
    mock_db_connection.fetchrow.return_value = None
    
    response = client.get("/issue/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Задача не найдена"
