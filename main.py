from http import client
import imp
from types import new_class
from pymongo import MongoClient

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder

class Reservation(BaseModel):
    name : str
    time: int
    table_number: int
    
client = MongoClient('mongodb://localhost', 27017)

# TODO fill in database name
db = client["mini_exceed13"]

# TODO fill in collection name
collection = db["Reservation"]

app = FastAPI()


# TODO complete all endpoint.
@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name:str):
    result = collection.find({"name": name}, {"_id":0})
    res = []
    for r in result:
        res.append(r)
    print(res)
    if result != None:
        return {
            "status": "found",
            "result": result
        }
    else:
        raise HTTPException(404, f"Couldn't find reservation with name: {name}'")
    pass

@app.get("reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    pass

@app.post("/reservation")
def reserve(reservation : Reservation):
    pass

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    pass

@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    pass

