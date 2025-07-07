import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app, NewIssuse

client = TestClient(app)

@pytest.fixture
def mock_database():
    """Fixture to mock database connection and methods."""
    with patch("app.conn") as mock_conn:
        yield mock_conn

def test_create_new_issuse(mock_database):
    mock_database.execute = AsyncMock()

    response = client.post("/issuse", json={
        "key": "DPO-873",
        "name": "Test Issue",
        "status": "TODO",
        "description": "Test description"
    })

    assert response.status_code == 200
    assert response.json() == {"message": "Задача добавленна"}
    
    mock_database.execute.assert_called_once_with(
        '''
        INSERT INTO issuse(key, name, status, description) VALUES($1, $2, $3, $4)
        ''',
        "DPO-873", "Test Issue", "TODO", "Test description"
    )

def test_get_issue_by_id(mock_database):
    mock_database.fetchrow = AsyncMock(return_value={
        "key": "DPO-873",
        "name": "Test Issue",
        "status": "TODO",
        "description": "Test description"
    })

    response = client.get("/issuse/1")

    assert response.status_code == 200
    issue = NewIssuse(**response.json())
    
    assert issue.key == "DPO-873"
    assert issue.name == "Test Issue"
    assert issue.status == "TODO"
    assert issue.description == "Test description"

def test_get_issue_by_key(mock_database):
    mock_database.fetchrow = AsyncMock(return_value={
        "key": "DPO-873",
        "name": "Test Issue",
        "status": "TODO",
        "description": "Test description"
    })

    response = client.get("/issuse/key/DPO-873")

    assert response.status_code == 200
    issue = NewIssuse(**response.json())
    
    assert issue.key == "DPO-873"
    assert issue.name == "Test Issue"
    assert issue.status == "TODO"
    assert issue.description == "Test description"
