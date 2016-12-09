import os
import datetime
import time
import threading
import matplotlib
matplotlib.use("Agg")
from pylab import *
try:
   import cPickle as pickle
except:
   import pickle

from Parameters import *
from Forcing import *
from Map import Map
from Transition import Transition
from Simulation import Simulation
from Output import Output
from Display import Display

# Model version and variables
version = 'CORSET_v5'
variables = ['C','Cb','Cs','T','M','E','H','Ps','Pl','U',
             'catchH','catchPs','catchPl']

def Inputs(inputpath,outputpath):
   print 'Processing inputs'
   init_errors = 0
   error_log = open(outputpath + 'error_log.txt','w')
   print >>error_log,datetime.datetime.now().strftime('%d-%m-%y, %H:%M')
   #print >>error_log,os.getenv('COMPUTERNAME')
   print >>error_log,'\n',
   warning_log = open(outputpath + 'warning_log.txt','w')
   print >>warning_log,datetime.datetime.now().strftime('%d-%m-%y, %H:%M')
   #print >>warning_log,os.getenv('COMPUTERNAME')
   print >>warning_log,'\n',
   print >>warning_log,'No warnings'
   warning_log.close()
   
   # Check user options file is correctly labelled
   try:
      options = open(inputpath + '/CORSET_options.txt','U')
   except:
      print >>error_log,'Missing input files'
      print >>error_log,'** Input folder should contain an options file',
      print >>error_log,'"CORSET_options.txt"'
      init_errors += 1
   if init_errors > 0:
      error_log.close()
      raise SystemExit(1)
   
   # Read in user options and check for errors
   optd = {}
   options_lines = options.readlines()
   options.close()
   valid_names = ["scenario","region","res_MAR","res_SCS","years",
                  "equilibration","runs","seed","initial_vals",
                  "forc_hurr","hfreq","hmax_sr","hmin_cat","hmax_cat",
                  "forc_cm","cmfreq","cmmax_sr",
                  "forc_fish","fmin_MAR","fmax_MAR","fmin_SCS","fmax_SCS",
                  "fmin_user","fmax_user","forc_df","forc_nut","forc_sed"]
   for line in options_lines:
      clean_line = line.strip()
      if((len(clean_line) > 0) and (clean_line[0] != '#')):
         splits = clean_line.split('=')
         if(len(splits) == 2):
            varname = splits[0].strip()            
            value = splits[1].strip()
            var_split = value.split("#")
            if(len(var_split) == 2):
               value = var_split[0].strip()
            if(varname in valid_names):
               if(len(splits) == 2):
                  if(varname == 'scenario'):
                     optd['scenario'] = value
                  elif(varname in ['fmin_MAR','fmax_MAR','fmin_SCS','fmax_SCS',
                  'fmin_user','fmax_user']):
                     optd[varname] = float(value)
                  else:
                     optd[varname] = int(value)
            else:
               if init_errors == 0:
                  print >>error_log,'Errors in options file'
               print >>error_log,'"%s" is not a valid input key' %varname
               print >>error_log,'Valid input keys are ' + `valid_names` 
               init_errors += 1
   if init_errors > 0:
      error_log.close()
      raise SystemExit(1)
   
   if optd['region'] not in [0,1,2]:
      print >>error_log,'Errors in options file'
      print >>error_log,'** Input for "region" should be either "0", "1" or "2"'
      print >>error_log,'(current value of "%s" is invalid)' %optd['region']
      init_errors += 1
   if optd['region'] == 0:
      if optd['res_MAR'] not in [1,2]:
         if init_errors == 0:
            print >>error_log,'Errors in options file'
         print >>error_log,\
               '** Input for "res_MAR" should be either "1" or "2"'
         print >>error_log,'(current value of "%s" is invalid)' %optd['res_MAR']
         init_errors += 1
   if optd['region'] == 1:
      if optd['res_SCS'] not in [1,3]:
         if init_errors == 0:
            print >>error_log,'Errors in options file'
         print >>error_log,\
               '** Input for "res_SCS" should be either "1" or "3"'
         print >>error_log,'(current value of "%s" is invalid)' %optd['res_SCS']
         init_errors += 1
   if optd['years'] <= 0 or type(optd['years']) != int:
      if init_errors == 0:
         print >>error_log,'Errors in options file'
      print >>error_log,'** Input for "years" should be a positive integer'
      print >>error_log,'(current value of "%s" is invalid)' %optd['years']
      init_errors += 1
   if optd['region'] == 1 and optd['res_SCS'] == 1:
      if optd['years'] > 50:
         if init_errors == 0:
            print >>error_log,'Errors in options file'
         print >>error_log,'** Input for "years" should be less than or equal',
         print >>error_log,'to 50 for scenarios with res_SCS = 1'
         init_errors += 1
      if optd['equilibration'] < 0 or type(optd['equilibration']) != int:
         if init_errors == 0:
               print >>error_log,'Errors in options file'
         print >>error_log,\
               '** Input for "equilibration" should be an integer value'
         print >>error_log,'greater than or equal to zero',
         print >>error_log,'(current value of "%s" is invalid)' \
               %optd['equilibration']
         init_errors += 1
      if optd['equilibration'] > 10:
         if init_errors == 0:
               print >>error_log,'Errors in options file'
         print >>error_log,'** Input for "equilibration" should be less than', 
         print >>error_log,'or equal to 10'
         init_errors += 1
      if optd['runs'] <= 0 or type(optd['runs']) != int:
         if init_errors == 0:
               print >>error_log,'Errors in options file'
         print >>error_log,\
               '** Input for "runs" should be a positive integer'
         print >>error_log,\
               '(current value of "%s" is invalid)' %optd['runs']
         init_errors += 1
      if optd['runs'] > 5:
         if init_errors == 0:
               print >>error_log,'Errors in options file'
         print >>error_log,'** Input for "runs" should be less than or equal',
         print >>error_log,'to 5 for scenarios with res_SCS = 1'
         init_errors += 1
   else:
      if optd['years'] > 300:
         if init_errors == 0:
            print >>error_log,'Errors in options file'
         print >>error_log,'** Input for "years" should be less than or equal',
         print >>error_log,'to 300'
         init_errors += 1
      if optd['equilibration'] < 0 or type(optd['equilibration']) != int:
         if init_errors == 0:
               print >>error_log,'Errors in options file'
         print >>error_log,\
               '** Input for "equilibration" should be an integer value'
         print >>error_log,'greater than or equal to zero'
         print >>error_log,'(current value of "%s" is invalid)' \
               %optd['equilibration']
         init_errors += 1
      if optd['equilibration'] > 50:
         if init_errors == 0:
               print >>error_log,'Errors in options file'
         print >>error_log,'** Input for "equilibration" should be less than',
         print >>error_log,'or equal to 50, MOD BY MK 0922 16'
         init_errors += 1
      if optd['runs'] <= 0 or type(optd['runs']) != int:
         if init_errors == 0:
               print >>error_log,'Errors in options file'
         print >>error_log,\
               '** Input for "runs" should be a positive integer'
         print >>error_log,\
               '(current value of "%s" is invalid)' %optd['runs']
         init_errors += 1  
      if optd['runs'] > 100:
         if init_errors == 0:
               print >>error_log,'Errors in options file'
         print >>error_log,\
               '** Input for "runs" should be less than or equal to 100, MOD BY MK 0922 16'
         init_errors += 1  
   if optd['region'] in [0,1]:
      if optd['initial_vals'] not in [0,1]:
         if init_errors == 0:
            print >>error_log,'Errors in options file'
         print >>error_log,\
               '** Input for "initial_vals" should be either "0" or "1"'
         print >>error_log,'(current value of "%s" is invalid)' \
               %optd['initial_vals']
         init_errors += 1
   if optd['forc_hurr'] not in [0,1,2,3]:
      if init_errors == 0:
         print >>error_log,'Errors in options file'
      print >>error_log,\
            '** Input for "forc_hurr" should be either "0", "1", "2" or "3"'
      print >>error_log,'(current value of "%s" is invalid)' %optd['forc_hurr']
      init_errors += 1
   if optd['forc_hurr'] in [1,2]:
      if optd['hfreq'] <= 0 or type(optd['hfreq']) != int:
         if init_errors == 0:
            print >>error_log,'Errors in options file'
         print >>error_log,'** Input for "hfreq" should be a positive integer'
         print >>error_log,'(current value of "%s" is invalid)' %optd['hfreq']
         init_errors += 1
      if optd['hmin_cat'] not in [1,2,3,4,5]:
         if init_errors == 0:
            print >>error_log,'Errors in options file'
         print >>error_log,\
               '** Input for "hmin_cat" should be an integer in the range 1-5'
         print >>error_log,'(current value of "%s" is invalid)'%optd['hmin_cat']
         init_errors += 1
      if optd['hmax_cat'] not in [1,2,3,4,5]:
         if init_errors == 0:
            print >>error_log,'Errors in options file'
         print >>error_log,\
               '** Input for "hmax_cat" should be an integer in the range 1-5'
         print >>error_log,'(current value of "%s" is invalid)'%optd['hmax_cat']
         init_errors += 1
      if optd['hmax_cat'] < optd['hmin_cat']:
         if init_errors == 0:
            print >>error_log,'Errors in options file'
         print >>error_log,\
               '** Input for "hmax_cat" should greater than or equal to'
         print >>error_log,'the input for "hmin_cat"'
         init_errors += 1
   if optd['forc_cm'] not in [0,1,2,3]:
      if init_errors == 0:
         print >>error_log,'Errors in options file'
      print >>error_log,\
            '** Input for "forc_cm" should be either "0", "1", "2" or "3"'
      print >>error_log,'(current value of "%s" is invalid)' %optd['forc_cm']
      init_errors += 1
   if optd['forc_cm'] == 1:
      if optd['cmfreq'] <= 0 or type(optd['cmfreq']) != int:
         if init_errors == 0:
            print >>error_log,'Errors in options file'
         print >>error_log,'** Input for "cmfreq" should be a positive integer'
         print >>error_log,'(current value of "%s" is invalid)' %optd['cmfreq']
         init_errors += 1
   if optd['forc_fish'] not in [0,1,2,3]:
      if init_errors == 0:
         print >>error_log,'Errors in options file'
      print >>error_log,\
            '** Input for "forc_fish" should be either "0", "1", "2" or "3"'
      print >>error_log,'(current value of "%s" is invalid)' %optd['forc_fish']
      init_errors += 1
   if optd['forc_fish'] in [1,3]:
      if optd['region'] == 0:
         if optd['fmin_MAR'] < 0:
            if init_errors == 0:
               print >>error_log,'Errors in options file'
            print >>error_log,\
            '** Input for "fmin_MAR" should be greater than or equal to zero'
            print >>error_log,'(current value of "%s" is invalid)' \
            %optd['fmin_MAR']
            init_errors += 1
         if optd['fmax_MAR'] < 0:
            if init_errors == 0:
               print >>error_log,'Errors in options file'
            print >>error_log,\
            '** Input for "fmax_MAR" should be greater than or equal to zero'
            print >>error_log,'(current value of "%s" is invalid)' \
            %optd['fmax_MAR']
            init_errors += 1
         if optd['fmax_MAR'] < optd['fmin_MAR']:
            if init_errors == 0:
               print >>error_log,'Errors in options file'
            print >>error_log,\
               '** Input for "fmax_MAR" should greater than or equal to'
            print >>error_log,'the input for "fmin_MAR"'
            init_errors += 1
      if optd['region'] == 1:
         if optd['fmin_SCS'] < 0:
            if init_errors == 0:
               print >>error_log,'Errors in options file'
            print >>error_log,\
            '** Input for "fmin_SCS" should be greater than or equal to zero'
            print >>error_log,'(current value of "%s" is invalid)' \
            %optd['fmin_SCS']
            init_errors += 1
         if optd['fmax_SCS'] < 0:
            if init_errors == 0:
               print >>error_log,'Errors in options file'
            print >>error_log,\
            '** Input for "fmax_SCS" should be greater than or equal to zero'
            print >>error_log,'(current value of "%s" is invalid)' \
            %optd['fmax_SCS']
            init_errors += 1
         if optd['fmax_SCS'] < optd['fmin_SCS']:
            if init_errors == 0:
               print >>error_log,'Errors in options file'
            print >>error_log,\
               '** Input for "fmax_SCS" should greater than or equal to'
            print >>error_log,'the input for "fmin_SCS"'
            init_errors += 1
      if optd['region'] == 2:
         if optd['fmin_user'] < 0:
            if init_errors == 0:
               print >>error_log,'Errors in options file'
            print >>error_log,\
            '** Input for "fmin_user" should be greater than or equal to zero'
            print >>error_log,'(current value of "%s" is invalid)' \
            %optd['fmin_user']
            init_errors += 1
         if optd['fmax_user'] < 0:
            if init_errors == 0:
               print >>error_log,'Errors in options file'
            print >>error_log,\
            '** Input for "fmax_user" should be greater than or equal to zero'
            print >>error_log,'(current value of "%s" is invalid)' \
            %optd['fmax_user']
            init_errors += 1
         if optd['fmax_user'] < optd['fmin_user']:
            if init_errors == 0:
               print >>error_log,'Errors in options file'
            print >>error_log,\
               '** Input for "fmax_user" should greater than or equal to'
            print >>error_log,'the input for "fmin_user"'
            init_errors += 1
   if optd['forc_df'] not in [0,1]:
      if init_errors == 0:
         print >>error_log,'Errors in options file'
      print >>error_log,'** Input for "forc_df" should be either "0" or "1"'
      print >>error_log,'(current value of "%s" is invalid)' %optd['forc_df']
      init_errors += 1
   if optd['forc_nut'] not in [0,1,2]:
      if init_errors == 0:
         print >>error_log,'Errors in options file'
      print >>error_log,\
            '** Input for "forc_nut" should be either "0", "1" or "2"'
      print >>error_log,'(current value of "%s" is invalid)' %optd['forc_nut']
      init_errors += 1
   if optd['forc_sed'] not in [0,1,2]:
      if init_errors == 0:
         print >>error_log,'Errors in options file'
      print >>error_log,\
            '** Input for "forc_sed" should be either "0", "1" or "2"'
      print >>error_log,'(current value of "%s" is invalid)' %optd['forc_sed']
      init_errors += 1
   if init_errors > 0:
      error_log.close()
      raise SystemExit(1)
   globals().update(optd)
   
   if region == 0: 
      res = str(res_MAR) + 'km'
   elif region == 1: 
      res = str(res_SCS) + 'km'
   else: res = 'none'

   foptions = {}
   foptions['hfreq'] = hfreq; foptions['hmax_sr'] = hmax_sr
   foptions['hmin_cat'] = hmin_cat; foptions['hmax_cat'] = hmax_cat
   foptions['cmfreq'] =  cmfreq; foptions['cmmax_sr'] = cmmax_sr
   if region == 0:
      foptions['f'] = [fmin_MAR,fmax_MAR]
   elif region == 1:
      foptions['f'] = [fmin_SCS,fmax_SCS]
   else:
      foptions['f'] = [fmin_user,fmax_user]
   
   # Pathnames for input files
   filenames = {}
   if region == 0: reg = 'MAR'
   elif region == 1: reg = 'SCS'
   else: reg = 'user'
   
   if reg == 'MAR' or reg == 'SCS':
      pathmap = inputpath + reg + '_' + res + '.txt'
      if os.path.exists(pathmap) != 1:
         print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain a mapfile "%s"' \
               %(reg + '_' + res + '.txt')
         init_errors += 1
   else:
      pathmap = inputpath + reg + '_map.txt'
      if os.path.exists(pathmap) != 1:
         print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain a mapfile "%s"' \
               %(reg + '_map.txt')
         init_errors += 1
   pathsrnames = inputpath + reg + '_srnames.txt'
   if os.path.exists(pathsrnames) != 1:
      if init_errors == 0:
         print >>error_log,'Missing input files'
      print >>error_log,'** Input folder should contain a mapfile "%s"' \
            %(reg + '_srnames.txt')
      init_errors += 1

   paramfile = inputpath + reg + '_params.txt'
   if os.path.exists(paramfile) != 1:
      if init_errors == 0:
         print >>error_log,'Missing input files'
      print >>error_log,'** Input folder should contain a parameter file "%s"' \
            %(reg + '_params.txt')
      init_errors += 1
   if reg == 'MAR' or reg == 'SCS':
      if initial_vals == 0:
         ivfile = inputpath + reg + '_iv.txt'
      elif initial_vals == 1:
         ivfile = inputpath + reg + '_iv_healthy.txt'
   else:
      ivfile = inputpath + reg + '_iv.txt'
   if os.path.exists(ivfile) != 1:
      if init_errors == 0:
         print >>error_log,'Missing input files'
      print >>error_log,\
            '** Input folder should contain an initial values file "%s"' \
            %(reg + '_iv.txt')
      init_errors += 1
   filenames['paramfile'] = paramfile; filenames['ivfile'] = ivfile
   
   pathtmCs = inputpath + reg + '_matrix_coral.txt'
   pathtmF = inputpath + reg + '_matrix_fish.txt'
   pathtmU = inputpath + reg + '_matrix_urch.txt'
   if os.path.exists(pathtmCs) != 1:
      if init_errors == 0:
         print >>error_log,'Missing input files'
      print >>error_log,\
            '** Input folder should contain a matrix file for corals "%s"' \
            %(reg + '_matrix_coral.txt')
      init_errors += 1
   if os.path.exists(pathtmF) != 1:
      if init_errors == 0:
         print >>error_log,'Missing input files'
      print >>error_log,\
            '** Input folder should contain a matrix file for fish "%s"' \
            %(reg + '_matrix_fish.txt')
      init_errors += 1
   if os.path.exists(pathtmU) != 1:
      if init_errors == 0:
         print >>error_log,'Missing input files'
      print >>error_log,\
            '** Input folder should contain a matrix file for urchins "%s"' \
            %(reg + '_matrix_urch.txt')
      init_errors += 1
   if reg == 'MAR' or reg == 'SCS':
      pathtmID = inputpath + reg + '_' + res + '_cell_source.txt'
   else:
      pathtmID = inputpath + reg + '_cell_source.txt'
   if os.path.exists(pathtmID) != 1:
      if init_errors == 0:
         print >>error_log,'Missing input files'
      print >>error_log,'** Input folder should contain the file "%s"' \
            %(reg + '_cell_source.txt')
      init_errors += 1
   if init_errors > 0:
      error_log.close()
      raise SystemExit(1)
   
   if forc_cm == 3:
      if reg == 'MAR' and res != '2km':
         print >>error_log,'Forcing option errors'
         print >>error_log,'** Coral mortality option 3 can only be'
         print >>error_log,'implemented for the default MAR spatial resolution'
         print >>error_log,'(2km x 2km)'
         init_errors += 1
      if reg == 'SCS' and res != '3km':
         print >>error_log,'Forcing option errors'
         print >>error_log,'** Coral mortality option 3 can only be'
         print >>error_log,'implemented for the default SCS spatial resolution'
         print >>error_log,'(3km x 3km)'
         init_errors += 1 
   if forc_fish == 0 and forc_df == 1:
      if init_errors == 0:
         print >>error_log,'Forcing option errors'
      print >>error_log,'** Destructive fishing forcing can only be implemented'
      print >>error_log,'in combination with fishing forcing options 1 - 3'
      init_errors += 1
   if forc_df == 1 and reg == 'MAR':
      if init_errors == 0:
         print >>error_log,'Forcing option errors'
      print >>error_log,'** Destructive fishing forcing can only be implemented'
      print >>error_log,'for the Philippines/South China Sea region'
      init_errors += 1
   if forc_fish == 3:
      if reg == 'MAR' and res != '2km':
         if init_errors == 0:
            print >>error_log,'Forcing option errors'
         print >>error_log,'** Fishing forcing option 3 can only be implemented'
         print >>error_log,'for the default MAR spatial resolution'
         print >>error_log,'(2km x 2km)'
         init_errors += 1
      if reg == 'SCS' and res != '3km':
         if init_errors == 0:
            print >>error_log,'Forcing option errors'
         print >>error_log,'** Fishing forcing option 3 can only be implemented'
         print >>error_log,'for the default SCS spatial resolution'
         print >>error_log,'(3km x 3km)'
         init_errors += 1 
   if forc_nut == 2:
      if reg == 'MAR' and res != '2km':
         if init_errors == 0:
            print >>error_log,'Forcing option errors'
         print >>error_log,'** Nutrification forcing option 2 can only be'
         print >>error_log,'implemented for the default MAR spatial resolution'
         print >>error_log,'(2km x 2km)'
         init_errors += 1
      if reg == 'SCS' and res != '3km':
         if init_errors == 0:
            print >>error_log,'Forcing option errors'
         print >>error_log,'** Nutrification forcing option 2 can only be'
         print >>error_log,'implemented for the default SCS spatial resolution'
         print >>error_log,'(3km x 3km)'
         init_errors += 1 
   if forc_sed == 2:
      if reg == 'MAR' and res != '2km':
         if init_errors == 0:
            print >>error_log,'Forcing option errors'
         print >>error_log,'** Sedimentation forcing option 2 can only be'
         print >>error_log,'implemented for the default MAR spatial resolution'
         print >>error_log,'(2km x 2km)'
         init_errors += 1
      if reg == 'SCS' and res != '3km':
         if init_errors == 0:
            print >>error_log,'Forcing option errors'
         print >>error_log,'** Sedimentation forcing option 2 can only be'
         print >>error_log,'implemented for the default SCS spatial resolution'
         print >>error_log,'(3km x 3km)'
         init_errors += 1
   if init_errors > 0:
      error_log.close()
      raise SystemExit(1)
         
   if forc_nut == 1: 
      nfile = inputpath + reg + '_nutrification_1.txt'
      if os.path.exists(nfile) != 1:
         print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain the file "%s"' \
         %(reg + '_nutrification_1.txt')
         init_errors += 1
   elif forc_nut == 2: 
      nfile = inputpath + reg + '_nutrification_2.txt'
      if os.path.exists(nfile) != 1:
         print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain the file "%s"' \
         %(reg + '_nutrification_2.txt')
         init_errors += 1
   else: nfile = 'none'
   if forc_sed == 1: 
      sfile = inputpath + reg + '_sedimentation_1.txt'
      if os.path.exists(sfile) != 1:
         if init_errors == 0:
            print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain the file "%s"' \
         %(reg + '_sedimentation_1.txt')
         init_errors += 1
   elif forc_sed == 2: 
      sfile = inputpath + reg + '_sedimentation_2.txt'
      if os.path.exists(sfile) != 1:
         if init_errors == 0:
            print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain the file "%s"' \
         %(reg + '_sedimentation_2.txt')
         init_errors += 1
   else: sfile = 'none'
   if forc_hurr == 3: 
      hfile = inputpath + reg + '_hurricanes_3.txt'
      if os.path.exists(hfile) != 1:
         if init_errors == 0:
            print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain the file "%s"' \
         %(reg + '_hurricanes_3.txt')
         init_errors += 1
   else: hfile = 'none'
   if forc_cm == 2: 
      cmfile = inputpath + reg + '_coral_mortality_2.txt'
      if os.path.exists(cmfile) != 1:
         if init_errors == 0:
            print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain the file "%s"' \
         %(reg + '_coral_mortality_2.txt')
         init_errors += 1
   elif forc_cm == 3: 
      cmfile = inputpath + reg + '_coral_mortality_3.txt'
      if os.path.exists(cmfile) != 1:
         if init_errors == 0:
            print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain the file "%s"' \
         %(reg + '_coral_mortality_3.txt')
         init_errors += 1
   else: cmfile = 'none'
   if forc_df == 1: 
      dffile = inputpath + reg + '_destructive_fishing_1.txt'
      if os.path.exists(dffile) != 1:
         if init_errors == 0:
            print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain the file "%s"' \
         %(reg + '_destructive_fishing_1.txt')
         init_errors += 1
   else: dffile = 'none'
   if forc_fish == 2: 
      ffile = inputpath + reg + '_fishing_2.txt'
      if os.path.exists(ffile) != 1:
         if init_errors == 0:
            print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain the file "%s"' \
         %(reg + '_fishing_2.txt')
         init_errors += 1
   elif forc_fish == 3: 
      ffile = inputpath + reg + '_fishing_3.txt'
      if os.path.exists(ffile) != 1:
         if init_errors == 0:
            print >>error_log,'Missing input files'
         print >>error_log,'** Input folder should contain the file "%s"' \
         %(reg + '_fishing_3.txt')
         init_errors += 1
   else: ffile = 'none'
   filenames['nfile'] = nfile; filenames['sfile'] = sfile
   filenames['hfile'] = hfile; filenames['cmfile'] = cmfile
   filenames['dffile'] = paramfile; filenames['dffile'] = ivfile
   filenames['ffile'] = ffile
   if init_errors > 0:
      error_log.close()
      raise SystemExit(1)

   # Input map and subregion names
   reefmap = Map(); reefmap.reefmap(pathmap,forc_hurr,forc_cm,hmax_sr,cmmax_sr)
   init_errors += reefmap.init_errors
   if init_errors > 0:
      print >>error_log,'Map input errors'
      for errors in reefmap.error_text:
         print >>error_log,errors
      error_log.close()
      raise SystemExit(1)
   reefmap.srnames(pathsrnames)
   init_errors += reefmap.init_errors
   if init_errors > 0:
      print >>error_log,'Map input errors'
      for errors in reefmap.error_text:
         print >>error_log,errors
      error_log.close()
      raise SystemExit(1)
   
   # Input parameters and initial values
   params = Params(paramfile,region,years,equilibration,runs,seed,foptions)
   init_errors += params.init_errors
   if init_errors > 0:
      print >>error_log,'Parameter input errors'
      for errors in params.error_text:
         print >>error_log,errors
      error_log.close()
      raise SystemExit(1)
   params.initVals(ivfile,reefmap.srrange,reefmap.cell_area)
   init_errors += params.init_errors
   if init_errors > 0:
      print >>error_log,'Initial values input errors'
      for errors in params.error_text:
         print >>error_log,errors
      error_log.close()
      raise SystemExit(1)
    
   # Input and format transition matrices    
   transitionCs = Transition(); transitionF = Transition()
   transitionU = Transition(); transition = Transition()
   transitionCs.readTM(pathtmCs); transitionF.readTM(pathtmF)
   transitionU.readTM(pathtmU)
   init_errors += (transitionCs.init_errors + transitionF.init_errors +
                   transitionU.init_errors)
   if init_errors > 0:
      print >>error_log,'Transition matrix input errors'
      for errors in transitionCs.error_text:
         print >>error_log,errors
      for errors in transitionF.error_text:
         print >>error_log,errors
      for errors in transitionU.error_text:
         print >>error_log,errors
      for errors in transition.error_text:
         print >>error_log,errors
      error_log.close()
      raise SystemExit(1)
   transition.polytocell(pathtmID,reefmap.reeftotal,transitionCs.ptotal,
                         transitionF.ptotal,transitionU.ptotal)
   init_errors += transition.init_errors
   if init_errors > 0:
      print >>error_log,'Transition matrix input errors'
      for errors in transition.error_text:
         print >>error_log,errors
      error_log.close()
      raise SystemExit(1)
   transitionCs.adjustTM(transition); transitionF.adjustTM(transition)
   transitionU.adjustTM(transition)
   transition.adjustPCmap(transitionU.transition)
    
   # Instantiate forcings
   forcing_nut = Forcing(forc_nut,'nutrification')
   forcing_nut.nsSched(nfile,reefmap,years)
   forcing_sed = Forcing(forc_sed,'sedimentation')
   forcing_sed.nsSched(sfile,reefmap,years)
   forcing_hurr = Forcing(forc_hurr,'hurricanes')
   forcing_hurr.hSched(hfile,reefmap,years)
   forcing_cm = Forcing(forc_cm,'coral_mortality')
   forcing_cm.cmSched(cmfile,reefmap,years)
   forcing_f = Forcing(forc_fish,'fishing')
   forcing_f.fSched(ffile,reefmap,years)
   forcing_df = Forcing(forc_df,'destructive_fishing')
   forcing_df.dfSched(dffile,reefmap,years)
   init_errors += (forcing_nut.init_errors + forcing_sed.init_errors + 
                   forcing_hurr.init_errors + forcing_cm.init_errors + 
                   forcing_f.init_errors + forcing_df.init_errors)
   warnings = (forcing_nut.warnings + forcing_sed.warnings + 
               forcing_hurr.warnings + forcing_cm.warnings + 
               forcing_f.warnings + forcing_df.warnings)
   if init_errors > 0:
      print >>error_log,'Forcing input errors'
      for errors in forcing_nut.error_text:
         print >>error_log,errors
      for errors in forcing_sed.error_text:
         print >>error_log,errors
      for errors in forcing_hurr.error_text:
         print >>error_log,errors
      for errors in forcing_cm.error_text:
         print >>error_log,errors
      for errors in forcing_f.error_text:
         print >>error_log,errors
      for errors in forcing_df.error_text:
         print >>error_log,errors
      error_log.close()
      raise SystemExit(1)
   warning_log = open(outputpath + 'warning_log.txt','w')
   print >>warning_log,datetime.datetime.now().strftime('%d-%m-%y, %H:%M')
   #print >>warning_log,os.getenv('COMPUTERNAME')
   print >>warning_log,'\n',
   if warnings > 0:
      print >>warning_log,'Forcing input warnings'
      for warning in forcing_nut.warning_text:
         print >>warning_log,warning
      for warning in forcing_sed.warning_text:
         print >>warning_log,warning
      for warning in forcing_hurr.warning_text:
         print >>warning_log,warning
      for warning in forcing_cm.warning_text:
         print >>warning_log,warning
      for warning in forcing_f.warning_text:
         print >>warning_log,warning
      for warning in forcing_df.warning_text:
         print >>warning_log,warning
   else:
      print >>warning_log,'No warnings'
   warning_log.close()
   
   # Report zero errors
   if init_errors == 0:
      print >>error_log,'No input errors'
   error_log.close()
  
   #create the directory
   os.mkdir(outputpath + '_pickle')
  
   # Pickle inputs
   p = open(outputpath + '_pickle/scenario','w')
   pickle.dump(scenario,p); p.close()
   p = open(outputpath + '_pickle/filenames','w')
   pickle.dump(filenames,p); p.close()
   p = open(outputpath + '_pickle/reefmap','w')
   pickle.dump(reefmap,p); p.close()
   p = open(outputpath + '_pickle/params','w')
   pickle.dump(params,p); p.close()
   p = open(outputpath + '_pickle/transitionCs','w')
   pickle.dump(transitionCs,p); p.close()
   p = open(outputpath + '_pickle/transitionF','w')
   pickle.dump(transitionF,p); p.close()
   p = open(outputpath + '_pickle/transitionU','w')
   pickle.dump(transitionU,p); p.close()
   p = open(outputpath + '_pickle/transition','w')
   pickle.dump(transition,p); p.close()
   p = open(outputpath + '_pickle/forcing_nut','w')
   pickle.dump(forcing_nut,p); p.close()
   p = open(outputpath + '_pickle/forcing_sed','w')
   pickle.dump(forcing_sed,p); p.close()
   p = open(outputpath + '_pickle/forcing_hurr','w')
   pickle.dump(forcing_hurr,p); p.close()
   p = open(outputpath + '_pickle/forcing_cm','w')
   pickle.dump(forcing_cm,p); p.close()
   p = open(outputpath + '_pickle/forcing_f','w')
   pickle.dump(forcing_f,p); p.close()
   p = open(outputpath + '_pickle/forcing_df','w')
   pickle.dump(forcing_df,p); p.close()
        
def Simulate(inputpath, outputpath):
   print 'Running simulation'
   
   if(not (outputpath[-1] == '/')):
      outputpath = outputpath + "/"

   # Load pickled inputs
   p = open(outputpath + '_pickle/reefmap','r')
   reefmap = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/params','r')
   params = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/transitionCs','r')
   transitionCs=pickle.load(p); p.close()
   p = open(outputpath + '_pickle/transitionF','r')
   transitionF = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/transitionU','r')
   transitionU = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/transition','r')
   transition = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_nut','r')
   forcing_nut = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_sed','r')
   forcing_sed = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_hurr','r')
   forcing_hurr=pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_cm','r')
   forcing_cm = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_f','r')
   forcing_f = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_df','r')
   forcing_df = pickle.load(p); p.close()
   
   # Lists and dictionaries to catch model results
   defectruns = []
   mcavs = {}; mcCIs = {}; mcavsSR = {}; mcCIsSR = {}; cellavs = {}
   hlog_cat = []; hlog_sr = []; cmlog_sr = []
   for var in variables:
      mcavs[var] = []; mcCIs[var] = []; mcavsSR[var] = []; mcCIsSR[var] = []
      cellavs[var] = []
   run_names = []
   for run in range(params.runs):
      run_names.append('model' + str(run))
   
   # Run the model
   tstart = time.time()
   runs = {}
   threads = []
   for run in range(params.runs):
      runs[run_names[run]] = Simulation(reefmap,params)
      transitionCb = Transition()
      transitionCb.makeTMR(transition.pctotal,params.paramrec['dlarv_Cb'],run)
      t = threading.Thread(target=Simulation.model, args=(runs[run_names[run]],
          reefmap,params,variables,transition,
          transitionCb,transitionCs,transitionF,transitionU,
          forcing_nut,forcing_sed,forcing_hurr,
          forcing_cm,forcing_f,forcing_df,100,1,run))
      threads.append(t)
   
   if params.runs <= 1:
      for run in range(params.runs):
         threads[run].start()
      for run in range(params.runs):
         threads[run].join()
   else:
      runchunks = [range(params.runs)[i:i+1] for i in range(0,params.runs,1)]
      for chunk in runchunks:
         for run in chunk:
            threads[run].start()
         for run in chunk:
            threads[run].join()
   
   for run in range(params.runs):
      if runs[run_names[run]].errors > 0: defectruns.append(run)
      if runs[run_names[run]].errors == 0:
         for var in variables:
            mcavs[var].append(runs[run_names[run]].avs[var])
            mcCIs[var].append(runs[run_names[run]].CIs[var])
            mcavsSR[var].append(runs[run_names[run]].avsSR[var])
            mcCIsSR[var].append(runs[run_names[run]].CIsSR[var])
            cellavs[var].append(runs[run_names[run]].modelout[var][-1])
         hlog_cat.append(runs[run_names[run]].hlog_cat)
         hlog_sr.append(runs[run_names[run]].hlog_sr)
         cmlog_sr.append(runs[run_names[run]].cmlog_sr)
   tend = time.time()
   timing = tend - tstart
  
   # Pickle model results
   p = open(outputpath + '_pickle/mcavs','w'); pickle.dump(mcavs,p); p.close()
   p = open(outputpath + '_pickle/mcCIs','w'); pickle.dump(mcCIs,p); p.close()
   p = open(outputpath + '_pickle/mcavsSR','w'); pickle.dump(mcavsSR,p); p.close()
   p = open(outputpath + '_pickle/mcCIsSR','w'); pickle.dump(mcCIsSR,p); p.close()
   p = open(outputpath + '_pickle/cellavs','w'); pickle.dump(cellavs,p); p.close()
   p = open(outputpath + '_pickle/hlog_cat','w'); pickle.dump(hlog_cat,p); p.close()
   p = open(outputpath + '_pickle/hlog_sr','w'); pickle.dump(hlog_sr,p); p.close()
   p = open(outputpath + '_pickle/cmlog_sr','w'); pickle.dump(cmlog_sr,p); p.close()
   p = open(outputpath + '_pickle/defectruns','w'); pickle.dump(defectruns,p); p.close()
   p = open(outputpath + '_pickle/timing','w'); pickle.dump(timing,p); p.close()

def Outputs(inputpath,outputpath):
   print 'Generating outputs'
  
   if(not (outputpath[-1] == '/')):
      outputpath = outputpath + "/"

 
   # Load pickeled model results
   p = open(outputpath + '_pickle/scenario','r'); scenario = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/filenames','r'); filenames = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/reefmap','r'); reefmap = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/params','r'); params = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/mcavs','r'); mcavs = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/mcCIs','r'); mcCIs = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/mcavsSR','r'); mcavsSR = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/mcCIsSR','r'); mcCIsSR = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/cellavs','r'); cellavs = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_nut','r'); forcing_nut = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_sed','r'); forcing_sed = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_hurr','r'); forcing_hurr=pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_cm','r'); forcing_cm = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_f','r'); forcing_f = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/forcing_df','r'); forcing_df = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/hlog_cat','r'); hlog_cat = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/hlog_sr','r'); hlog_sr = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/cmlog_sr','r'); cmlog_sr = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/defectruns','r'); defectruns = pickle.load(p); p.close()
   p = open(outputpath + '_pickle/timing','r'); timing = pickle.load(p); p.close()
   
   # Pathnames for output files
   pathmeans = outputpath + scenario + '_means'
   pathmeansSR = outputpath + scenario + '_meansSR'
   pathspatial = outputpath + scenario + '_spatial'
   pathlog = outputpath + scenario + '_log.txt'
   pathlogF = outputpath + scenario + '_logF.txt'
   pathparamsout = outputpath + scenario + '_params.txt'
   pathoptionsout = outputpath + scenario + '_options.txt'
   
   output = Output()
   runf = params.runs - len(defectruns)
   
   # Write output files
   output.meansCSV(pathmeans,params,mcavs,runf)
   output.meansSRCSV(pathmeansSR,params,reefmap,mcavsSR,runf)
   output.spatialTXT(pathspatial,variables,params,reefmap,cellavs,100,1)
   output.meansCDF(pathmeans,reefmap,params,variables,runf,mcavs)
   output.meansSRCDF(pathmeansSR,reefmap,params,variables,runf,mcavsSR)
   output.writeLog(pathlog,version,scenario,params,reefmap,
   filenames['paramfile'],filenames['ivfile'],timing,defectruns)
   output.writeLogF(pathlogF,params,forcing_f,forcing_nut,forcing_sed,
   forcing_hurr,forcing_cm,forcing_df,
   filenames['paramfile'],filenames['ivfile'],filenames['ffile'],
   filenames['nfile'],filenames['sfile'],filenames['hfile'],
   filenames['cmfile'],filenames['dffile'],hlog_cat,hlog_sr,cmlog_sr,runf)
   #output.writeParams(pathparamsout,filenames['paramfile'])
   #output.writeParams(pathoptionsout,inputpath + '/CORSET_options.txt')
   
   # Create and save graphics
   display = Display()
   display.plotEndSR(reefmap,params,output)
   display.plotDynamics(reefmap,params,output)
   display.plotDynamicsSR(reefmap,params,output)
   display.plotCatchSR(reefmap,params,output)
   display.savePlot(outputpath,scenario)
