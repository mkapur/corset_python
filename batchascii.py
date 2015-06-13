# Import system modules  
import arcgisscripting, os  
  
# Create the Geoprocessor object  
gp = arcgisscripting.create()  
  
# Set local variables
#In this case, you need to designate the directory individually. Working on a script that will go through ALL model outputs and make raster conversions.
InAsciiFile = None  
inDir = r"C:\Users\mkapur\Dropbox\_CORSET\modeloutputs\061015"  
OutRaster = r"C:\Users\mkapur\Dropbox\_CORSET\modeloutputs\061015\outRaster"  

#run for loop and truncate "test_spatial_" from beginning of each file name. Add output rasters into folder indicated above.
for InAsciiFile in os.listdir(inDir):  
	if InAsciiFile.endswith(".txt"):
        # Process: ASCIIToRaster_conversion  
		gp.ASCIIToRaster_conversion(os.path.join(inDir,InAsciiFile), os.path.join(OutRaster,InAsciiFile.rsplit(".")[0][13:]), "FLOAT")
		