class Obstacle:
    def __init__(self, locX, locY):
        self.LocationX = locX
        self.LocationY = locY

    def GetX(self):
        return self.LocationX

    def GetY(self):
        return self.LocationY

    def ConvertToJson(self):
        data = {"X": self.LocationX, "Y": self.LocationY}
        return data
    
