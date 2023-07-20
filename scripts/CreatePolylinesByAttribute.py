import arcpy
from arcpy import da as da
import csv
import os
from laplist import LapList


class CreatePolylinesByAttribute(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Polylines by Attribute"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param = arcpy.Parameter(
            displayName="Input Table",
            name="input_table",
            datatype="DETable",
            parameterType="Required",
            direction="Input")
        params = [param]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.AddMessage('Imported Tool')
        arcpy.AddMessage(parameters)

        arcpy.env.workspace = r'C:\Users\kcneinstedt\OneDrive - mercercounty.org\Documents\ArcGIS\Projects\MyProject11\MyProject11.gdb'

        input_table = parameters[0]

        polyline_fc = os.path.join(arcpy.env.workspace, 'output')

        arcpy.CreateFeatureclass_management(arcpy.env.workspace, "output", 'POLYLINE', spatial_reference='GCS_WGS_1984')
        arcpy.AddField_management(polyline_fc, 'Lap', 'SHORT')
        dictionary = {}

        with open(input_table, "r") as gpsTrack:
            # Set up CSV reader and process the header
            csvReader = csv.reader(gpsTrack)
            header = next(csvReader)
            lapIndex = header.index("Lap")
            highest_lap_list = []

            for row in csvReader:
                try:
                    highest_lap_list.append(row[lapIndex])
                except IndexError:
                    continue
            total_laps = max(highest_lap_list)
            print(total_laps)
            gpsTrack.close()

        # Setting the range to the total_laps would iterate one short, because the end of the range is exclusive.
        # To include the last lap, increase the range by one. Less a magic number and more something when using ranges.
        for i in range(int(total_laps) + 1):
            # Create one LapList object per lap, up to the total number of laps.
            # Leave the lap coordinate array an empty list for now.
            dictionary[i] = LapList(i, [])

        for i in dictionary:
            # Reopen the csv to start the iterator at the beginning again for each lap number.
            with open(input_table, "r") as gpsTrack:
                # Set up CSV reader and process the header as seen in the lesson.
                csvReader = csv.reader(gpsTrack)
                header = next(csvReader)
                lapIndex = header.index("Lap")
                latIndex = header.index("Latitude")
                lonIndex = header.index("Longitude")

                for row in csvReader:
                    try:
                        # If the "Lap" column is 0, append coordinates as a tuple to the dictionary[0] object's coord list.
                        # Next iteration, if the "Lap" column is 1, appends coordinate tuple to the dictionary[1] object.
                        # And so on!
                        if int(row[lapIndex]) == i:
                            dictionary[i].coords.append((float(row[lonIndex]), float(row[latIndex])))

                        else:
                            continue

                    except IndexError:
                        continue

        gpsTrack.close()

        for i in dictionary:
            print(dictionary[i].coords)
            dictionary[i].draw_self(polyline_fc)

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
