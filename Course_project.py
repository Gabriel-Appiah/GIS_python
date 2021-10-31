#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Gabriel Appiah
#
# Created:     24/11/2020
#-------------------------------------------------------------------------------

import arcpy, os, sys

from arcpy.sa import *

# set your workspace, processing extent and raster anlysis cell size
arcpy.env.workspace = r'C:\Users\Gabriel\Desktop\Newaywsofdoingthings - Copy'

arcpy.env.cellSize = 100

# Data Preparation
# check out spatial analytic extension
arcpy.CheckOutExtension("spatial")

# Dissolve Counties Boundaries and use it as the env. extent

arcpy.Dissolve_management("StudyArea.shp","Dissolve_Co.shp","","","MULTI_PART","DISSOLVE_LINES")

arcpy.env.extent = "Dissolve_Co.shp"

# Convert counties polygon to raster to be used as a mask

#arcpy.PolygonToRaster_conversion("Dissolve_Co.shp", "FID", "raster_county","CELL_CENTER")

arcpy.env.mask = "rast_county"


#Data Preparation for Analysis
# Clipping files
#def clipt(inputfeature, clip_features,outfeature):
    #clipAnlysis = arcpy.Clip_analysis(inputfeature,clip_features,outfeature)
    #return clipAnlysis

#clipt("POP.shp","Dissolve_Co.shp","POPbyStudy.shp")
#clipt("Merge_Wetlands.shp","Dissolve_Co.shp","Wetlands.shp")
#clipt("Regional_Road.shp","Dissolve_Co.shp","Road1.shp")

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "PoPproj", "Dissolve_Co"


#Projecting the population by Block Group Data using State Plane
#Delete old files not useful in the analysis

#outCS = arcpy.SpatialReference('NAD 1983 UTM Zone 14N')
#arcpy.Project_management("POP.shp","POPbyStudy.shp",outCS)

#in_features = "POPbyStudy.shp"
#clip_features = "Dissolve_Co.shp"
#out_feature_class= r'C:\Users\Gabriel\Desktop\FinalFinalnewFinalFinal - Copy\Popproj.shp'
#arcpy.Clip_analysis(in_features,clip_features,out_feature_class)


#arcpy.Delete_management("POPbyStudy.shp")
#arcpy.Delete_management("POP.shp")



#Merge parcel data of the 5 counties, and create fieldmapping object
parcel_Ply = "Plymouth_parcel.shp"
parcel_Ida = "IdaCounty.shp"
parcel_Che = "Cherokee.shp"
parcel_Woo = "WoodburyCounty.shp"
#parcel_Dak = "Dakota_parcel.shp"

out_feature5 = "Parcel.shp"

#Create the required Field Map and Field Mapping Objects

fm_Land_Class = arcpy.FieldMap()

fms = arcpy.FieldMappings()

#Get the field names of the outpute featues from the originals files
#add fields to their corresponding fieldmap objects

field = "Land_Class"

fm_Land_Class.addInputField(parcel_Ply,field)
fm_Land_Class.addInputField(parcel_Ida,field)
fm_Land_Class.addInputField(parcel_Che,field)
fm_Land_Class.addInputField(parcel_Woo,field)
#fm_Land_Class.addInputField(parcel_Dak,field)

#Set the output field properties for the fieldmap objects
#add the fieldMap objects to the FieldMapping object

fieldName = fm_Land_Class.outputField
fieldName.name = "Land_Class"
fm_Land_Class.outputField = fieldName

fms.addFieldMap(fm_Land_Class)


arcpy.Merge_management([parcel_Ply,parcel_Che,parcel_Ida,parcel_Woo], out_feature5, fms)


#Delete old files not useful in the analysis

def deletfc(FClass1,FClass2,FClass3,FClass4):
    shapefile0=arcpy.Delete_management(FClass1)
    shapefile1=arcpy.Delete_management(FClass2)
    shapefile2=arcpy.Delete_management(FClass3)
    shapefile3=arcpy.Delete_management(FClass4)
    #shapefile4=arcpy.Delete_management(FClass5)
    return shapefile0,shapefile1,shapefile2,shapefile3

deletfc(parcel_Ply,parcel_Ida,parcel_Che,parcel_Woo)


#in_features= "Regional_Road.shp"
#clip_features = "Dissolve_Co.shp"
#out_feature_class= r'C:\Users\Gabriel\Desktop\FinalFinalnewFinalFinal - Copy\Road.shp'
#arcpy.Clip_analysis(in_features,clip_features,out_feature_class)
#arcpy.Delete_management("Regional_Road.shp")

# select major roads using where clause in the five counties


arcpy.MakeFeatureLayer_management("Regional_Road.shp", "roadslyr")

wclause = """ "FFC" = 'Interstate' OR "FFC" = 'Minor Arterial' OR "FFC" = 'Other Principal Arterial' OR "FFC" = 'Major Collector' """

arcpy.SelectLayerByAttribute_management("roadslyr", "NEW_SELECTION", wclause)

# Calcuate the Eucleadean distance around the major roads in the five counties

arcpy.gp.EucDistance_sa("roadslyr", "EucDist", "", "", "", "PLANAR", "", "")


# create a function for polygon to raster convention

# convert polygon raster

#arcpy.PolygonToRaster_conversion("PoPproj.shp", "POP_DEN", "POPRaster","CELL_CENTER")

#arcpy.PolygonToRaster_conversion("Parcel.shp", "Land_Class", "LandRaster","CELL_CENTER")

#arcpy.PolygonToRaster_conversion("Wetland.shp", "WETLAND_TY", "WetRaster","CELL_CENTER")


#in_features = "Merge_Wetlands.shp"
#clip_features = "Dissolve_Co.shp"
#out_feature_class= r'C:\Users\Gabriel\Desktop\FinalFinalnewFinalFinal - Copy\Wetlands.shp'
#arcpy.Clip_analysis(in_features,clip_features,out_feature_class)
#arcpy.Delete_management("Merge_Wetlands.shp")


def rast_conv(inFeatures,valField,outRaster):
    rastLayer = arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster,"CELL_CENTER")
    return rastLayer

ft_Classes = arcpy.ListFeatureClasses()
for fc in ft_Classes:
    inFeatures = fc
    valField = [f.name for f in arcpy.ListFields(fc)]
    for f in valField:
        if f == "POP_DEN":
            valFields = f
            outRaster1 = "Rt" + f
            rast_conv(inFeatures,valFields,outRaster1)
        elif f == "Land_Class":
            valField1 = f
            outRaster2 = "Rt" + f
            rast_conv(inFeatures,valField1,outRaster2)
        elif f == "WETLAND_TY":
            valField2 = f
            outRaster3 = "Rst" + f
            rast_conv(inFeatures,valField2,outRaster3)
        elif f == "FLD_ZONE":
            valField3 = f
            outRaster4  = "Rst"+f
            rast_conv(inFeatures,valField3,outRaster4)
        else:
            print "Rest of the Feature Class would not be converted to raster dataset"


# Create a reclassification function the rasters
def reClass(rast,reclassField,remap,outfeature):
    reClassified = arcpy.gp.Reclassify_sa(rast, reclassField,remap,outfeature,"DATA")
    return reClassified

# Reclassify Wetland
rast0 = outRaster3
reclassField0 = "VALUE"
remap0 = "1 5 0;NODATA 1"
outfc0 = "reclasswetL"

reClass(rast0,reclassField0,remap0,outfc0)

#Reclassify Land Use
rast1 = outRaster2
reclassField1 = "LAND_CLASS"
remap1 = "Agricultural 4;Commercial 3;Residential 0;Exempt 0;Industrial 4"
outfc1 = "reclasspar"

reClass(rast1,reclassField1,remap1,outfc1)

# Reclassify Pop_Density
rast2 = outRaster1
reclassField2 = "VALUE"
remap2 = "0 100 0;100 500 1;500 2500 2;2500 5000 3;5000 13900 4"
outfc2 = "reclasspop"

reClass(rast2,reclassField2,remap2,outfc2)

# Reclassify Distance from Major Road
rast3 = "EucDist"
reclassField3 = "VALUE"
remap3 = "0 1500 4;1500 3000 3;3000 4500 2;4500 6000 1;6000 14000 0"
outfc3 = "reclassdist"

reClass(rast3,reclassField3,remap3,outfc3)

rast4 = outRaster4
reClassField4 = "FLD_ZONE"
remap4 = "'0.2 PCT ANNUAL CHANCE FLOOD HAZARD' 0;A 0;AE 0;X 1;AO 0;AH 0;NODATA 1"
outfc4 = "reClassFP"

reClass(rast4,reClassField4,remap4,outfc4)


# Combine the reclassified layers by using raster calculator
inputs = '("reclassdist"+"reclasspop"+"reclasspar")*"reclasswetl"*"reClassFP"'
outputfc = "suitablesite"

arcpy.gp.RasterCalculator_sa(inputs,outputfc)
print(arcpy.GetMessages())


