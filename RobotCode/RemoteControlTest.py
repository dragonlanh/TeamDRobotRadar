from gopigo import *
import sys
import requests
import json


def GetMovementMode():
    res = requests.get("http://192.168.1.7:8080/MovementMode")
    data = res.content.decode()
    converted = json.loads(data)
    print(converted['Mode'])
    return converted['Mode']


def GetActiveButton():
    res = requests.get("http://192.168.1.7:8080/GetButton")
    data = res.content.decode()
    converted = json.loads(data)
    print(converted['ButtonPress'])
    return converted['ButtonPress']


while True:
    if GetMovementMode == "idle":
        pass
    if GetmovementMode == "remote":
        button = GetActiveButton
        if button == "w":
            print(button)
        elif button == "a":
            print(button)
        elif button == "s":
            print(button)
        elif button == "d":
            print(button)
        else:
            print(button)



