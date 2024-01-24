from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import datetime
from pydantic import BaseModel


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


class Weight(BaseModel):
    id: int
    weight: float
    timestamp: datetime.datetime


class User(BaseModel):
    id: int
    name: str
    height: float


class Bmi(BaseModel):
    id: int
    weight: float
    height: float
    bmi: float


@app.get("/")
async def read_root():
    return {"message": "Welcome to the weight tracker!"}


@app.post("/id/{id}/log_weight")
async def log_weight(id: int, weight: float):
    try:
        current_timestamp = datetime.datetime.now()
        data = (id, weight, current_timestamp)
        query = "INSERT INTO weight (id, weight, timestamp) VALUES (?, ?, ?)"
        connection = sqlite3.connect(appDB)
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        connection.close()
        return {"message": "Logging weight tracking data", "data": data}
    except Exception as e:
        return {"error": str(e)}


@app.get("/id/{id}/latest_weight", response_model=Weight)
async def get_latest_weight(id: int):
    try:
        query = "SELECT * FROM weight WHERE id = ? ORDER BY timestamp DESC LIMIT 1"
        connection = sqlite3.connect(appDB)
        cursor = connection.cursor()
        result = cursor.execute(query, (id,))
        data = result.fetchone()
        connection.close()
        weight_data = Weight(id=data[0], weight=data[1], timestamp=data[2] ) 
        return weight_data.model_dump()
    except Exception as e:
        return {"error": str(e)}


@app.get("/id/{id}/user", response_model=User)
async def get_user(id: int):
    try:
        query = "SELECT * FROM user WHERE id = ?"
        connection = sqlite3.connect(appDB)
        cursor = connection.cursor()
        result = cursor.execute(query, (id,))
        data = result.fetchone()
        connection.close()
        user_data = User(id=data[0], name=data[1], height=data[2] ) 
        print(user_data.model_dump().get("name"))
        return user_data.model_dump()
    except Exception as e:
        return {"error": str(e)}


@app.get("/id/{id}/bmi", response_model=Bmi)
async def get_bmi(id: int):
    try:
        latest_weight = await get_latest_weight(id)
        weight = latest_weight.get("weight")
        user = await get_user(id)
        height = user.get("height")
        bmi = weight/(height*height)
        bmi_data = Bmi(id=id, weight=weight, height=height, bmi=bmi)
        return bmi_data.model_dump()
    except Exception as e:
        return {"error": str(e)}

    
@app.post("/id/{id}/update_user")
async def update_user(id: int, name: str, height: float):
    try:
        data = (name, height, id)
        query = """
                UPDATE user 
                SET name = ?, height = ?
                WHERE id = ?;
                """
        connection = sqlite3.connect(appDB)
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        connection.close()
        return {"message": "Updated user data", "data": data}
    except Exception as e:
        return {"error": str(e)}