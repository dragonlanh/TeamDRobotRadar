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





