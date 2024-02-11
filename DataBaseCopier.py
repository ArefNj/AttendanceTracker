import csv
from enum import Enum


class State(Enum):
    PRESENT = 'Present'
    ABSENT = 'Absent'
    ADMIN = 'Admin'


fileName = input() + ".csv"
# -----------------------------------------------------------------------

DataBase = {}

# READ CSV FILE
with open("MAIN_DATABASE.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        Id = row[0]
        name = row[1]
        user = row[2]
        if user == "Admin":
            DataBase.__setitem__(Id, [name, State.ADMIN])
        elif user == "Present":
            DataBase.__setitem__(Id, [name, State.PRESENT])
        else:
            DataBase.__setitem__(Id, [name, State.ABSENT])

with open(fileName, "w", newline="") as file:
    writer = csv.writer(file)
    for i in DataBase:
        row = [i, DataBase.get(i)[0], DataBase.get(i)[1].value]
        writer.writerow(row)
