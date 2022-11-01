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


def GetActiveMovement():
    res = requests.get("http://192.168.1.7:8080/GetMovement")
    data = res.content.decode()
    converted = json.loads(data)
    print(converted['MovementPress'])
    return converted['MovementPress']


while True:
    if GetMovementMode == "idle":
        pass
    if GetMovementMode == "auto":
        movement = GetActiveMovement()
        if movement == "fwd":
            print(movement)
        elif movement == "right":
            print(movement)
        elif movement == "left":
            print(movement)
        elif movement == "180":
            print(movement)
        elif movement == "halt":
            print(movement)
        else:
            print(movement)