import os, sys
#Set Workspace Env
workspace = r"C:\Users\mkapur\Dropbox\_CORSET\modeloutputs\MHI\102615c"

#Make sure the script is working within that path
os.chdir(workspace)

#A for-loop that goes through each file and replaces one string with another
for f in os.listdir(workspace):
	os.renames(f, f.replace("85noMPA", "noforc6").lower())

print "files successfully renamed"