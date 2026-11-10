from fastapi import FastAPI, Response,HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
import os 
database_url = os.environ["DATABASE_URL"]

postgres_dll_directory = os.add_dll_directory(r"C:\Program Files\PostgreSQL\18\bin")
import psycopg 

from psycopg.rows import dict_row



app = FastAPI(title="Notes API", version="0.1.0")

@app.get("/hello")
def hello():
  return{"message": "Hello from Notes API"}

@app.get("/health")
def health():
  return {"status": "ok"}

class NoteCreate(BaseModel):
  title: str = Field(min_length = 1, max_length = 80)
  content: str= Field(min_length = 1, max_length = 500)



@app.get("/notes")
def notes_list():
  with psycopg.connect(database_url, row_factory=dict_row) as conn:
    cursor = conn.execute("SELECT id, title,content FROM notes")
    rows = cursor.fetchall()
  return rows

@app.post("/notes", status_code=201)
def note_create(data: NoteCreate):
  with  psycopg.connect(database_url, row_factory=dict_row) as conn:
    cursor = conn.execute("INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id, title, content", (data.title, data.content))
    note = cursor.fetchone()
  return note

@app.get("/notes/{note_id}")
def notes_id(note_id: int):
  with  psycopg.connect(database_url, row_factory=dict_row) as conn:
    cursor = conn.execute("SELECT id, title, content FROM notes WHERE id = %s", (note_id,))
    note = cursor.fetchone()
  if note is None:
    raise HTTPException(status_code=404, detail="Note not found") 
  return note    
      
      
  


    
  
  
