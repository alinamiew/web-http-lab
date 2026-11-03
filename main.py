from fastapi import FastAPI, Response
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

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

notes = []
next_id = 1

@app.get("/notes")
def notes_list():
  return notes

@app.post("/notes", status_code=201)
def note_create(data: NoteCreate):
  global next_id  
  note = {
    "id" : next_id,
    "title": data.title,
    "content": data.content,
  }
  notes.append(note)
  next_id +=1
  return note
  


    
  
  
