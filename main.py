from fastapi import FastAPI, HTTPException
import asyncpg
from pydantic import BaseModel
from enum import Enum
from typing import Optional

app = FastAPI()

class IssueStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    Review = "Review"
    QA = "qa"
    Done = "done"
    CLOSED = "closed"

class NewIssue(BaseModel):
    key: str
    name: str
    status: IssueStatus
    description: str

class IssueResponse(NewIssue):
    id: int

@app.on_event("startup")
async def startup_event():
    app.state.conn = await asyncpg.connect(
        user='postgres',
        password='password',
        database='fastapi-postgres',
        host='127.0.0.1'
    )

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.conn.close()

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
    return dict(record)

@app.get("/issue/{id}", response_model=IssueResponse)
async def read_issue(id: int):
    conn = app.state.conn
    row = await conn.fetchrow(
        'SELECT id, key, name, status, description FROM issue WHERE id = $1',
        id
    )
    
    if not row:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return dict(row)

@app.get("/issue/key/{key}", response_model=IssueResponse)
async def get_issue_by_key(key: str):
    conn = app.state.conn
    row = await conn.fetchrow(
        'SELECT id, key, name, status, description FROM issue WHERE key = $1',
        key
    )
    
    if not row:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return dict(row)
