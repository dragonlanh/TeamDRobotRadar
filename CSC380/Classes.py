import json


class Obstacle:
    def __init__(self, ID, locX, locY):
        self.LocationX = locX
        self.LocationY = locY
        self.ID = ID

    def GetX(self):
        return self.LocationX

    def GetY(self):
        return self.LocationY

    def GetID(self):
        return self.ID

    def GetXY_Adjusted(self):
        return self.LocationX - 300, self.LocationY - 20

    def ConvertToJson(self):
        data = {"X": (self.LocationX - 300), "Y": (self.LocationY - 20)}
        return data
