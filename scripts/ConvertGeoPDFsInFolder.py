import arcpy
from ObjectBox import ConvertGeoPDF


class ConvertGeoPDFsInFolder(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Convert GeoPDFs in Folder"
        self.description = "# Object that enters folder given as path. Iterates through each file in path, checking " \
                           "that it's a .pdf. Creates a .gdb named after the folder. For each in folder, if .pdf, " \
                           "converts .pdf to .tif in that .gdb."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter('pdf_path',
                                 'Folder path of PDFs',
                                 direction='Input',
                                 datatype='DEFolder')
        params = [param0]
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
        convert = ConvertGeoPDF(parameters[0].ValueAsText)
        convert.convertPDF()
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
