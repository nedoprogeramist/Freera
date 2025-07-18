from fastapi import FastAPI, HTTPException
import asyncpg
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: initialize resources")
    app.state.conn = await asyncpg.connect(
		user='postgres',
		password='password',
		database='fastapi-postgres',
        host='127.0.0.1'
		)    
    yield
    print("Shutting down: cleanup resources")
    await app.state.conn.close()

class IssueStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    QA = "qa"
    DONE = "done"
    CLOSED = "closed"

class NewIssue(BaseModel):
    key: str
    name: str
    status: IssueStatus
    description: str

class IssueResponse(NewIssue):
    @classmethod
    def from_record(cls, record):
        return cls(
            id=record["id"],
            key=record["key"],
            name=record["name"],
            status=record["status"],
            description=record["description"]
        )
    
@app.post("/issue", response_model=IssueResponse)
async def create_new_issue(new_issue: NewIssue):
    conn = app.state.conn
    record = await conn.fetchrow(
        '''
        INSERT INTO issue(key, name, status, description)
        VALUES($1, $2, $3, $4)
        RETURNING id, key, name, status, description
        ''',
        new_issue.key, new_issue.name, new_issue.status.value, new_issue.description
    )
    return IssueResponse.from_record(record)

@app.get("/issue/{id}", response_model=IssueResponse)
async def read_issue(id: int):
    try:
        conn = app.state.conn
        query = """SELECT id, key, name, status, description FROM issue WHERE id = $1 """
        row = await conn.fetchrow(query,id)
		
        if not row:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return IssueResponse.from_record(row)
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

@app.get("/issue/key/{key}", response_model=IssueResponse)
async def get_issue_by_key(key: str):
    try:
        conn = app.state.conn
        query = """SELECT id, key, name, status, description FROM issue WHERE key = $1 """
        row = await conn.fetchrow(query, key)
		
        if not row:
             raise HTTPException(status_code=404, detail="Задача не найдена")
        return IssueResponse.from_record(record)
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
