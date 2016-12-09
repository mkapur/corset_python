# Name: DefineProjection.py 
# Description: Records the coordinate system information for the specified input dataset or feature class

# import system modules
import arcpy
import os

# set workspace environment
arcpy.env.workspace = r"C:\Users\mkapur\Dropbox\_CORSET\modeloutputs\MHI"   
#workspace = r"C:\Users\mkapur\Dropbox\_CORSET\modeloutputs\MHI\072315b"    
validNames = ["corl", "eaca", "hrbc", "herb", "lgpc", "lgpi", "maca", "mact", "smpc", "smpi", "urch"]

#set local variables
x = 0
z = x + 1
NoProjCount = 0 

#Identify rasters in your directory
FileList = arcpy.ListRasters()

#iterate through your designated directory, check if they're already projected, and project them into WGS_1984

for f in os.walk(workspace):
	for File in FileList:
		FileList = arcpy.ListRasters()
		desc = arcpy.Describe(File)
		SR = desc.spatialReference
		if SR.name == "Unknown":
			print "Projection of " + str(File) + " is " + SR.name + " so defining projection."
			f = open('NoProjection.txt', 'a')
			f.write(str(File)+"\n")
			f.close()
			arcpy.DefineProjection_management(File, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]") 
			NoProjCount=NoProjCount+1
		else:    
			print File + " is already projected into" + str(SR.name)

