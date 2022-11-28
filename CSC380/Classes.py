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
        finalX, finalY = self.LocationX - 300, self.LocationY - 20
        xmod = finalX % 10
        ymod = finalY % 10
        if xmod < 5:
            finalX -= xmod
        else:
            finalX += (10 - xmod)

        if ymod < 5:
            finalY -= ymod
        else:
            finalY += (10 - ymod)

        return finalX, finalY

    def ConvertToJson(self):
        data = {"X": (self.LocationX - 300), "Y": (self.LocationY - 20)}
        return data
