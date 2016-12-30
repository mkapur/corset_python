# A script to be used in ArcGIS to assign subregions to DAR FishChart Map. 
# This helped match polygons from fishery reporting regions to one of the four subregions used in CORSET

# Import system modules
import arcpy
from arcpy import env
 
# Set environment settings
env.workspace = "C:/data/airport.gdb"
 
# Set local variables
inTable = "MHI_FishChart08"
fieldName = "Subregion"
expression = "myCalc(!AREA_ID!)"
codeblock = """def myCalc(basemap):
	if basemap >= 1:
		return 2
	if areaid >= 300 and areaid <= 400:
		return 3
	if areaid >= 500 and areaid <= 600:
		return 1
	if areaid <= 200:
		return 4
	else:
		return 0"""
 
 
# Execute CalculateField 
arcpy.CalculateField_management(inTable, fieldName, expression, "PYTHON", codeblock)
