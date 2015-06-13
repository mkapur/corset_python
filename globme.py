import os
rootdir = 'C:\Users\mkapur\Dropbox\_CORSET\modeloutputs'
gp = arcgisscripting.create() 
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
		if file.endswith(".txt") and file.startswith("test_spatial_"):
			print os.path.join(subdir, file)
			arcpy.ASCIIToRaster_conversion(os.path.join(files,file), os.path.join(files,file.rsplit(".")[0][13:]), "FLOAT")
			