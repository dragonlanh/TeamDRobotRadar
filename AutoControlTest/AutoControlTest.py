from gopigo import *
import easygopigo
import sys
import requests
import json

set_left_speed(175)
currentTurn = "none"


def GetMovementMode():
    try:
        res = requests.get("http://192.168.1.19:8080/MovementMode")
        data = res.content.decode()
        converted = json.loads(data)
        print(converted['Mode'])
        return converted['Mode']
    except requests.exceptions.Timeout as err:
        print("timeout error")


def GetActiveMovement():
    try:
        res = requests.get("http://192.168.1.19:8080/GetButton", timeout=.5)
        print(res)
        data = res.content.decode()
        converted = json.loads(data)
        print(converted['ButtonPress'])
        return converted['ButtonPress']
    except requests.exceptions.Timeout as err:
        print("timeout error")


def SendTurn(turn):
    try:
        res = requests.get('http://192.168.1.19:8080/ChangeTurn/{}'.format(turn), timeout=.5)
        print(res)
    except requests.exceptions.Timeout as err:
        pass


def UpdateCurrentTurn(turn):
    if turn != currentTurn:
        SendTurn(turn)
        return turn
    return turn


while True:
    if GetMovementMode() == "idle":
        print("idle")
    if GetMovementMode() == "auto":
        movement = GetActiveMovement()
        if movement == "fwd":
            print(movement)
            fwd()
        elif movement == "right":
            currentTurn = UpdateCurrentTurn("turning")
            print(movement)
            turn_right_wait_for_completion(90)
            currentTurn = UpdateCurrentTurn("turned")
        elif movement == "left":
            currentTurn = UpdateCurrentTurn("turning")
            print(movement)
            turn_left_wait_for_completion(90)
            currentTurn = UpdateCurrentTurn("turned")
        elif movement == "180":
            currentTurn = UpdateCurrentTurn("turning")
            print(movement)
            turn_right_wait_for_completion(180)
            currentTurn = UpdateCurrentTurn("turned")
        elif movement == "halt":
            print(movement)
            stop()
        else:
            print(movement)

