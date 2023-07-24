import arcpy


class BackupAGOL(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Download ArcGIS Online Content"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param = arcpy.Parameter(
            name="Folder",
            displayName="Folder",
            datatype="DEFolder"
        )
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
        import arcgis
        from arcgis.gis import GIS

        arcpy.AddMessage("ArcGIS Online Org account")
        gis = GIS('home')
        arcpy.AddMessage("Logged in as " + str(gis.properties.user.username))

        def downloadUserItems(downloadFormat):
            try:
                # Search items by username
                items = gis.content.search(query='owner:*', item_type='Feature *', max_items=50)
                for item in items:
                    print(item)

                # Loop through each item and if equal to Feature service then download it
                for item in items:
                    if item.type:
                        try:
                            result = item.export('sample {}'.format(item.title), downloadFormat)
                            result.download(parameters[0].ValueAsText)
                            print(f'Processed {item.title}')
                            # Delete the item after it downloads to save on space
                            result.delete()

                        except Exception as e:
                            print(e)
                            continue
            except Exception as e:
                print(e)

        # Function takes in two parameters. Username and the type of download format
        downloadUserItems(downloadFormat='File Geodatabase')
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
