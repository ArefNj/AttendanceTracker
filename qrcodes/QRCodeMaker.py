import csv
import qrcode
from openpyxl import load_workbook
IDs = []

with open("../MAIN_DATABASE.csv", "r") as file:
    reader = csv.reader(file)
    for i in reader:
        IDs.append(i[0])

for data in IDs:
    img = qrcode.make(data)
    name = data + ".png"
    img.save(name)

workbook = load_workbook("testDatabase.xlsx")
sheet1 = workbook.active

# for i in sheet1['c2:']
