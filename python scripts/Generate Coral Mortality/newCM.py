## A script to construct "coral_mortality_2" text files for various RCP scenarios
## Creation date 16 Feb 2016
## M Kapur maia.kapur@noaa.gov

import random
import os

## for 8.5 Bleaching occurs with a 
## long-term frequency of twice per decade until year 2046, 
### after which it occurs annually; mortality ranges from 0.05 – 0.15
f2 = open(r'C:/Users/mkapur/Dropbox/_CORSET/DENDOGYRA/new85.txt', 'w')
f2.write("year\tdamage\taffected subregions(list)\n") ## heading

## real events at 09, 14 and 15
for n in (9,14,15):
	f2.write(str(n) + "\t[0.05,0.15]\t[1,2,3,4]\n")
## randomly select years for bleaching events between 2015 and 2046, with an avg of 2x/decade
rcp85 = range(15,46)
cmYrs = random.sample(rcp85,6)
## sort list
cmYrs.sort()
for y in range(1,5):
	f2.write(str(cmYrs[y]) + "\t[0.05,0.15]\t[1,2,3,4]\n")	
## fill in annual bleaching events following yr 2046
for n in range(46,101):
	f2.write(str(n) + "\t[0.05,0.15]\t[1,2,3,4]\n")
f2.close()

## for 4.5 Bleaching occurs with a 
## long-term frequency of twice per decade until year 2056, 
### after which it occurs annually; mortality ranges from 0.05 – 0.15
f1 = open(r'C:/Users/mkapur/Dropbox/_CORSET/DENDOGYRA/new45.txt', 'w')
f1.write("year\tdamage\taffected subregions(list)\n")
rcp45 = range(20,56)
cmYrs = random.sample(rcp45,7)
cmYrs.sort()
for n in (9,14,15):
	f1.write(str(n) + "\t[0.05,0.15]\t[1,2,3,4]\n")
 
for y in range(1,6):
	f1.write(str(cmYrs[y]) + "\t[0.05,0.15]\t[1,2,3,4]\n")
	
for n in range(56,101):
	f1.write(str(n) + "\t[0.05,0.15]\t[1,2,3,4]\n")
f1.close()

## To quickly edit damage values
f1 = open(r'C:/Users/mkapur/Dropbox/_CORSET/MHI_input/user_coral_mortality_2.txt', 'r')
f2 = open(r'C:/Users/mkapur/Dropbox/_CORSET/MHI_input/MAR_coral_mortality_4.txt', 'w')
for line in f1:
    f2.write(line.replace('[0.002,0.20]','[0.05,0.15]'))
f1.close()
f2.close()
