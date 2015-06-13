import arcgisscripting, os, arcpy 
rootdir = "C:\Users\mkapur\Dropbox\_CORSET\modeloutputs"
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print os.path.join(subdir, file)
        filepath = subdir + os.sep + file
        if filepath.endswith(".txt"):
           arcpy.ASCIIToRaster_conversion(os.path.join(files, file), os.path.join(files, file.rsplit(".")[0][13:]), "FLOAT") 
			
	