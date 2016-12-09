import arcpy  
import os  

#set workspace environment 
workspace = arcpy.GetParameterAsText(0)  
arcpy.env.overwriteOutput = True
ignore = ['logs']
#iterate through files in the root directory
for root, dirs, files in os.walk(workspace):
		#ignore directories listed in the "ignore" argument
		for idir in ignore:
			if idir in dirs:
				dirs.remove(idir)
		for f in files:
			#select txt files to convert
			if f.endswith(".txt"):
				#create an object with the path and filename
				txt = os.path.join(root, f)
				#create a pair that consists of the entire path and the ".txt"
				name, ext = os.path.splitext(txt)
				#create a pair that consists of the head (leading up to first backslash) and tail(everything after)
				#so that you can truncate the first 13 characters of the filename
				outras, tail = os.path.split(name)
				#invoke the conversion tool
				arcpy.ASCIIToRaster_conversion(txt, os.path.join(outras, tail[12:]), "FLOAT")