import datetime
import os
import csv
import numpy as N
from numpy import *
from scipy.io import netcdf
from scipy.io.netcdf import netcdf_file as Dataset

class Output:
    """Format and write model output.

       writeLog       -- Write model run log.
       writeLogF      -- Write forcing details for each model run to logF.
       writeParams    -- Output parameter file.
       meansCDF       -- Write output (averaged across all cells and runs) to 
		         netCDF file.
       meansSRCDF     -- Write output (averaged across cells within subregions  
                         and runs) to netCDF file.
       meansCSV       -- Write output (averaged across all cells) to comma 
		         delimited file for each run.
       meansSRCSV     -- Write output (averaged across cells within subregions) 
                         to comma delimited file for each run.
       spatialTXT     -- Write spatial output (averaged across runs for   
                         the final simulation year) to text files.
       """
    
    def writeLog(self,pathname,version,scenario,params,reefmap,paramfile,ivfile,
        timing,defectruns):
	"""Write model run log."""
        outfile = open(pathname, 'w')
        print >>outfile,datetime.datetime.now().strftime("%d-%m-%y, %H:%M")
	#print >>outfile,os.getenv('COMPUTERNAME')
        print >>outfile,"\nversion: " + version + ",",
	if params.region == 0:
	    print >>outfile,"region: MAR,",
	if params.region == 1:
	    print >>outfile,"region: SCS,",
	print >>outfile,"scenario: %s" %scenario
	print >>outfile,"parameter input: %s" %paramfile
	print >>outfile,"initial value input: %s" %ivfile
        print >>outfile,"cell size: %.2G square km (%.2Gkm x %.2Gkm)," \
        %(reefmap.cell_area,reefmap.cell_x,reefmap.cell_y),
	print >>outfile,"map dimensions: %dkm x %dkm" \
	%(reefmap.reefmap.shape[1]*reefmap.cell_x,
	  reefmap.reefmap.shape[0]*reefmap.cell_y)
        print >>outfile,"%d reef cells," %reefmap.reeftotal,
	print >>outfile,"%d subregions" %reefmap.srrange
	print >>outfile,"%d years," %params.years,
        print >>outfile,"%d equilibration years," %params.equilib,
	print >>outfile,"%d update timesteps per year," %params.update,
        if params.runs == 1:
            print >>outfile,"%d model run" %params.runs
        else:
            print >>outfile,"%d model runs" %params.runs
        if len(defectruns) != 0:	
	    print >>outfile, "defect runs: ",
	    for i in range(len(defectruns)):
		print >>outfile, "%d," %defectruns[i],
	    print >>outfile, "\n",         
        print >>outfile,"runtime: %d seconds" %(timing)
        outfile.close()
	
    def writeLogF(self,pathname,params,forcing_f,forcing_nut,forcing_sed,
	forcing_hurr,forcing_cm,forcing_df,pfile,ivfile,ffile,nfile,sfile,hfile,
	cmfile,dffile,hlog_cat,hlog_sr,cmlog_sr,runf):
	"""Write forcing log."""
        outfile = open(pathname, 'w')
	print >>outfile,\
	      datetime.datetime.now().strftime("%d-%m-%y, %H:%M")
	#print >>outfile,os.getenv('COMPUTERNAME')
	if forcing_f.opt == 0 and forcing_nut.opt == 0 and \
	forcing_sed.opt == 0 and forcing_hurr.opt == 0 and \
	forcing_cm.opt == 0 and forcing_df.opt == 0:
	    print >>outfile,"no forcings"
	else:
	    print >>outfile,"seed for forcings: %d" %params.seed
	    if forcing_nut.opt != 0:
		print >>outfile,"nutrification forcing (option %d)," \
		%forcing_nut.opt,
		print >>outfile,"input: %s" %nfile
	    if forcing_sed.opt != 0:
		print >>outfile,"sedimentation forcing (option %d)," \
		%forcing_sed.opt,
		print >>outfile,"input: %s" %sfile	
	    if forcing_hurr.opt == 1 or forcing_hurr.opt == 2:
		print >>outfile,"hurricane forcing (option %d)," \
		%forcing_hurr.opt,
		print >>outfile,"no input"
	    elif forcing_hurr.opt == 3:
		print >>outfile,"hurricane forcing (option %d)," \
		%forcing_hurr.opt,
		print >>outfile,"input: %s" %hfile	
	    if forcing_cm.opt == 1:
		print >>outfile,"coral mortality forcing (option %d)," \
		%forcing_cm.opt,
		print >>outfile,"no input"
	    elif forcing_cm.opt > 1:
		print >>outfile,"coral mortality forcing (option %d)," \
		%forcing_cm.opt,
		print >>outfile,"input: %s" %cmfile
	    if forcing_df.opt == 1:
		print >>outfile,"destructive fishing forcing (option %d)," \
		%forcing_f.opt,
		print >>outfile,"input: %s" %dffile
	    if forcing_f.opt == 1:
		print >>outfile,"fishing forcing (option %d)" %forcing_f.opt
	    if forcing_f.opt > 1:
		print >>outfile,"fishing forcing (option %d)," %forcing_f.opt,
		print >>outfile,"input: %s" %ffile
	    
	    for r in range(runf):
		if forcing_hurr.opt == 1 or forcing_hurr.opt == 2 or\
		   forcing_cm.opt == 1 or forcing_cm.opt == 3:
		    print >>outfile,"\nRun %d" %(r+1)
		    if forcing_hurr.opt == 1 or forcing_hurr.opt == 2:
			if len(hlog_sr[r].keys()) == 0:
			    print >>outfile,"no hurricanes"
			else:
			    for i in sort(hlog_sr[r].keys()):
				print >>outfile,"hurr: year %d" %i,
				print >>outfile,"(strength = %d)" \
				      %hlog_cat[r][i],
				if len(hlog_sr[r][i]) == 0:
				    print >>outfile,"all subregions"
				else: 
				    print >>outfile,\
				    "subregions %s" %str(sort(hlog_sr[r][i]))
		    if forcing_cm.opt == 1:
			if len(cmlog_sr[r].keys()) == 0:
			    print >>outfile,"no coral mortality events"
			else:
			    for i in sort(cmlog_sr[r].keys()):
				print >>outfile,"coral mortality: year %d" %i,
				if len(cmlog_sr[r][i]) == 0:
				    print >>outfile,"all subregions"
				else: 
				    print >>outfile,"subregions %s" \
				    %str(sort(cmlog_sr[r][i]))
		    if forcing_cm.opt == 3:
			if len(cmlog_sr[r].keys()) == 0:
			    print >>outfile,"no coral mortality events"
			else:
			    for i in sort(cmlog_sr[r].keys()):
				print >>outfile,"coral mortality: year %d" %i
		else:
		    break
        outfile.close()
    
    def writeParams(self,pathname,pfile):
	"""Output parameter file."""
	params = open(pfile,'r')
	outfile = open(pathname, 'w')
	for lines in params.readlines():
	    print >> outfile, lines,
	outfile.close()	   
	params.close()
    
    def meansCDF(self,path,reefmap,params,variables,runf,mcavs):
	"""Write output (averaged across all cells)
	to netCDF file for each model run.
	"""
        nrecs = params.years; nruns = runf

        # open a new netCDF file for writing
        pathm = path + ".nc"        
        ncfile = Dataset(pathm,'w')
        
        # output data
	self.outavs = {}; self.outCIs = {}
	for var in variables:
	    self.outavs[var] = []; self.outCIs[var] = []
	for i in range(params.years):
	    calcben = {}; calccon = {}
	    for var in ['C','Cb','Cs','T','M','E']:
		calcben[var] = []
		for r in range(runf):
		    calcben[var].append(mcavs[var][r][i])
		self.outavs[var].append(round(mean(calcben[var]),2))
		self.outCIs[var].append([round((self.outavs[var][-1] 
	        - 1.96*std(calcben[var])),2),round((self.outavs[var][-1] 
		+ 1.96*std(calcben[var])),2)])
		if self.outCIs[var][-1][0] < 0: self.outCIs[var][-1][0] = 0
	        if self.outCIs[var][-1][1] > 100: self.outCIs[var][-1][1] = 100
	    for var in ['H','Ps','Pl','U','catchH','catchPs','catchPl']:
		calccon[var] = []
		for r in range(runf):
		    calccon[var].append(mcavs[var][r][i])
		self.outavs[var].append(round(mean(calccon[var]),2))
		self.outCIs[var].append([round((self.outavs[var][-1] 
	        - 1.96*std(calccon[var])),2),round((self.outavs[var][-1] 
		+ 1.96*std(calccon[var])),2)])
		if self.outCIs[var][-1][0] < 0: self.outCIs[var][-1][0] = 0
	    
        # create dimensions
        ncfile.createDimension('Year',nrecs)
	ncfile.createDimension('CI',2)
        
        # create variables 
        C_av = ncfile.createVariable('Coral','d',('Year',))
        Cb_av = ncfile.createVariable('Brooding_coral','d',('Year',))
        Cs_av = ncfile.createVariable('Spawning_coral','d',('Year',))
        T_av = ncfile.createVariable('Macroturf','d',('Year',))
        M_av = ncfile.createVariable('Macroalgae','d',('Year',))
        E_av = ncfile.createVariable('EAC','d',('Year',))
        H_av = ncfile.createVariable('Herbivores','d',('Year',))
        Ps_av = ncfile.createVariable('Small_piscivores','d',('Year',))
        Pl_av = ncfile.createVariable('Large_piscivores','d',('Year',))
        U_av = ncfile.createVariable('Urchins','d',('Year',))
	catchH_av = ncfile.createVariable('Herbivore_catch','d',('Year',))
        catchPs_av = ncfile.createVariable('Small_piscivore_catch','d',
	('Year',))
	catchPl_av = ncfile.createVariable('Large_piscivore_catch','d',
	('Year',))
        C_CI = ncfile.createVariable('Coral_CI','d',('Year','CI'))
        Cb_CI = ncfile.createVariable('Brooding_coral_CI','d',('Year','CI'))
        Cs_CI = ncfile.createVariable('Spawning_coral_CI','d',('Year','CI'))
        T_CI = ncfile.createVariable('Macroturf_CI','d',('Year','CI'))
        M_CI = ncfile.createVariable('Macroalgae_CI','d',('Year','CI'))
        E_CI = ncfile.createVariable('EAC_CI','d',('Year','CI'))
        H_CI = ncfile.createVariable('Herbivores_CI','d',('Year','CI'))
        Ps_CI = ncfile.createVariable('Small_piscivores_CI','d',('Year','CI'))
        Pl_CI = ncfile.createVariable('Large_piscivores_CI','d',('Year','CI'))
        U_CI = ncfile.createVariable('Urchins_CI','d',('Year','CI'))
        catchH_CI = ncfile.createVariable('Herbivore_catch_CI','d',
	('Year','CI'))
	catchPs_CI = ncfile.createVariable('Small_piscivore_catch_CI','d',
	('Year','CI'))
        catchPl_CI = ncfile.createVariable('Large_piscivore_catch_CI','d',
	('Year','CI'))
	
        # set the units attribute
        for i in [C_av, Cb_av, Cs_av, T_av, M_av, E_av,
		  C_CI, Cb_CI, Cs_CI, T_CI, M_CI, E_CI]:
            i.units = 'Cover (%)'
        for i in [H_av, Ps_av, Pl_av, U_av, H_CI, Ps_CI, Pl_CI, U_CI,
		  catchH_av, catchPs_av, catchPl_av,
		  catchH_CI, catchPs_CI, catchPl_CI]:
            i.units = 'Biomass (kg/km^2)'
	    
        # write data to variables
        for i in range(nrecs):
	    C_av[i] = self.outavs['C'][i]
	    Cb_av[i] = self.outavs['Cb'][i]
	    Cs_av[i] = self.outavs['Cs'][i]
	    T_av[i] = self.outavs['T'][i]
	    M_av[i] = self.outavs['M'][i]
	    E_av[i] = self.outavs['E'][i]
	    H_av[i] = self.outavs['H'][i]
	    Ps_av[i] = self.outavs['Ps'][i]
	    Pl_av[i] = self.outavs['Pl'][i]
	    U_av[i] = self.outavs['U'][i]
	    catchH_av[i] = self.outavs['catchH'][i]
	    catchPs_av[i] = self.outavs['catchPs'][i]
	    catchPl_av[i] = self.outavs['catchPl'][i]
            C_CI[i] = self.outCIs['C'][i]
	    Cb_CI[i] = self.outCIs['Cb'][i]
	    Cs_CI[i] = self.outCIs['Cs'][i]
	    T_CI[i] = self.outCIs['T'][i]
	    M_CI[i] = self.outCIs['M'][i]
	    E_CI[i] = self.outCIs['E'][i]
	    H_CI[i] = self.outCIs['H'][i]
	    Ps_CI[i] = self.outCIs['Ps'][i]
	    Pl_CI[i] = self.outCIs['Pl'][i]
	    U_CI[i] = self.outCIs['U'][i]
	    catchH_CI[i] = self.outCIs['catchH'][i]
	    catchPs_CI[i] = self.outCIs['catchPs'][i]
	    catchPl_CI[i] = self.outCIs['catchPl'][i]
        
        # close the file
        ncfile.close()
    	
    def meansSRCDF(self,path,reefmap,params,variables,runf,mcavsSR):
	"""Write output (averaged across cells within subregions)
	to netCDF file for each model run.
	"""
        nrecs = params.years; nruns = runf
	nsubregs = int(reefmap.srrange)

        # open a new netCDF file for writing
        pathm = path + ".nc"        
        ncfile = Dataset(pathm,'w')
        
        # output data
	self.outavsSR = {}; self.outCIsSR = {}
	for var in variables:
	    self.outavsSR[var] = [[] for sr in range(nsubregs)]
	    self.outCIsSR[var] = [[] for sr in range(nsubregs)]
	for sr in range(nsubregs):
	    for i in range(params.years):
		calcben = {}; calccon = {}
	        for var in ['C','Cb','Cs','T','M','E']:
		    calcben[var] = []
		    for r in range(runf):
			calcben[var].append(mcavsSR[var][r][sr][i])
		    self.outavsSR[var][sr].append(round(mean(calcben[var]),2))
		    self.outCIsSR[var][sr].append([round((self.outavsSR[var]
		    [sr][-1]-1.96*std(calcben[var])),2),round((self.outavsSR
		    [var][sr][-1]+1.96*std(calcben[var])),2)])
		    if self.outCIsSR[var][sr][-1][0] < 0:
			self.outCIsSR[var][sr][-1][0] = 0
		    if self.outCIsSR[var][sr][-1][1] > 100:
			self.outCIsSR[var][sr][-1][1] = 100
		for var in ['H','Ps','Pl','U','catchH',
			'catchPs','catchPl']:
		    calccon[var] = []
		    for r in range(runf):
			calccon[var].append(mcavsSR[var][r][sr][i])
		    self.outavsSR[var][sr].append(round(mean(calccon[var]),2))
		    self.outCIsSR[var][sr].append([round((self.outavsSR[var]
		    [sr][-1]-1.96*std(calccon[var])),2),round((self.outavsSR
		    [var][sr][-1]+1.96*std(calccon[var])),2)])
		    if self.outCIsSR[var][sr][-1][0] < 0:
			self.outCIsSR[var][sr][-1][0] = 0
        
        # create dimensions
        ncfile.createDimension('Subregion',nsubregs)
        ncfile.createDimension('Year',nrecs)
	ncfile.createDimension('CI',2)	
        
        # create variables 
        C_avSR = ncfile.createVariable('Coral','d',('Subregion','Year'))
        Cb_avSR = ncfile.createVariable('Brooding_coral','d',
                ('Subregion','Year'))
        Cs_avSR = ncfile.createVariable('Spawning_coral','d',
                ('Subregion','Year'))
        T_avSR = ncfile.createVariable('Macroturf','d',('Subregion','Year'))
        M_avSR = ncfile.createVariable('Macroalgae','d',('Subregion','Year'))
        E_avSR = ncfile.createVariable('EAC','d',('Subregion','Year'))
        H_avSR = ncfile.createVariable('Herbivores','d',('Subregion','Year'))
        Ps_avSR = ncfile.createVariable('Small_piscivores','d',
                ('Subregion','Year'))
        Pl_avSR = ncfile.createVariable('Large_piscivores','d',
                ('Subregion','Year'))
        U_avSR = ncfile.createVariable('Urchin','d',('Subregion','Year'))
	catchH_avSR = ncfile.createVariable('Herbivore_catch','d',
                ('Subregion','Year'))
        catchPs_avSR = ncfile.createVariable('Small_piscivore_catch','d',
                ('Subregion','Year'))
        catchPl_avSR = ncfile.createVariable('Large_piscivore_catch','d',
                ('Subregion','Year'))
        C_CISR = ncfile.createVariable('Coral_CI','d',
		('Subregion','Year','CI'))
        Cb_CISR = ncfile.createVariable('Brooding_coral_CI','d',
                ('Subregion','Year','CI'))
        Cs_CISR = ncfile.createVariable('Spawning_coral_CI','d',
                ('Subregion','Year','CI'))
        T_CISR = ncfile.createVariable('Macroturf_CI','d',
                ('Subregion','Year','CI'))
        M_CISR = ncfile.createVariable('Macroalgae_CI','d',
                ('Subregion','Year','CI'))
        E_CISR = ncfile.createVariable('EAC_CI','d',
                ('Subregion','Year','CI'))
        H_CISR = ncfile.createVariable('Herbivores_CI','d',
                ('Subregion','Year','CI'))
        Ps_CISR = ncfile.createVariable('Small_piscivores_CI','d',
                ('Subregion','Year','CI'))
        Pl_CISR = ncfile.createVariable('Large_piscivores_CI','d',
                ('Subregion','Year','CI'))
        U_CISR = ncfile.createVariable('Urchin_CI','d',
                ('Subregion','Year','CI'))
        catchH_CISR = ncfile.createVariable('Herbivore_catch_CI','d',
                ('Subregion','Year','CI'))
        catchPs_CISR = ncfile.createVariable('Small_piscivore_catch_CI','d',
                ('Subregion','Year','CI'))
        catchPl_CISR = ncfile.createVariable('Large_piscivore_catch_CI','d',
                ('Subregion','Year','CI'))
	
        # set the units attribute
        for i in [C_avSR, Cb_avSR, Cs_avSR, T_avSR,M_avSR, E_avSR, 
		  C_CISR, Cb_CISR, Cs_CISR, T_CISR, M_CISR, E_CISR]:
            i.units = 'Cover (%)'
        for i in [H_avSR, Ps_avSR, Pl_avSR, U_avSR,
		  H_CISR, Ps_CISR, Pl_CISR, U_CISR,
		  catchH_avSR, catchPs_avSR, catchPl_avSR,
		  catchH_CISR, catchPs_CISR, catchPl_CISR]:
            i.units = 'Biomass (kg/km^2)'
        
        # write data to variables
        for sr in range(nsubregs):
	    C_avSR[sr] = self.outavsSR['C'][sr]
	    Cb_avSR[sr] = self.outavsSR['Cb'][sr]
	    Cs_avSR[sr] = self.outavsSR['Cs'][sr]
	    T_avSR[sr] = self.outavsSR['T'][sr]
	    M_avSR[sr] = self.outavsSR['M'][sr]
	    E_avSR[sr] = self.outavsSR['E'][sr]
	    H_avSR[sr] = self.outavsSR['H'][sr]
	    Ps_avSR[sr] = self.outavsSR['Ps'][sr]
	    Pl_avSR[sr] = self.outavsSR['Pl'][sr]
	    U_avSR[sr] = self.outavsSR['U'][sr]
	    catchH_avSR[sr] = self.outavsSR['catchH'][sr]
	    catchPs_avSR[sr] = self.outavsSR['catchPs'][sr]
	    catchPl_avSR[sr] = self.outavsSR['catchPl'][sr]
	    C_CISR[sr] = self.outCIsSR['C'][sr]
	    Cb_CISR[sr] = self.outCIsSR['Cb'][sr]
	    Cs_CISR[sr] = self.outCIsSR['Cs'][sr]
	    T_CISR[sr] = self.outCIsSR['T'][sr]
	    M_CISR[sr] = self.outCIsSR['M'][sr]
	    E_CISR[sr] = self.outCIsSR['E'][sr]
	    H_CISR[sr] = self.outCIsSR['H'][sr]
	    Ps_CISR[sr] = self.outCIsSR['Ps'][sr]
	    Pl_CISR[sr] = self.outCIsSR['Pl'][sr]
	    U_CISR[sr] = self.outCIsSR['U'][sr]
	    catchH_CISR[sr] = self.outCIsSR['catchH'][sr]
	    catchPs_CISR[sr] = self.outCIsSR['catchPs'][sr]
	    catchPl_CISR[sr] = self.outCIsSR['catchPl'][sr]
        
        # close the file
        ncfile.close()
	
    def meansCSV(self,path,params,mcavs,runf):
	"""Write output (averaged across all cells) to comma 
	   delimited file for each run.
	"""
	pathm = path + ".csv"        
        outm = csv.writer(open(pathm,'wb'), delimiter=',')
	for r in range (runf):
	    if r == 0:
		outm.writerow(['Run','Year','Coral','Macroturf','Macroalgae',
			      'EAC','Herbivores','Small piscivores', 
			      'Large piscivores','Urchins','Herbivore catch',
			      'Small piscivore catch','Large piscivore catch'])
	    for i in range(params.years):
		outm.writerow([r+1,i+1,mcavs['C'][r][i],mcavs['T'][r][i],
			      mcavs['M'][r][i],mcavs['E'][r][i],
			      mcavs['H'][r][i],mcavs['Ps'][r][i],
			      mcavs['Pl'][r][i],mcavs['U'][r][i],
			      mcavs['catchH'][r][i],mcavs['catchPs'][r][i],
			      mcavs['catchPl'][r][i]])
	    
    def meansSRCSV(self,path,params,reefmap,mcavsSR,runf):
	"""Write output (averaged across cells within subregions) 
	   to comma delimited file for each run.
	"""
	pathm = path + ".csv"        
        outm = csv.writer(open(pathm,'wb'), delimiter=',')
	for r in range (runf):
	    if r == 0:
		outm.writerow(['Run','Subregion','Year','Coral','Macroturf',
			    'Macroalgae','EAC','Herbivores','Small piscivores',
			    'Large piscivores','Urchins','Herbivore catch',
			    'Small piscivore catch','Large piscivore catch'])
	    for sr in range(reefmap.srrange):
		for i in range(params.years):
		    outm.writerow([r+1,sr+1,i+1,mcavsSR['C'][r][sr][i],
		      mcavsSR['T'][r][sr][i],mcavsSR['M'][r][sr][i],
		      mcavsSR['E'][r][sr][i],mcavsSR['H'][r][sr][i],
		      mcavsSR['Ps'][r][sr][i],mcavsSR['Pl'][r][sr][i],
		      mcavsSR['U'][r][sr][i],mcavsSR['catchH'][r][sr][i],
		      mcavsSR['catchPs'][r][sr][i],
		      mcavsSR['catchPl'][r][sr][i]])		
	
    def spatialTXT(self,path,variables,params,reefmap,cellavs,sc_ben,sc_con):
	"""Write spatial output (averaged across runs for   
	   the final simulation year) to text files.
	"""
	paths = [path+'_coral.txt',path+'_macroturf.txt',path+'_macroalgae.txt',
		 path+'_EAC.txt',path+'_herbivores.txt',
		 path+'_smpiscivores.txt',path+'_lgpiscivores.txt',
		 path+'_urchins.txt',path+'_hcatch.txt',path+'_smpcatch.txt',
		 path+'_lgpcatch.txt']        
	self.cellavs = {}
	newvariables = variables[:]
	newvariables.remove('Cb'); newvariables.remove('Cs')
	for var in newvariables:
	    self.cellavs[var] = []
	for cell in range(len(cellavs['C'][0])):
	    calcben = {}; calccon = {}
	    for var in ['C','T','M','E']:
		calcben[var] = []
		for r in range(len(cellavs['C'])):
		    calcben[var].append(cellavs[var][r][cell]*sc_ben)
		self.cellavs[var].append(round(mean(calcben[var]),2))
	    for var in ['H','Ps','Pl','U','catchH',
			'catchPs','catchPl']:
		calccon[var] = []
		for r in range(len(cellavs['C'])):
		    calccon[var].append(cellavs[var][r][cell]*sc_con)
		self.cellavs[var].append(round(mean(calccon[var]),2))
	for p in range(len(paths)):
	    outs = open(paths[p],'w')
	    if params.region == 0:
		if reefmap.cell_area == 1:
		    print >>outs,'ncols         326'
		    print >>outs,'nrows         631'
		    print >>outs,'xllcorner     307316.369'
		    print >>outs,'yllcorner     1751552.92'
		    print >>outs,'cellsize      1000'
		    print >>outs,'NODATA_value  -9999'
		elif reefmap.cell_area == 4:
		    print >>outs,'ncols         163'
		    print >>outs,'nrows         316'
		    print >>outs,'xllcorner     307316.369'
		    print >>outs,'yllcorner     1751552.92'
		    print >>outs,'cellsize      2000'
		    print >>outs,'NODATA_value  -9999'
	    elif params.region == 1:
		if reefmap.cell_area == 1:
		    print >>outs,'ncols         1163'
		    print >>outs,'nrows         1465'
		    print >>outs,'xllcorner     112'
		    print >>outs,'yllcorner     7.45'
		    print >>outs,'cellsize      0.00778'
		    print >>outs,'NODATA_value  -9999'
		elif reefmap.cell_area == 9:
		    print >>outs,'ncols         388'
		    print >>outs,'nrows         489'
		    print >>outs,'xllcorner     112'
		    print >>outs,'yllcorner     7.45'
		    print >>outs,'cellsize      0.0233'
		    print >>outs,'NODATA_value  -9999'
	    for ii in range(reefmap.length):
		for jj in range(reefmap.width):
		    if reefmap.reefmap[ii,jj] != 0.0:
			print >>outs,self.cellavs[newvariables[p]].pop(0),
		    else:
			print >>outs,-9999,
		    if jj == reefmap.width - 1:
			print >>outs,'\n',
	    outs.close()
	    