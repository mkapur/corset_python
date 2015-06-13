# Import system modules  
import arcgisscripting, os, arcpy 
arcpy.env.workspace = "C:\Users\mkapur\Dropbox\_CORSET\modeloutputs"
#ascFileList = arcpy.ListFiles("*.txt")
# Create the Geoprocessor object  
gp = arcgisscripting.create()  

#for ascFile in arcpy.ListFiles("*.txt"):
#	ascFileName = file.rsplit(".")[0][13:]
#	rastFile = ascFileName + "out.img"
#	arcpy.ASCIIToRaster_conversion(ascFile, rastFile, "FLOAT")
#desginate root file to look in
rootdir = "C:\Users\mkapur\Dropbox\_CORSET\modeloutputs"
inDir = subdir, dirs, files in os.walk(rootdir)
InAsciiFile = None  
outRaster = "output"
#Iterate raster conversion command through each subdirectory
for InAsciiFile in os.walk(rootdir):
        if file.rsplit(".")[-1] == "txt":   
			gp.ASCIIToRaster_conversion(os.path.join(inDir,InAsciiFile), os.path.join(OutRaster,file.rsplit(str("."))[0][13:]), "FLOAT")

			
#inDir = ios.walk(rootdir)
#for f in inDir:
#	if f.rsplit(".")[-1] == "txt":
#		ascFileName = f.rsplit(".")[0][13:]
#		rastFile = ascFileName + "out.asc"
#		arcpy.ASCIIToRaster_conversion(os.path.join(inDir, f), os.path.join(rastFile, ascFileName), "FLOAT")



#for root, dirs, files in os.walk(rootdir):
 #   for f in files:
  #      if f.startswith('test_spatial') and f.endswith('.txt'):
	#		ascFileName = f.rsplit(".")[0][13:]
	#		rastFile = ascFileName + "out.asc"
	#		arcpy.ASCIIToRaster_conversion(os.path.join(rootdir, f), os.path.join(rastFile, ascFileName), "FLOAT")

#for root, dirs, files in os.walk(rootdir):
 #   for f in files:
  #      if f.startswith('test_spatial') and f.endswith('.txt'):
	#		print f
	#		arcpy.ASCIIToRaster_conversion(os.path.join(f, rastFile), "FLOAT")