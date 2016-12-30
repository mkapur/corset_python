mkapur@poire:~$ cat generateParallelCommnads.py

import argparse
import os
import shutil


# Reads the user_params file and for each pram
# write a modified input directory with min and another with max
# additionally, for each command, write n number of lines in the bashFile 
# that will be executed in parallel


parser = argparse.ArgumentParser(description='Generate input Files for paralle execution of Corset')
parser.add_argument('--nb_samples', type=int,
                   help='number of samples per variable to create,', required=True)
parser.add_argument('--params_file', type=argparse.FileType('r'),
                   help='file containing the program params', required=True)
parser.add_argument('--inputs_dir',
                   help='directory_containing all the modified input directories', required=True)
parser.add_argument('--outputs_dir',
                   help='directory_containing all the modified output directories', required=True)

args = parser.parse_args()


print "you are running with %s samples for the param file %s and directory %s" % (args.nb_samples, 
                                                                                  args.params_file.name, os.path.dirname(args.params_file.name))

if os.path.exists(args.inputs_dir):
    raise Exception("%s alread exists. Cannot overwrite directory" % args.inputs_dir)
if os.path.exists(args.outputs_dir):
    raise Exception("%s alread exists. Cannot overwrite directory" % args.outputs_dir )

os.mkdir(args.inputs_dir) ##makes a directory called whatever inputs_dir
os.mkdir(args.outputs_dir)

def getParamToChange(paramsFile): ##the text file with ranges
    modParams = []
    for line in paramsFile:
        line = line.rstrip() ##take each line individually
        if line.strip():
            data = line.split(",") ##break off the pieces before/after comma
            if len(data) == 3:
                modParams.append(data[0]) ##assigns first split value to list “modParams” (this will be alpha_C etc)
    return modParams

changeParams =  getParamToChange(args.params_file) ##do it to the txt file indicated. It’s assigning this function to an object

bashFile  = open("coreset_all.sh", 'w') ## A shell script is a computer program designed to be run by the Unix shell, a command line interpreter. The various dialects of shell scripts are considered to be scripting languages. ##so it’s calling this separate scripting file, which looks like just a bunch of directories.


for param in changeParams: ##each time you run the function (not sure what sub-object this designates)
    # copy the original input directory. ##The shutil module offers a number of high-level operations on files and collections of files. In particular, functions are provided which support file copying and removal. For operations on individual files, see also the os module.

    shutil.copytree(os.path.dirname(args.params_file.name), os.path.join(args.inputs_dir,  "%s_min" % param)) ##recursively copies your txt file (source) to a destination made on-the-fly that is pathed to your “Inputs” dir, with param_min appended
    shutil.copytree(os.path.dirname(args.params_file.name), os.path.join(args.inputs_dir,  "%s_max" % param)) ##same thing for max

##^^ is the part where you’re creating a fat batch of new input files, one for each param, that it will then go on and run.
    
    # make user params
    minFile = open(os.path.join(args.inputs_dir, "%s_min" % param, "user_params.txt") ,'w') ##open your new min and max file (alpha_c_min, alpha_c_max)
    maxFile = open(os.path.join(args.inputs_dir, "%s_max" % param, "user_params.txt") ,'w')
    
    # create args.nb_samples output directories for each of min and max ##do this as many times as specified by nb_samples
    for i in range(args.nb_samples):
        os.mkdir( os.path.join(args.outputs_dir, "%s_min_%s" % (param, i) ) ) ##loops through I and appends to end of file name; drops into outputs
        os.mkdir( os.path.join(args.outputs_dir, "%s_max_%s" % (param, i) ) )
    

    for line in open(args.params_file.name, 'r'):
        line = line.rstrip()
        data = line.split(",")
        if data[0] and data[0] == param: ##not sure why this is said twice
            minFile.write("%s,%s\n" % (param, data[1])) ##assign the second value (min, after 1st comma) to the min file, and name it by alpha_C, VALUE followed by a line break
            maxFile.write("%s,%s\n" % (param, data[2])) ##same thing using second max value
        else:
            minFile.write(line+"\n") ##otherwise just put in the line and a line break. Some of the lines are just notes so this overlooks them.
            maxFile.write(line+"\n")

    minFile.close()
    maxFile.close()

    # generate args.nb_samples in the bash file for each of the args.nb_samples
    for i in range(args.nb_samples):
        bashFile.write('python code/Main.py %s %s\n' % (os.path.join(args.inputs_dir,"%s_min/" % param), 
                                                      os.path.join(args.outputs_dir,"%s_min_%s/" % (param, i)) ))
        bashFile.write('python code/Main.py %s %s\n' % (os.path.join(args.inputs_dir,"%s_max/" % param), 
                                                      os.path.join(args.outputs_dir,"%s_max_%s/" % (param, i)) ))

bashFile.close()
