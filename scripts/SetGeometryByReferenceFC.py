import arcpy


class SetGeometryByReferenceFC(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Set Geometry to Match Reference Layer"
        self.description = "This tool accepts sets the geometry of a target feature class to match a reference class " \
                           "if their identifying fields match."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(name="target_fc",
                                 displayName="Target Feature Class",
                                 direction="Input",
                                 datatype="DEFeatureClass"
                                 )
        param1 = arcpy.Parameter(name="reference_fc",
                                 displayName="Reference Feature Class",
                                 direction="Input",
                                 datatype="DEFeatureClass"
                                 )
        param2 = arcpy.Parameter(name="target_field",
                                 displayName="Target Field",
                                 direction="Input",
                                 datatype="Field"
                                 )
        param3 = arcpy.Parameter(name="reference_field",
                                 displayName="Reference Field",
                                 direction="Input",
                                 datatype="Field"
                                 )
        params = [param0, param1, param2, param3]
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
        import arcpy as ap
        import arcpy.da as da

        target_fc = parameters[0].ValueAsText  # ap.GetParameterAsText()
        reference_fc = parameters[1].ValueAsText  # ap.GetParameterAsText()
        reference_dict = {}
        target_field = parameters[2].ValueAsText
        reference_field = parameters[3].ValueAsText


        def build_reference_dict():
            with da.SearchCursor(reference_fc, ["OID@", "SHAPE@", reference_field]) as searchcursor:
                for row in searchcursor:
                    reference_dict[row[2]] = row[1]

                ap.AddMessage(reference_dict)
                return

        def replace_geometry():
            with da.UpdateCursor(target_fc, ["OID@", "SHAPE@", target_field]) as cursor:
                for row in cursor:
                    key = row[2]
                    try:
                        # Simple variable swap. Point geometries in their current spatial reference/units are reassigned.
                        row[1] = reference_dict[key]
                        cursor.updateRow(row)
                        ap.AddMessage(f'OID {row[0]} Point set')
                    except AttributeError:
                        ap.AddMessage('AttributeError')
                        print('AttributeError')
                    except UnboundLocalError:
                        ap.AddMessage(f'{key} not found')
                        print(f'{key} not found')
                    except KeyError:
                        if key is None:
                            ap.AddMessage(f'Key is None for OID {row[0]}')
                    except Exception as e:
                        ap.AddMessage(f'An unknown error occurred. {e}')

        if ap.Describe(target_fc).spatialReference.name == ap.Describe(reference_fc).spatialReference.name:
            ap.AddMessage('Started')

            build_reference_dict()
            replace_geometry()

            ap.AddMessage('Completed.')
        else:
            ap.AddMessage("Spatial references do not match. Tool cancelled.")
            ap.AddMessage(ap.Describe(target_fc).spatialReference.name + "is not equal to " + ap.Describe(reference_fc).spatialReference.name)

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
