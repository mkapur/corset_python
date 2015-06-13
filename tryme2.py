# Import system modules  
import arcgisscripting, os, itertools, os.path

ROOT = r'C:\Users\mkapur\Dropbox\_CORSET\modeloutputs'

outRaster = outRaster

for path in itertools.product(outRaster):
    print os.path.join(ROOT, *path)

# Create the Geoprocessor object  
gp = arcgisscripting.create()  
  
# Set local variables  
InAsciiFile = None  
inDir = r"C:\Users\mkapur\Dropbox\_CORSET\modeloutputs\060815a"  


#run for loop and truncate "test_spatial_" from beginning of each file name. Add output rasters into a specific folder for each one.
for InAsciiFile in os.walk(inDir):  
    if InAsciiFile.startswith('test_spatial') and InAsciiFile.endswith('.txt'):  
        print InAsciiFile  
        # Process: ASCIIToRaster_conversion  
        gp.ASCIIToRaster_conversion(os.path.join(inDir,InAsciiFile), os.path.join(OutRaster,InAsciiFile.rsplit(".")[0][13:]), "FLOAT")
