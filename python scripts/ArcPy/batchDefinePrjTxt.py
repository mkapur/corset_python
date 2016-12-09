# Name: DefineProjection.py 
# Description: Records the coordinate system information for the specified input dataset or feature class

# import system modules
import arcpy
import os
arcpy.env.overwriteOutput = True

# set workspace environment
arcpy.env.workspace = r"C:\Users\mkapur\Dropbox\_CORSET\modeloutputs\MHI\072315b"  
workspace = arcpy.GetParameterAsText(0)  
validNames = ["corl", "eaca", "hrbc", "herb", "lgpc", "lgpi", "maca", "mact", "smpc", "smpi", "urch"]

#set local variables
x = 0
z = x + 1
NoProjCount = 0 

#Identify rasters in your directory
def findRasters (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join (root, file)


FileList  = arcpy.ListRasters()
for root, dirs, files in os.walk(workspace):
	if files.endswith(tuple(validNames)):
		print files

#define local variables		
outRaster = os.path.join(File + "prj")
corsetprj = r"C:\Users\mkapur\Dropbox\_CORSET\mk_code\CORSET_MHI.prj"

#iterate through your whole directory, check if they're already projected, and project them into WGS_1984
#currently this ONLY WORKS on a main output file, not a mother file.
for root, dirs, files in os.walk(workspace):
	FileList = arcpy.ListRasters()
	for f in FileList:
		#FileList = arcpy.ListRasters()
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
			print File + " is already projected into " + str(SR.name)
		elif SR.name == "WGS_1984":
			print "Projection of " + str(File) + " is " + SR.name + " so projecting to CORSET_MHI."
			arcpy.ProjectRaster_management(f, outRaster, corsetprj)
			f = open('NoProjection.txt', 'a')
			f.write(str(File)+"\n")
			f.close()
			arcpy.DefineProjection_management(File, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]") 
			NoProjCount=NoProjCount+1
		else:    
			print File + " has a spatial referernce defined as " + str(SR.name)
		
			


