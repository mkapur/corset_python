## A script to quickly select the cells randomly chosen as MPAs using selectMPAnut.py script. Useful for visualization.
## Note: Be sure that the mpaCells textfile you are refering to corresponds to the resolution of the layer you indicate.
## M Kapur 08 Oct 2015
## Update 29 Dec 2016

import os

##this just creates a where clause (query) for each value in MPAs. Kind of takes a while.
#dir = 'C:/Users/mkapur/Dropbox/_CORSET/mk_code/'
gdb = r'C:/Users/mkapur/Documents/corset.gdb/'
num = 10 ##change this to 10 or 20 if you want
#fileName = os.path.join(dir, str(num) + "mpaCells.txt")
#fileName = arcpy.getParameterAsText(0) ##select which MPA file you'd like to work with
fileName = 'C:/Users/mkapur/Dropbox/_CORSET/mk_code/10mpaCells.txt'
text_file = open(fileName, 'r')  
for cell in text_file:
	query = 'reef_cell'+"="+str(cell)
	arcpy.management.SelectLayerByAttribute("mhi_grid_2k_coral","ADD_TO_SELECTION",query)
	#outFile = arcpy.getParameterAsText(1)
	#layerName = arcpy.getParameterAsText(2)
	#arcpy.CopyFeatures_management("mhi_grid_2k_coral", outFile, layerName)
	arcpy.CopyFeatures_management("mhi_grid_2k_coral", os.path.join(gdb, "mpaCells"+str(num)))
