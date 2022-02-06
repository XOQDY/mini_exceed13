from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

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
def reserve(reservation : Reservation):
    pass

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    pass

@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    query = {"name": name, "table_number": table_number}
    collection.delete_many(query)
    return {
        "result": "done."
    }

