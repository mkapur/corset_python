##Script to batch select-by-attributes on a raster after converting it to an "integer" raster.
##Created by: M Kapur 09 22 2015

##You may copy and paste the whole thing into the ArcPy window, or save it somewhere, right-click in the ArcPy
##window and hit "load".

import arcpy
import os
from arcpy import env
from arcpy.sa import *

#Set workspace environment
workspace = r"C:\Users\mkapur\Documents\temp.gdb" #your working directory - a root directory containing all raster files of interest
arcpy.env.overwriteOutput = True #this allows you to overwrite previous outputs from this script, should you choose to change something

outDir = u"D:\DXF-Export\\" ## you can use this in place of "root" on line 20 if you'd like to save elsewhere. Otherwise it will save in wd.
sqlClause = "Value < -75 AND Value > -400" ##Change this if necessary
			
for root, dirs, files in os.walk(workspace): #this "walks" thru your workspace directory
	rasters = arcpy.ListRasters("*") #generates a list of raster datasets in workspace
	for r in rasters:
		outRasInt = os.path.join(root, r) + "int" ##name of new "int" raster will be the same with the string "int" at end
		arcpy.Int_3d(r, outRasInt) #run int conversion on each raster
		print "successfully converted %s to Int Raster" % r
		s = outRasInt
		attExtract = arcpy.sa.ExtractByAttributes(s, sqlClause) #invoke extraction tool
		outRasSel = os.path.join(s[:-3]) + "Sel"
		attExtract.save(outRasSel) #save the outputs
		print "successfully extracted %s by specified attributes" % outRasInt


