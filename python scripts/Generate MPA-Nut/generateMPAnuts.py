# A script to randomly generate reef cell numbers for 5%, 10%, and 20% MPA coverage, given a number of total cells. 
# This saves them in CORSET-ready format.
## M Kapur 08 Oct 2015
## Update 29 Dec 2016
import random
import os

percentages = [0.05, 0.10, 0.20] ##assign the percentage values

numCells = 571 ##it is zero-indexed so this will automatically account for that. Change this as needed based on res.

## MPAs
for p in percentages:
	reefCells = range(1, numCells) ##generates a list from 0 to x
	##takes a random sample from your cell range of the appropriate size, coerced to integer 
	mpaCells = random.sample(reefCells, int(numCells * p)) 
	save_path = 'C:/Users/mkapur/Dropbox/_CORSET/mk_code/' ##where you want to save it
	completeName = os.path.join(save_path + str(int(p*100)) +"mpaCells"+".txt") ##the name of the file
	text_file = open(completeName, 'w')
	text_file.write("\n".join(str(x) for x in mpaCells)) ##write the elements in a single column text file
	text_file.close()
	print "%s percent MPA reef cells generated, added to file %s" % (p, completeName)
	
##nutrification
for p in percentages:
	reefCells = range(1, numCells) ##generates a list from 0 to x
	nutCells = random.sample(reefCells, int(numCells * p)) 
	save_path = 'C:/Users/mkapur/Dropbox/_CORSET/mk_code/'
	completeName = os.path.join(save_path + str(int(p*100)) +"nutCells"+".txt")
	text_file = open(completeName, 'w')
	text_file.write("year\taffected cell IDs (list)\n") ## write in the title plus a line break
	for y in range(1,101):
		text_file.write(str(y)+"\t") ##write in the year plus a tab
		text_file.write(str(nutCells)+"\n") ## write in the list of values
	text_file.close()
	print "%s percent nutrified reef cells generated, added to file %s" % (p, completeName)
