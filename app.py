from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import datetime

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

appDB = "weight_tracker.db"

@app.get("/")
async def read_root():
    return {"message": "Welcome to the weight tracker!"}

@app.get("/id/{id}/data")
async def get_data(id: int):
    connection = sqlite3.connect(appDB)
    cursor = connection.cursor()
    res = cursor.execute("SELECT * from weight")
    data = res.fetchall()
    connection.close()
    return {"message": "Weight tracking data", "data": data}

@app.post("/id/{id}/log_weight")
async def log_weight(id: int, weight: float):
    try:
        current_timestamp = datetime.datetime.now()
        data = (id, weight, current_timestamp)
        query = """INSERT INTO weight (id, weight, timestamp) VALUES (?, ?, ?)"""
        connection = sqlite3.connect(appDB)
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        connection.close()
        return {"message": "Logging weight tracking data", "data": data}
    except Exception as e:
        return {"error": str(e)}