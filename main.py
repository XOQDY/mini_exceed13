from pymongo import MongoClient

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from typing import Optional


class Reservation(BaseModel):
    name: str
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
def get_reservation_by_name(name: str):
    result = collection.find({"name": name}, {"_id": 0})
    res = []
    for r in result:
        res.append(r)
    print(res)
    if result is not None:
        return {
            "status": "found",
            "result": result
        }
    else:
        raise HTTPException(404, f"Couldn't find reservation with name: {name}'")
    pass


@app.get("/reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    query = {"table_number": table}
    result = collection.find(query, {"_id": 0, "name": 1, "time": 1, "table_number": 1})
    my_result = []
    for r in result:
        my_result.append(r)
    # print(my_result)
    if len(my_result) == 0:
        return {
            "result": "Not Found."
        }
    else:
        return {
            "result": my_result
        }


@app.post("/reservation")
def reserve(reservation: Reservation):
    time = reservation.time
    table_number = reservation.table_number
    query = {"time": time, "table_number": table_number}
    search = collection.find_one(query, {"_id": 0})
    if search is not None:
        raise HTTPException(status_code=404, detail={
            "message": f"Unfortunately, table number {table_number} at {time} "
                       f"already reserved so the new reservation will not allowed"})
    m = jsonable_encoder(reservation)
    collection.insert_one(m)
    return {"message": f"You reservation table number {table_number} is success."}


@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    tquery = {"name": reservation.name}
    ch = collection.find(tquery)
    resc = []
    for r in ch:
        resc.append(r)
    if len(resc)==0:
        raise HTTPException(400,f"Couldn't find name:{reservation.name}")
    time = reservation.time
    table_number = reservation.table_number
    query = {"time": time, "table_number": table_number}
    search = collection.find_one(query, {"_id": 0})
    if search is not None:
        raise HTTPException(400,f"Table not available")
    collection.update_many({"name":reservation.name},{"$set":{"table_number":reservation.table_number,"time":reservation.time}}) 
    return {
        "status": "updated success",
    }


@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number: int):
    query = {"name": name, "table_number": table_number}
    collection.delete_many(query)
    return {
        "result": "done."
    }
