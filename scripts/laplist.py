import arcpy
import arcpy.da as da


class LapList:
    def __init__(self, lap: int, coords: list):
        self.self = self
        self.lap = lap
        self.coords = coords

    def take_coords(self, coordinate_list: list):
        for coordinate_tuple in coordinate_list:
            self.coords.append(coordinate_tuple)

    def draw_self(self, polyline_fc):
        with da.InsertCursor(polyline_fc, ['SHAPE@', 'Lap']) as cursor:
            cursor.insertRow((self.coords, int(self.lap, )))
        del cursor
