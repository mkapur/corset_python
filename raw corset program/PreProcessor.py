import sys 
from Engine import *

# CORSET_v5
#
# Regional scale bio-physical coral reef model, with map input and 
# parameterisation for the Meso-American Barrier Reef system and the 
# South China Sea complex.
#
# Initial conditions are set for each subregion.

try:
    inputpath = sys.argv[1]
    outputpath = sys.argv[2]
except:
    inputpath = 'input/'
    outputpath = 'output/'

Inputs(inputpath,outputpath)   # Process inputs: to switch off preceed with '#'

