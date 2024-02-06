import arcpy
import os
from arcpy import conversion as cv


class ConvertGeoPDF:
    # Object that enters folder given as path. Iterates through each file in path, checking that it's a .pdf.
    # Creates a .gdb named after the folder. For each in folder, if .pdf, converts .pdf to .tif in that .gdb
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        print(self.pdf_path)

    def convertPDF(self):
        folder_name = os.path.split(self.pdf_path)[1]
        print(folder_name)
        arcpy.CreateFileGDB_management(
            fr"C:\Users\kcneinstedt\OneDrive - mercercounty.org\Documents\ArcGIS\Projects\CRG_Imagery_Local",
            folder_name)
        for each in os.listdir(self.pdf_path):
            try:
                print(each)
                print(os.path.splitext(each)[1])
                if os.path.splitext(each)[1] != ".pdf":
                    continue

                else:
                    input_path = os.path.join(self.pdf_path, each)
                    print(input_path)
                    output_path = os.path.join(self.pdf_path, fr'{os.path.basename(each)}.tif')
                    cv.PDFToTIFF(input_path, output_path)
                    cv.RasterToGeodatabase(output_path,
                                           fr"C:\Users\kcneinstedt\OneDrive - mercercounty.org\Documents\ArcGIS\Projects\CRG_Imagery_Local\{folder_name}.gdb")

            except Exception as e:
                print(e)


r"""
path = fr"C:\Users\kcneinstedt\Downloads\GeoPDFs\Lawrence"

for folders in os.listdir(path):
    folder = os.path.join(path, folders)
    convert = ConvertGeoPDF(folder)
    convert.convertPDF()
"""


class PointMaker:
    # Object that contains an input and output feature class.
    # Methods can be used to build a dictionary of elevation values, and/or create a point class from line class.
    def __init__(self, in_fc, out_fc):
        self.in_fc = in_fc
        self.out_fc = out_fc

    def build_points_dict(self):
        points_dict = {}

        with arcpy.da.SearchCursor(self.in_fc, field_names=['OID@', 'SHAPE@XYZ']) as cursor:
            for row in cursor:
                points_dict[row[0]] = (row[1], row[2])

        print(points_dict)
        return points_dict

    def create_points_fc(self):
        try:

            arcpy.FeatureVerticesToPoints_management(self.in_fc, self.out_fc, 'ALL')
            arcpy.AddMessage(fr'Creating points from {self.in_fc}...')
            print(fr'Creating points from {self.in_fc}...')
        except Exception as e:
            print(e)

    def build_elevation_raster(self):
        arcpy.IDW_ga(self.out_fc, 'Shape.Z', None, fr'{self.out_fc}_raster')


if __name__ == '__main__':
    point = PointMaker(r'\\640gis01\GIS_Data\Publish\Parks\Trails\Trails.gdb\Trails',
                       r'\\640gis01\GIS_Data\Publish\Parks\Trails\Trails.gdb\TrailElevations')

    point.create_points_fc()
    point.build_elevation_raster()
