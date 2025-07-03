from fastapi import FastAPI
import asyncio
import asyncpg
from pydantic import BaseModel
from sql-comands import migrations
app = FastAPI()

async def main():  
  conn = await asyncpg.connect(user='posstgres', password='password', database='fastapi-postgres', host='127.0.0.1')
  return conn
  
asyncio.run(main())

async def createTable(conn):
    try:
      for command in migrations:
        await conn.execute(command)
    except Exception as e:
        print(f"Ошибка при выполнении миграции: {e}")
    finally:
        await conn.close()

asyncio.run(createTable())

class NewIssuse(BaseModel):
	key: str
	name: str
	status: issuse_status
	description: str
    
@app.post("/issuse")
async def createNewIssuse(new_issuse: NewIssuse):
	
	await conn.execute('''
        INSERT INTO issuse(key, name, status, description) VALUES($1, $2, $3, $4,)
    ''',
    new_issuse.key, new_issuse.name, new_issuse.status, new_issuse.description )
	return {"message" : "Задача добавленна"}

@app.get("/issuse/{id}")
async def read_issuse(id: str):
    row = await conn.fetchrow('SELECT * FROM issuse WHERE key = $1', id)
    if row:
        return dict(row)
    return {"error": "Задача не найдена"}

@app.get("/issuse/key/{key}", response_model=NewIssuse)
async def getIssueByKey(key: str):
    try:
        row = await conn.fetchrow('SELECT * FROM issuse WHERE key = $1', key)
        if row is None:
            return None
        return NewIssuse(**row)
    except SomeException as e:
      print(f"Произошла ошибка: {e}")
    finally:
      pass
