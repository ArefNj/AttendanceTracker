import csv
from enum import Enum
import cv2
import numpy as np
from pyzbar.pyzbar import decode


class State(Enum):
    PRESENT = 'Present'
    ABSENT = 'Absent'
    ADMIN = 'Admin'


# Setting
fileAddress = "test.csv"
autoCheckerFlag = False


video = cv2.VideoCapture(0)
video.set(3, 640)
video.set(4, 480)


# AutoChecker settings
checker = None
counter = None
if autoCheckerFlag:
    counter = 8

# ----------------------------------------------------------------------------------------------------------------------
DataBase = {}

# READ CSV FILE
with open(fileAddress, "r") as file:
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


while True:
    success, img = video.read()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape(-1, 1, 2)
        pts2 = barcode.rect
        label = None
        label_color = None

        # Check QRCode
        if myData in DataBase.keys():
            name = DataBase.get(myData)[0]
            state = DataBase.get(myData)[1]

            # Present
            if state == State.PRESENT:
                label = name
                label_color = (0, 255, 0)
            # Admin
            elif state == State.ADMIN:
                label = 'Admin: ' + name
                label_color = (255, 0, 255)
            # Absent
            else:
                # Admin Check System
                # Automatic system
                if autoCheckerFlag:
                    if checker == myData:
                        counter -= 1
                    else:
                        checker = myData
                    if counter < 0:
                        counter = 5
                        DataBase.__setitem__(myData, [name, State.PRESENT])
                # Manual System
                # KEY_WAIT for accept
                accept_key = cv2.waitKey(1)
                if accept_key == ord(" "):
                    DataBase.__setitem__(myData, [name, State.PRESENT])

                label = myData
                label_color = (255, 0, 0)
        # NOT_VALID_QRCODE
        else:
            label = "NOT VALID"
            label_color = (255, 0, 255)

        cv2.putText(img, label, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, label_color, 2)
        cv2.polylines(img, [pts], True, label_color, 3)

    # SHOW VIDEO
    cv2.imshow('cam_1', img)

    # Print List
    print_list_key = cv2.waitKey(1)
    if print_list_key == ord("h"):
        # PRINT DATA_BASE
        print('-' * 30)
        for i in DataBase.values():
            print(i[0] + "\t, " + i[1].value)
        print('-' * 30)

    # BREAK KEY
    break_key = cv2.waitKey(1)
    if break_key == 27:
        break

# PRINT DATA_BASE
print("END" * 10)
print('-' * 30)
for i in DataBase.values():
    print(i[0] + "\t, " + i[1].value)
print('-' * 30)

with open(fileAddress, "w", newline="") as file:
    writer = csv.writer(file)
    for i in DataBase:
        row = [i, DataBase.get(i)[0], DataBase.get(i)[1].value]
        writer.writerow(row)

# RELEASE CAM
video.release()
cv2.destroyAllWindows()
