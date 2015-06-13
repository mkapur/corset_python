# Import system modules  
import arcgisscripting, os, glob  
  
# Create the Geoprocessor object  
gp = arcgisscripting.create()  
  
# Set local variables  
gp.workspace = r"C:\Users\mkapur\Dropbox\_CORSET\modeloutputs"  
#gp.outputCoordinateSystem = "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"  
 
configfiles = glob.glob(r'gp.workspace\*.txt')
# Process: ASCIIToRaster_conversion  
for x in configfiles:  
    gp.ASCIIToRaster_conversion(x, os.path.split(os.path.basename(x)[0][13:]), "FLOAT")  