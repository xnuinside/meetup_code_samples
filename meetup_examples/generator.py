from uuid import uuid4
from random import choice, randint
from datetime import datetime
import json

# create datasets for memory profilers example data/ships.json, data/cargo.json


ships = [{'name': uuid4().hex, 'id': uuid4().int/100000000000000000000} for _ in range(10)]
cargo = [{
    'id': randint(1000000, 2000000),
    'product': {'name': choice(["Elec'sOil", "NewProd", "Duper", "Super"]),
                "uid": choice(["elec109ui", "newpr9032", "duper123", "super123"])},
    "quantity": {"value": randint(1000, 2450), "id": "mt"},
    'dates': {'start': choice([datetime(2200, 10, 11), datetime(2200, 10, 14),
                               datetime(2200, 10, 12), datetime(2200, 10, 13)]),
              'end': choice([datetime(2200, 11, 11), datetime(2200, 11, 14),
                             datetime(2200, 11, 12), datetime(2200, 11, 13)])}
              } for _ in range(6000)]


def datetime_serialize(o):
    if isinstance(o, datetime):
        return o.isoformat()

with open('data/ships.json', 'w+') as ships_file:
    json.dump(ships, ships_file, indent=1, default=datetime_serialize)

with open('data/cargo.json', 'w+') as cargo_file:
    json.dump(cargo, cargo_file, indent=1, default=datetime_serialize)


