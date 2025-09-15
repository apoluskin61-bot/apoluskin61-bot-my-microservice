import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_db_conn, init_db

app = FastAPI(title="Demo Microservice")

@app.on_event("startup")
def startup():
    init_db()

class NoteIn(BaseModel):
    content: str

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/status")
def status():
    return {
        "service": "ok",
        "db_host": os.getenv("POSTGRES_HOST", "db"),
        "db": os.getenv("POSTGRES_DB", "appdb")
    }

@app.post("/data")
def create_note(note: NoteIn):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO notes(content) VALUES (%s) RETURNING id;", (note.content,))
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"id": row["id"], "content": note.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data")
def list_notes():
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
