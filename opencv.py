import cv2
import numpy 
from gui_buttons import *

# The buttons
button = Buttons()
button.add_button("person", 25, 25)

# Connect OpenCV to DNN
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320, 320), scale=1/255)

objects = []
with open("dnn_model/objects.txt", "r") as file_object:
    for object_name in file_object.readlines():
        object_name = object_name.strip()
        objects.append(object_name)

print("Object list")
print(objects)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Works on mouse click
def click(event, x, y, flags, params):
    global button_person
    if event == cv2.EVENT_LBUTTONDOWN:
        button.button_click(x, y)
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click)

while True:
    ret, frame = cam.read()

    active_buttons = button.active_buttons_list()
    print("Active buttons: ", active_buttons)

    (ids, scores, boxes) = model.detect(frame)
    for id, score, box in zip(ids, scores, boxes):
        x, y, w, h = box
        object_name = objects[id]

        if object_name in active_buttons:
            cv2.putText(frame, object_name, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 1,(100, 10, 50), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 10, 50), 3)

    # Display buttons
    button.display_buttons(frame)



    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()