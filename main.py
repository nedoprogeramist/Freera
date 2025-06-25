from fastapi import FastAPI
import asyncio
import asyncpg
from pydantic import BaseModel
app = FastAPI()

conn = await asyncpg.connect(user='posstgres', password='password', 'database='fastapi-postgres', host='127.0.0.1')

async def createTable(conn):
	
	with open(create_table.sql, 'r') as file:
        sql_commands = file.read()
    
    await conn.execute(sql_commands)

asyncio.run(createTable())

class NewIssuse(BaseModel):
	key str
	name str
	status issuse_status
	description str
    
@app.post("/issuse")
async def createNewIssuse(new_issuse: NewIssuse):
	
	await conn.execute('''
        INSERT INTO issuse(key, name, status, description) VALUES($1, $2, $3, $4,)
    ''',
    new_issuse.key, new_issuse.name, new_issuse.status, new_issuse.description )
	return {"message" : "Задача добавленна"}

@app.get("/issuse/{id}", response_model=NewIssuse)
async def getIssueById(id: int):
	
	 try:
        row = await conn.fetchrow('SELECT * FROM issuse WHERE key = $1', id)
        if row is None:
            return None
        return NewIssuse(**row)
	
@app.get("/issuse/key/{key}", response_model=NewIssuse)
async def getIssueByKey(key: str):
    try:
        row = await conn.fetchrow('SELECT * FROM issuse WHERE key = $1', key)
        if row is None:
            return None
        return NewIssuse(**row)
