from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json

app = FastAPI()

class Visitor(BaseModel):
    PersonCode: int
    PersonRole: str
    LastSecurityPointNumber: int
    LastSecurityPointDirection: str
    LastSecurityPointTime: datetime

visitors = []

MAX_CLIENTS = 50
MAX_EMPLOYEE = 10

import random

for i in range(MAX_CLIENTS):
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    current_time = datetime.now().replace(hour=random_hour, minute=random_minute)
    visitors.append(
        Visitor(
            PersonCode=i+1,
            PersonRole="Client",
            LastSecurityPointNumber=random.randint(1, 22),
            LastSecurityPointDirection=random.choice(["in", "out"]),
            LastSecurityPointTime=current_time
        )
    )
for i in range(MAX_EMPLOYEE):
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    current_time = datetime.now().replace(hour=random_hour, minute=random_minute)
    visitors.append(
        Visitor(
            PersonCode=i+1,
            PersonRole="Doctor",
            LastSecurityPointNumber=random.randint(1, 22),
            LastSecurityPointDirection=random.choice(["in", "out"]),
            LastSecurityPointTime=current_time
        )
    )


@app.get("/PersonLocations/{name}")
def get_todays_visitors(name: str):
    today = datetime.now().date()
    today_visitors = [visitor.dict() for visitor in visitors if visitor.LastSecurityPointTime.date() == today]
    filename = f"visitors_{name}_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.json"
    with open(filename, "w") as file:
        json.dump(str(today_visitors), file)

    return today_visitors