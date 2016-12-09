#MKapur
#Batch Raster to PCA
#Import system modules
import arcpy, os
from arcpy import env
from arcpy.sa import *

# Set environment settings
workspace = arcpy.GetParameterAsText(0) 

arcpy.env.overwriteOutput = True

rasterList = arcpy.ListRasters("*", "GRID")

input_raster = arcpy.GetParameterAsText(1)
arcpy.SetParameter(2, input_raster)

# Check out the ArcGIS Spatial Analyst extension license
# arcpy.checkOutExtension("Spatial")

#designate the name and location of output data file
outRaster = arcpy.GetParameterAsText(3) 

for rasters in os.walk(input_raster):
# Set local variables
	inRasterBand1 = arcpy.GetParameterAsText(0)
	inRasterBand2 = arcpy.GetParameterAsText(1)
	numberComponents = 3
# Execute PrincipalComponents
	outPrincipalComp = PrincipalComponents(rasters, 2,
                                       outDataFile)
	print "successfully performed PCA on raster %r." %rasters								   
# Save the output
	outPrincipalComp.save()
	