from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


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
    pass


@app.get("reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    pass


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
    pass


@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number: int):
    pass
