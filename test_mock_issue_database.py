import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from main import app, IssueStatus, NewIssue, IssueResponse
from fastapi import HTTPException

@pytest.fixture
def client():
    with patch('asyncpg.connect', new_callable=AsyncMock) as mock_connect:
        mock_conn = AsyncMock()
        mock_connect.return_value = mock_conn
        
        with TestClient(app) as test_client:
            test_client.app.state.conn = mock_conn
            yield test_client

@pytest.fixture
def sample_issue():
    return {
        "id": 1,
        "key": "TEST-1",
        "name": "Test Issue",
        "status": IssueStatus.TODO.value,
        "description": "Test description"
    }

@pytest.mark.asyncio
async def test_create_new_issue(client, sample_issue):
    mock_conn = client.app.state.conn
    mock_conn.fetchrow.return_value = sample_issue
    
    new_issue_data = {
        "key": "TEST-1",
        "name": "Test Issue",
        "status": IssueStatus.TODO,
        "description": "Test description"
    }
    
    response = client.post("/issue", json=new_issue_data)
    
    assert response.status_code == 200
    assert response.json() == sample_issue
    
    mock_conn.fetchrow.assert_called_once_with(
        '''
        INSERT INTO issue(key, name, status, description)
        VALUES($1, $2, $3, $4)
        RETURNING id, key, name, status, description
        ''',
        "TEST-1", "Test Issue", "todo", "Test description"
    )

@pytest.mark.asyncio
async def test_read_issue_success(client, sample_issue):
    mock_conn = client.app.state.conn
    mock_conn.fetchrow.return_value = sample_issue
    
    response = client.get("/issue/1")
    
    assert response.status_code == 200
    assert response.json() == sample_issue
    
    mock_conn.fetchrow.assert_called_once_with(
        "SELECT id, key, name, status, description FROM issue WHERE id = $1",
        1
    )

@pytest.mark.asyncio
async def test_read_issue_not_found(client):
    mock_conn = client.app.state.conn
    mock_conn.fetchrow.return_value = None
    
    response = client.get("/issue/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Задача не найдена"

@pytest.mark.asyncio
async def test_get_issue_by_key_success(client, sample_issue):
    mock_conn = client.app.state.conn
    mock_conn.fetchrow.return_value = sample_issue
    
    response = client.get("/issue/key/TEST-1")
    
    assert response.status_code == 200
    assert response.json() == sample_issue
    
    mock_conn.fetchrow.assert_called_once_with(
        "SELECT id, key, name, status, description FROM issue WHERE key = $1",
        "TEST-1"
    )

@pytest.mark.asyncio
async def test_get_issue_by_key_not_found(client):
    mock_conn = client.app.state.conn
    mock_conn.fetchrow.return_value = None
    
    response = client.get("/issue/key/NOT-EXIST")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Задача не найдена"

@pytest.mark.asyncio
async def test_issue_response_from_record(sample_issue):
    mock_record = MagicMock()
    mock_record.__getitem__.side_effect = lambda key: sample_issue[key]
    
    response = IssueResponse.from_record(mock_record)
    
    assert response.key == sample_issue["key"]
    assert response.name == sample_issue["name"]
    assert response.status == sample_issue["status"]
    assert response.description == sample_issue["description"]
