"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime, date, time, timedelta

import helper
import model
import server

os.system("dropdb reservations")
os.system('createdb reservations')

model.connect_to_db(server.app)
model.db.create_all()

#Create timeslots for the upcoming year
timeslots_db = []
start_date = date(2022, 1, 1)
end_date = date(2023, 1, 1)
delta = timedelta(days=1)
while start_date < end_date:
    date = start_date.strftime("%Y-%m-%d")
    slots = [time(h, m).strftime('%H:%M') for h in range(0, 24) for m in (0,30)]
    for slot in slots:
        timeslot = helper.create_timeslots(date, slot)
        timeslots_db.append(timeslot)
    start_date += delta

#Add timeslots to SQLAlchemy and then commit
model.db.session.add_all(timeslots_db)
model.db.session.commit()

#Create 10 users
for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user = helper.create_user(email, password)
    model.db.session.add(user)

model.db.session.commit()
    