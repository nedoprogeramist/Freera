from fastapi import FastAPI
import asyncio
import asyncpg
from pydantic import BaseModel
app = FastAPI()

conn = await asyncpg.connect(user='posstgres', password='password', 'database='fastapi-postgres', host='127.0.0.1')

async def createTable(conn):
	await conn.execute('''
        CREATE TYPE status AS ENUM (
        'TODO', 
        'In Progress', 
        'Review',
        'QA',
        'Done',
        'Closed'
        )
    ''')
    
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS issuse(
            id int PRIMARY KEY AUTO_INCREMENT,
            key str,
            name str,
            status status,
            description str
        )
    ''')

asyncio.run(createTable())

class NewIssuse(BaseModel):
	key str,
    name str,
    status status,
    description str
    
@app.post("/issuse")
async def createNewIssuse(new_issuse: NewIssuse):
	
	await conn.execute('''
        INSERT INTO issuse(key, name, status, description) VALUES($1, $2, $3, $4,)
    ''',new_issuse.key, new_issuse.name, new_issuse.status, new_issuse.description )
	return {"message" : "Задача добавленна"}

@app.get("/issuse/{id}")
async def getIssueById(id: int):
	
	i = id
	row = await conn.fetchrow('SELECT * FROM issuse WHERE id = $1', i)
	return row
	
@app.get("/issuse/key/{key}")
async def get_issue_by_key(key: str):
	
	i = key
	row = await conn.fetchrow('SELECT * FROM issuse WHERE key = $1', i)
	return row
