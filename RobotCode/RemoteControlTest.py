from gopigo import *
import easygopigo
import sys
import requests
import json

Usensor = easygopigo.UltraSonicSensor()


def GetMovementMode():
    try:
        res = requests.get("http://192.168.1.19:8080/MovementMode", timeout=0.1)
        data = res.content.decode()
        converted = json.loads(data)
        print(converted['Mode'])
        return converted['Mode']
    except requests.exceptions.Timeout as err:
        print("timeout error")


def GetActiveButton():
    try:
        res = requests.get("http://192.168.1.19:8080/GetButton", timeout=0.1)
        data = res.content.decode()
        converted = json.loads(data)
        print(converted['ButtonPress'])
        return converted['ButtonPress']
    except requests.exceptions.Timeout as err:
        print("button error")


while True:
    # print("running")
    if GetMovementMode() == "idle":
        pass
    if GetMovementMode() == "remote":
        button = GetActiveButton()
        if button == "w":
            fwd()
        elif button == "a":
            left_rot()
        elif button == "s":
            bwd()
        elif button == "d":
            right_rot()
        else:
            print(button)





