#-------------------------------------------------------------------------------
# Name:        Bloodhound
# Purpose:     Make 'Select by Attribute' easier for GIS users
# Author:      Franklin Hutto
# Created:     06/09/2016
#-------------------------------------------------------------------------------
import arcpy
class ToolBox(object):
    def __init__(self):
        """Define the toolbox
        the name of the toolbox is the name of the .pyt file"""
        self.label = "SurveyToolBox"
        self.alias = "survey"
        # List of tools classes associated with this toolbox
        self.tools =[Bloodhound]

class Bloodhound(object):
    def __init__(self):
        """Define the tool
        (tool name is the name of the class"""
        self.label = "Bloodhound"
        self.description = "A tool to make 'Select by Attribute' easier for GIS users"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # first parameter
        param0 = arcpy.Parameter(
            displayName="Feature",
            name="Feature",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param0.filter.list = ["POINT", "POLYLINE", "POLYGON"]
        # second parameter
        param1= arcpy.Parameter(
            displayName="Field",
            name="Field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        param1.filter.list = ["Short", "Long", "Single", "Double", "Text", "Date"]
        param1.parameterDependencies = [param0.name]
        # third parameter
        param2= arcpy.Parameter(
            displayName="Record",
            name="Record",
            datatype="String",
            parameterType="Required",
            direction="Input")
        params = [param0,param1,param2]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute"""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameter before interanl
        validation is performed. This method is called whenever a parameter
        has been changed"""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each
        tool parameter. This method is called after internal validation"""
        return

    def execute(self, parameters, messages):
        """The source code of the tool"""
        #finds current mapdoucument and dataframe
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd,"Layers")[0]
        #input
        Feature = parameters[0].valueAsText
        Field= parameters[1].valueAsText
        Record = parameters[2].value
        #Clear Selection
        for l in arcpy.mapping.ListLayers(mxd):
          if l.supports("DATASETNAME"):arcpy.SelectLayerByAttribute_management(l, "CLEAR_SELECTION")
        #Check field type
        fields = arcpy.ListFields(Feature)
        for field in fields:
            if field.name == Field:
                field_type = field.type
        # Select by Attribute
        if field_type == "String": sql = "UPPER("+Field+")='"+Record.upper() + "'"
        elif field_type == "Date":
            dateSplit = Record.split()
            year = dateSplit[0]
            month = dateSplit[1]
            day = dateSplit[2]
            if month == '2' and day =='28' or day == '29':
                yearPlus = year
                monthPlus = '3'
                dayPlus = '1'
            elif month == '4' or month =='6' or month =='9' or month =='11' and day =='30':
                yearPlus = year
                monthPlus =str(int(dateSplit[1])+ 1)
                dayPlus = '1'
            elif month == '1' or month =='3' or month =='5' or month =='7' or month =='8'or month =='10' and day =='31':
                yearPlus = year
                monthPlus =str(int(dateSplit[1])+ 1)
                dayPlus = '1'
            elif month =='12' and day =='31':
                yearPlus = str(int(dateSplit[0])+ 1)
                monthPlus ='1'
                dayPlus = '1'
            else:
                yearPlus = year
                monthPlus = month
                dayPlus = str(int(dateSplit[2])+ 1)
            sql= ("LAST_EDITED_DATE BETWEEN timestamp '"
                    +year+"-"+month+"-"+day
                    +" 00:00:00' and timestamp '"
                    +yearPlus+"-"+monthPlus+"-"+dayPlus
                    +" 00:00:00'")
        else:sql =Field+"="+Record
        arcpy.SelectLayerByAttribute_management(Feature,"NEW_SELECTION",sql)
        #zoom to selected
        result = arcpy.GetCount_management(Feature)
        count = int(result.getOutput(0))
        if count > 0:
            df.zoomToSelectedFeatures()
            geometryType = arcpy.Describe(Feature)
            if geometryType.shapeType == "Point":
                if count == 1:
                    df.scale = 12000
                    arcpy.RefreshActiveView()
        else: arcpy.AddWarning("There was nothing selected")
        #delete stuff
        del mxd, df, fields, count, Feature, Field, Record









































