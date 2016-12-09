from numpy import *
from random import *
import copy
from Parameters import *
from Forcing import *   

class Simulation:
    """model      -- Run the local model for each reef cell in the base-map.
                     Calculate recruitment according to transition matrices.
                     Apply forcings.
       averages   -- Calculate averages and confidence intervals across all  
                     cells at each timestep.
       averagesSR -- Calculate averages and confidence intervals across all  
                     cells within a subregion at each timestep.
    """

    def __init__(self,reefmap,params):
	"""C  -- coral cover (proportion: sum of brooding and spawning corals)
          Cb -- brooding coral cover (proportion)
          Cs -- spawning coral cover (proportion)
          T  -- macroturf cover (proportion)
          M  -- macroalgal cover (proportion)
          E  -- epilithic algal community (EAC) cover (proportion)
          H  -- herbivorous fish biomass (kg/cell)
          Ps -- small piscivorous fish biomass (kg/cell)
          Pl -- large piscivorous fish biomass (kg/cell)
          U  -- urchin biomass (kg/cell)
       
          params   -- dictionary of parameters
          nut      -- dictionary of nutrification forcing parameters
          sed      -- dictionary of sedimentation forcing parameters
          hlog_sr  -- log of subregions affected by hurricanes (dictionary)
          hlog_cat -- log of hurricane severity (dictionary)
          cmlog_sr -- log of subregions affected by coral mortality (dictionary)
	  
	  rec0Cb,rec0Cs,rec0H,rec0P,rec0U
          -- lists to track the number of arriving recruits (year 0)
             per cell for each year
       
          rec1Cb,rec1Cs,rec1H,rec1P,rec1U
          -- lists to track the number of surviving recruits (year 1)
             per cell for each year
	     
	  catchH,catchPs,catchPl
          -- lists to track fish catches
        """
	
        self.params = params.paramlist.copy()
        self.paramscaled = params.paramscaled.copy()
        self.errors = 0
        
        # Calculate parameters that are scale dependent 
        # and update the parameter list
        params.paramScale(self.paramscaled,reefmap.cell_area)
        self.params.update(self.paramscaled)
        self.params.update(params.paramrec)
        self.params.update(params.paramforc)
        self.nut = {}
        self.sed = {}
        
        # Set up output logs for forcings
        self.hlog_sr = {}
        self.hlog_cat = {}
        self.cmlog_sr = {}
        
        # Set initial conditions
	self.C = [[]]; self.Cb = [[]]; self.Cs = [[]]; self.T = [[]]
        self.E = [[]]; self.M = [[]]; self.H = [[]]; self.Ps = [[]]
        self.Pl = [[]]; self.U = [[]]
	self.catchH = [[0 for r in range(reefmap.reeftotal)]]
	self.catchPs = [[0 for r in range(reefmap.reeftotal)]]
	self.catchPl = [[0 for r in range(reefmap.reeftotal)]]
        self.rec0Cb = [[0 for r in range(reefmap.reeftotal)]]
	self.rec0Cs = [[0 for r in range(reefmap.reeftotal)]]
	self.rec0H = [[0 for r in range(reefmap.reeftotal)]]
	self.rec0P = [[0 for r in range(reefmap.reeftotal)]] 
        self.rec0U = [[0 for r in range(reefmap.reeftotal)]]
        self.rec1Cb = [[0 for r in range(reefmap.reeftotal)]]
	self.rec1Cs = [[0 for r in range(reefmap.reeftotal)]]
	self.rec1H = [[0 for r in range(reefmap.reeftotal)]]
	self.rec1P = [[0 for r in range(reefmap.reeftotal)]] 
        self.rec1U = [[0 for r in range(reefmap.reeftotal)]]
        for r in range(reefmap.reeftotal):
            for i in range(reefmap.srrange+1)[1:]:
                if reefmap.subregid[r] == i:
                    self.Cb[0].append(params.init_vals[i-1]['Cb'])
                    self.Cs[0].append(params.init_vals[i-1]['Cs'])
                    self.C[0].append(self.Cb[0][r]+ self.Cs[0][r])
                    self.T[0].append(params.init_vals[i-1]['T'])
                    self.M[0].append(params.init_vals[i-1]['M'])
                    self.E[0].append(1 - params.init_vals[i-1]['Cb']
                    - params.init_vals[i-1]['Cs'] 
                    - params.init_vals[i-1]['T']
                    - params.init_vals[i-1]['M'])
                    self.H[0].append(params.init_vals[i-1]['H'])
                    self.Ps[0].append(params.init_vals[i-1]['Ps'])
                    self.Pl[0].append(params.init_vals[i-1]['Pl'])
                    self.U[0].append(params.init_vals[i-1]['U'])
                
    def model(self,reefmap,params,variables,transition,transitionCb,
        transitionCs,transitionF,transitionU,forcing_nut,forcing_sed,
	forcing_hurr,forcing_cm,forcing_f,forcing_df,sc_ben,sc_con,run):
	"""Run the local model for each reef cell in the base-map.
	   Calculate recruitment according to transition matrices.
	   Apply forcings.
	   
	   reproCb,reproCs,reproH,reproPs,reproPl,reproU
           -- lists to catch reproductive output for each transition polygon
       
           recruitsCb,recruitsCs,recruitsH,recruitsP,recruitsU  
           -- lists to catch recruits for each transition polygon
	"""
        
        p_cells = {}
        if params.pmethod == 0:
            self.p = params.calcParams(self.params,reefmap.cell_area,run)

        # Ensure some initial recruitment
        self.reproCb = [0 for p in range(transition.pctotal)]
        self.reproCs = [0 for p in range(transition.pctotal)]
        self.reproH = [0 for p in range(transition.pctotal)]
        self.reproPs = [0 for p in range(transition.pctotal)]
        self.reproPl = [0 for p in range(transition.pctotal)]
        self.reproU = [0 for p in range(transition.pctotal)]
        for r in range(reefmap.reeftotal):
            self.reproCb[transition.pc_map[r]] += self.params['l_C'][0]\
            *params.update*self.Cb[0][r]*reefmap.cell_area
            self.reproCs[transition.pc_map[r]] += self.params['l_C'][0]\
            *params.update*self.Cs[0][r]*reefmap.cell_area
            self.reproH[transition.pc_map[r]] += \
            self.params['l_H'][0]*params.update*self.H[0][r]
            self.reproPs[transition.pc_map[r]] += \
            self.params['l_Ps'][0]*params.update*self.Ps[0][r]
            self.reproPl[transition.pc_map[r]] += \
            self.params['l_Pl'][0]*params.update*self.Pl[0][r]
            self.reproU[transition.pc_map[r]] += \
            self.params['l_U'][0]*params.update*self.U[0][r]
        
        for i in range(params.years+params.equilib):
            year = i - (params.equilib - 1)
	    self.C.append([]); self.Cb.append([]); self.Cs.append([])
	    self.T.append([]); self.E.append([]); self.M.append([])
	    self.H.append([]); self.Ps.append([]) 
	    self.Pl.append([]); self.U.append([])
	    self.rec0Cb.append([]); self.rec0Cs.append([])
	    self.rec0H.append([]); self.rec0P.append([])
	    self.rec0U.append([])
	    self.rec1Cb.append([]); self.rec1Cs.append([])
	    self.rec1H.append([]); self.rec1P.append([])
	    self.rec1U.append([])
	    self.catchH.append([]); self.catchPs.append([])
	    self.catchPl.append([])
            
            if params.pmethod == 2:
                self.p = params.calcParams(self.params,reefmap.cell_area,run,i)
            
            # Calculate recruits for each year
            self.recruitsCb = [0 for p in range(transition.pctotal)]
            self.recruitsCs = [0 for p in range(transition.pctotal)]
            self.recruitsH = [0 for p in range(transition.pctotal)]
            self.recruitsP = [0 for p in range(transition.pctotal)]
            self.recruitsU = [0 for p in range(transition.pctotal)]
            for p in range(transition.pctotal):
                disperseCb = self.reproCb[p]*transitionCb.transition[p]
                disperseCs = self.reproCs[p]*transitionCs.transition[p]
                disperseH = self.reproH[p]*transitionF.transition[p]
                dispersePs = self.reproPs[p]*transitionF.transition[p]
                dispersePl = self.reproPl[p]*transitionF.transition[p]
                disperseP = self.reproPs[p]*transitionF.transition[p]\
                           + self.reproPl[p]*transitionF.transition[p]
                disperseU = self.reproU[p]*transitionU.transition[p]
                self.recruitsCb += disperseCb
                self.recruitsCs += disperseCs
                self.recruitsH += disperseH
                self.recruitsP += disperseP
                self.recruitsU += disperseU
		
            # Additional recruitment from external sources
            if transitionCs.ext_num > 0:        
                ext_reproCs = mean(self.reproCs)/transitionCs.ext_num
                disperseCs = ext_reproCs*transitionCs.ext_source
                self.recruitsCs += disperseCs
            if transitionF.ext_num > 0:
                ext_reproH = mean(self.reproH)/transitionF.ext_num
                ext_reproPs = mean(self.reproPs)/transitionF.ext_num
                ext_reproPl = mean(self.reproPl)/transitionF.ext_num
                disperseH = ext_reproH*transitionF.ext_source
                dispersePs = ext_reproPs*transitionF.ext_source
                dispersePl = ext_reproPl*transitionF.ext_source
                disperseP = ext_reproPs*transitionF.ext_source\
                             + ext_reproPl*transitionF.ext_source
                self.recruitsH += disperseH
                self.recruitsP += disperseP
            if transitionU.ext_num > 0:    
                ext_reproU = mean(self.reproU)/transitionU.ext_num
                disperseU = ext_reproU*transitionU.ext_source
                self.recruitsU += disperseU
            self.recruitsCb = list(self.recruitsCb)
            self.recruitsCs = list(self.recruitsCs)
            self.recruitsH = list(self.recruitsH)
            self.recruitsP = list(self.recruitsP)
            self.recruitsU = list(self.recruitsU)
            
            # Assign reef cells affected by nutrient and sediment forcings
            if forcing_nut.opt == 1:
                if year in forcing_nut.sched.keys():
                    forcing_nut.nsforcID(reefmap,year)
                    forcid_nut = forcing_nut.forcid
                else: forcid_nut = [0 for cell in range(reefmap.reeftotal)]
            elif forcing_nut.opt == 2:
                if year in forcing_nut.sched.keys():
                    forcid_nut = forcing_nut.sched[year]
                else: forcid_nut = [0 for cell in range(reefmap.reeftotal)]
            else: forcid_nut = [0 for cell in range(reefmap.reeftotal)]
            
            if forcing_sed.opt == 1:
                if year in forcing_sed.sched.keys():
                    forcing_sed.nsforcID(reefmap,year)
                    forcid_sed = forcing_sed.forcid
                else: forcid_sed = [0 for cell in range(reefmap.reeftotal)]
            elif forcing_sed.opt == 2:
                if year in forcing_sed.sched.keys():
                    forcid_sed = forcing_sed.sched[year]
                else: forcid_sed = [0 for cell in range(reefmap.reeftotal)]
            else: forcid_sed = [0 for cell in range(reefmap.reeftotal)]
            
            # Assign reef cells affected by hurricane forcing
            if forcing_hurr.opt == 1 or forcing_hurr.opt == 2:            
                if year > 1: 
                    #seed(params.seed)
                    seed(params.seed + run)
                    for s in range(i):
                        rand = random()
                    if rand > 1 - (1/self.p['hfreq']):
                        forcing_hurr.hforcID(reefmap,self.p['hmax_sr'],
                        self.p['hmin_cat'],self.p['hmax_cat'],params.years,year)
                        forcid_hurr = forcing_hurr.forcid
                        self.hlog_sr[year] = forcing_hurr.rand_sr
                        self.hlog_cat[year] = forcing_hurr.strength
                    else: forcid_hurr = [0 for cell in range(reefmap.reeftotal)]
                else: forcid_hurr = [0 for cell in range(reefmap.reeftotal)]
            elif forcing_hurr.opt == 3:
                if year in forcing_hurr.sched.keys():
                    forcid_hurr = forcing_hurr.sched[year]
                else: forcid_hurr = [0 for cell in range(reefmap.reeftotal)]
            else: forcid_hurr = [0 for cell in range(reefmap.reeftotal)]           
            
            # Assign reef cells affected by coral mortality forcing
            if forcing_cm.opt == 1:            
                if year > 1:
                    #seed(params.seed)
                    seed((params.seed + 0.001)*100 + run + 1)
                    for s in range(i):
                        rand = random()
                    if rand > 1 - (1/self.p['cmfreq']):
                        forcing_cm.cmforcID(reefmap,self.p['cmmax_sr'])
                        forcid_cm = forcing_cm.forcid
                        self.cmlog_sr[year] = forcing_cm.rand_sr
                    else: forcid_cm = [0 for cell in range(reefmap.reeftotal)]
                else: forcid_cm = [0 for cell in range(reefmap.reeftotal)]
            elif forcing_cm.opt == 2:
                if i == 0:
                    cm_C = copy.copy(forcing_cm.cm_C)
                if year in forcing_cm.sched.keys():
		    cm = cm_C.pop(0)
                    forcid_cm = forcing_cm.sched[year]
                else: forcid_cm = [0 for cell in range(reefmap.reeftotal)]
            elif forcing_cm.opt == 3:
                if year > 1:
                    #seed(params.seed)
                    seed((params.seed + 0.001)*100 + run + 1)
                    for s in range(i):
                        rand = random()
                    if rand > 1 - (1/self.p['cmfreq']):
                        forcing_cm.cmforcID(reefmap,self.p['cmmax_sr'])
                        forcid_cm = forcing_cm.forcid
                        self.cmlog_sr[year] = forcing_cm.rand_sr
                    else: forcid_cm = [0 for cell in range(reefmap.reeftotal)]
                else: forcid_cm = [0 for cell in range(reefmap.reeftotal)]
            else: forcid_cm = [0 for cell in range(reefmap.reeftotal)]
            
            # Assign reef cells affected by destructive fishing forcing
            if forcing_df.opt == 1:
                if year in forcing_df.sched.keys():
                    forcing_df.dfforcID(reefmap,year)
                    forcid_df = forcing_df.forcid
                else: forcid_df = [0 for cell in range(reefmap.reeftotal)]
            else: forcid_df = [0 for cell in range(reefmap.reeftotal)]
            
            # Set reproductive output back to zero        
            self.reproCb = [0 for p in range(transition.pctotal)]
            self.reproCs = [0 for p in range(transition.pctotal)]
            self.reproH = [0 for p in range(transition.pctotal)]
            self.reproPs = [0 for p in range(transition.pctotal)]
            self.reproPl = [0 for p in range(transition.pctotal)]
            self.reproU = [0 for p in range(transition.pctotal)]
            
            # Set recruits to zero
            recCb = [0 for r in range(reefmap.reeftotal)]
            recCs = [0 for r in range(reefmap.reeftotal)]
            recH = [0 for r in range(reefmap.reeftotal)]
            recP = [0 for r in range(reefmap.reeftotal)]
            recU = [0 for r in range(reefmap.reeftotal)]
            
            # Reset updating variables
            C = [self.C[i]]; Cb = [self.Cb[i]]; Cs = [self.Cs[i]]
            T = [self.T[i]]; M = [self.M[i]]; E = [self.E[i]]
            H = [self.H[i]]; Ps = [self.Ps[i]]; Pl = [self.Pl[i]]
            U = [self.U[i]] 
	    C.append([]); Cb.append([]); Cs.append([])
	    T.append([]); M.append([]); E.append([])
	    H.append([]); Ps.append([]); Pl.append([])
	    U.append([])
            
            # Yearly catches
            catchH = [0 for r in range(reefmap.reeftotal)]
            catchPs = [0 for r in range(reefmap.reeftotal)]
            catchPl = [0 for r in range(reefmap.reeftotal)]
	    
	    # Reset rho values
	    rho_H = [0 for r in range(reefmap.reeftotal)]
	    rho_Ps = [0 for r in range(reefmap.reeftotal)]
	    rho_Pl = [0 for r in range(reefmap.reeftotal)]	    
                
            # Loop through updating interval
            for ii in range(params.update):
                
                # Loop through cells and subregions and run local model
                for r in range(reefmap.reeftotal):
                    if params.pmethod == 1:
                        if i == 0:
                            p_cells[r] = params.calcParams(self.params,
                                         reefmap.cell_area,run,i,r)
                        self.p = p_cells[r]
                    if params.pmethod == 3:
                        if ii == 0:
                            p_cells[r] = params.calcParams(self.params,
                                                           reefmap.cell_area)
                        self.p = p_cells[r]
                    
                    # Nutrient forcing parameters
                    if forcid_nut[r] == 1:
                        self.nut['rnut_M'] = self.p['rnut_M']
                        self.nut['lnut_C'] = self.p['lnut_C']
                    else:
                        self.nut['rnut_M'] = 1
                        self.nut['lnut_C'] = 1
                    
                    # Sediment forcing parameters
                    if forcid_sed[r] == 1: 
                        self.sed['rsed_C'] = self.p['rsed_C']
                        self.sed['dsed_C'] = self.p['dsed_C']
                        self.sed['drecsed_C'] = self.p['drecsed_C']
                        self.sed['epsilonsed_C'] = self.p['epsilonsed_C']
                    else:        
                        self.sed['rsed_C'] = 1
                        self.sed['dsed_C'] = 0
                        self.sed['drecsed_C'] = 0
                        self.sed['epsilonsed_C'] = 1
                    
                    if ii == 0:
		    # Track the number of arriving recruits (per cell)
			self.rec0Cb[i+1].append(self.recruitsCb
						[transition.pc_map[r]])
                        self.rec0Cs[i+1].append(self.recruitsCs
						[transition.pc_map[r]])
                        self.rec0H[i+1].append(self.recruitsH
						[transition.pc_map[r]])
                        self.rec0P[i+1].append(self.recruitsP
						[transition.pc_map[r]])
                        self.rec0U[i+1].append(self.recruitsU
						[transition.pc_map[r]])
		    
		    # Apply mortality to recruits at the beginning of the year
                        recCb[r] = (self.recruitsCb[transition.pc_map[r]]/
                                 transition.pc_scale[r])\
                                *(1 - self.p['drec_C']*params.update)\
                                *(1 - self.sed['drecsed_C'])
                        recCs[r] = (self.recruitsCs[transition.pc_map[r]]/
                                 transition.pc_scale[r])\
                                *(1 - self.p['drec_C']*params.update)\
                                *(1 - self.sed['drecsed_C'])    
                        recU[r] = (self.recruitsU[transition.pc_map[r]]/
                                 transition.pc_scale[r])
                        if C[0][r] <= 0.05:
                            recH[r] = (self.recruitsH[transition.pc_map[r]]/
                                 transition.pc_scale[r])*0.3
                            recP[r] = (self.recruitsP[transition.pc_map[r]]/
                                  transition.pc_scale[r])*0.3
                        else:
                            recH[r] = (self.recruitsH[transition.pc_map[r]]/
                                     transition.pc_scale[r])\
                                    *(C[0][r]*10/(1 + 9*C[0][r]))
                            recP[r] = (self.recruitsP[transition.pc_map[r]]/
                                      transition.pc_scale[r])\
                                    *(C[0][r]*10/(1 + 9*C[0][r]))
                        
                        # Density-dependent mortality: fish and urchin recruits
			if recH[r]/reefmap.cell_area >= 1E+006:
			    ddrecH = max(self.p['drec_F']*params.update,
			    2E-007*recH[r]/reefmap.cell_area)
			else:
			    ddrecH = self.p['drec_F']*params.update
			if recP[r]/reefmap.cell_area >= 1E+006:
			    ddrecP = max(self.p['drec_F']*params.update,
			    2E-007*recP[r]/reefmap.cell_area)
			else:
			    ddrecP = self.p['drec_F']*params.update
			if recU[r]/reefmap.cell_area >= 1E+006:
			    ddrecU = max(self.p['drec_U']*params.update,
			    2E-007*recU[r]/reefmap.cell_area)
			else:
			    ddrecU = self.p['drec_U']*params.update                            
                        recH[r]= recH[r]*(1 - min(ddrecH,0.98))
                        recP[r] = recP[r]*(1 - min(ddrecP,0.98))
                        recU[r] = recU[r]*(1 - min(ddrecU,0.98))
                    
                        # Track the number of surviving recruits (per cell)
                        self.rec1Cb[i+1].append(recCb[r])
                        self.rec1Cs[i+1].append(recCs[r])
                        self.rec1H[i+1].append(recH[r])
                        self.rec1P[i+1].append(recP[r])
                        self.rec1U[i+1].append(recU[r])
                        
                    # Fishing pressure
                    if forcing_f.opt == 0 or year < 0: fishing = 0
                    elif forcing_f.opt == 2:
			if year == 0:
			    fishing = 0
			else:
			    fishing = forcing_f.sched[year][reefmap.subregid[r]\
				      -1]*reefmap.cell_area/params.update
                    elif forcing_f.opt == 3:
                        if year >= 0:
                            if r in forcing_f.mpa:
                                fishing = 0
                            else: fishing = self.p['f']*reefmap.cell_area
                        else: fishing = 0
                    else: fishing = self.p['f']*reefmap.cell_area
		    if ii == 0:
		        rho_H[r] = H[0][r]/(H[0][r]+Ps[0][r]+Pl[0][r])
			rho_Ps[r] = Ps[0][r]/(H[0][r]+Ps[0][r]+Pl[0][r])
			rho_Pl[r] = Pl[0][r]/(H[0][r]+Ps[0][r]+Pl[0][r])
                    
                    theta_H = H[0][r]/(self.p['i_H'] + H[0][r])
                    theta_U = U[0][r]/(self.p['i_U'] + U[0][r])
                    theta = theta_H*(1 - self.p['lambda_U']*theta_U)\
                    + theta_U*(1 - self.p['lambda_H']*theta_H)                   
    
                    # Brooding coral cover
                    Cb[-1].append(Cb[0][r]
                    + self.p['r_C']*self.sed['rsed_C']
                    *(1 - self.p['beta_M']*M[0][r])*(E[0][r]
                    + self.p['alpha_C']*T[0][r])*Cb[0][r]
                    - (self.p['d_C'] + self.sed['dsed_C'])*Cb[0][r]
                    - self.p['gamma_MC']*self.p['r_M']*self.nut['rnut_M']
                    *M[0][r]*Cb[0][r] + recCb[r]*self.p['arec_C']
                    /(reefmap.cell_area*params.update)*(E[0][r]
                    + self.p['epsilon_C']*self.sed['epsilonsed_C']*T[0][r]))
                    
                    # Spawning coral cover
                    Cs[-1].append(Cs[0][r]
                    + self.p['r_C']*self.sed['rsed_C']
                    *(1 - self.p['beta_M']*M[0][r])*(E[0][r]
                    + self.p['alpha_C']*T[0][r])*Cs[0][r]
                    - (self.p['d_C'] + self.sed['dsed_C'])*Cs[0][r]
                    - self.p['gamma_MC']*self.p['r_M']*self.nut['rnut_M']
                    *M[0][r]*Cs[0][r] + recCs[r]*self.p['arec_C']
                    /(reefmap.cell_area*params.update)*(E[0][r]
                    + self.p['epsilon_C']*self.sed['epsilonsed_C']*T[0][r]))
                    
                    # Total coral cover
                    C[-1].append(Cb[-1][r] + Cs[-1][r])
    
                    # Macroturf cover
                    T[-1].append(T[0][r]
                    + self.p['zeta_T']*(1 - theta)*E[0][r]
                    - self.p['g_T']*theta*T[0][r]
                    - self.p['epsilon_C']*self.sed['epsilonsed_C']*T[0][r]
                    *(recCb[r]*self.p['arec_C']/(reefmap.cell_area
                    *params.update) + recCs[r]*self.p['arec_C']
                    /(reefmap.cell_area*params.update))
                    - self.p['r_C']*self.sed['rsed_C']
                    *self.p['alpha_C']*(1 - self.p['beta_M']*M[0][r])
                    *T[0][r]*C[0][r] - self.p['gamma_MT']*self.p['r_M']
                    *self.nut['rnut_M']*M[0][r]*T[0][r])
                    
                    # Macroalgal cover
                    M[-1].append(M[0][r]
                    + self.p['r_M']*self.nut['rnut_M']
                    *M[0][r]*E[0][r] - self.p['g_M']*theta*M[0][r]
                    + self.p['gamma_MC']*self.p['r_M']*self.nut['rnut_M']
                    *M[0][r]*C[0][r]+ self.p['gamma_MT']*self.p['r_M']
                    *self.nut['rnut_M']*M[0][r]*T[0][r])
                    
                    # EAC cover
                    E[-1].append(1 - C[-1][r] - T[-1][r] - M[-1][r])
              
                    # Herbivorous fish biomass
                    H[-1].append(H[0][r]
                    + theta_H*(1 - self.p['lambda_U']*theta_U)
                    *(self.p['g_M']*M[0][r]*self.p['mu_M']
                    + self.p['g_T']*T[0][r]*self.p['mu_T']
                    + self.p['zeta_T']*E[0][r]*self.p['mu_E'])
                    - self.p['d_H']*H[0][r] - (self.p['g_Ps']
                    *Ps[0][r] + self.p['g_Pl']*Pl[0][r])
                    *((H[0][r])**2/((self.p['i_PH'])**2
                    + (H[0][r])**2))
                    - rho_H[r]*fishing*(H[0][r]/(self.p['i_FH'] + H[0][r]))
                    + self.p['brec_H']*recH[r]/params.update)
                    catchH[r] += rho_H[r]*fishing*(H[0][r]
                             /(self.p['i_FH'] + H[0][r]))
                    
                    # Small piscivorous fish biomass
                    Ps[-1].append(Ps[0][r]
                    + (1 - self.p['phi_Ps'])*self.p['r_Ps']*self.p['g_Ps']
                    *((H[0][r])**2/((self.p['i_PH'])**2
                    + (H[0][r])**2))*Ps[0][r] - self.p['d_Ps']*Ps[0][r]
                    - self.p['psi_Pl']*self.p['g_Pl']*((Ps[0][r])**2
                    /((self.p['i_PlPs'])**2 + (Ps[0][r])**2))
                    *Pl[0][r] - rho_Ps[r]*fishing
                    *(Ps[0][r]/(self.p['i_FPs'] + Ps[0][r]))
                    + self.p['brec_P']*recP[r]/params.update)
                    catchPs[r] += rho_Ps[r]*fishing*(Ps[0][r]
                              /(self.p['i_FPs'] + Ps[0][r]))
                    
                    # Large piscivorous fish
                    Pl[-1].append(Pl[0][r]
                    + self.p['phi_Ps']*self.p['r_Ps']*self.p['g_Ps']
                    *((H[0][r])**2/((self.p['i_PH'])**2
                    + (H[0][r])**2))*Ps[0][r]
                    + self.p['r_Pl']*self.p['g_Pl']*(((H[0][r])**2
                    /((self.p['i_PH'])**2 + (H[0][r])**2))
                    + self.p['psi_Pl']*((Ps[0][r])**2
                    /((self.p['i_PlPs'])**2 + (Ps[0][r])**2)))
                    *Pl[0][r] - self.p['d_Pl']*Pl[0][r]
                    - rho_Pl[r]*fishing*(Pl[0][r]/(self.p['i_FPl'] + Pl[0][r])))
                    catchPl[r] += rho_Pl[r]*fishing*(Pl[0][r]
                              /(self.p['i_FPl'] + Pl[0][r]))
                    
                    # Urchin biomass
                    U[-1].append(U[0][r]
                    + self.p['kappa_U']*theta_U
                    *(1 - self.p['lambda_H']*theta_H)
                    *(self.p['g_M']*M[0][r]*self.p['mu_M']
                    + self.p['g_T']*T[0][r]*self.p['mu_T']
                    + self.p['zeta_T']*E[0][r]*self.p['mu_E'])
                    - self.p['d_U']*U[0][r]
                    - self.p['q_U']*(U[0][r]**2)
                    + self.p['brec_U']*recU[r]/params.update)
                    
                    # Catch run-away dynamics
                    if str(Cb[-1][r]) == str(float(nan)): self.errors += 1
                    if str(Cs[-1][r]) == str(float(nan)): self.errors += 1
                    if str(T[-1][r]) == str(float(nan)): self.errors += 1
                    if str(M[-1][r]) == str(float(nan)): self.errors += 1
                    if str(H[-1][r]) == str(float(nan)): self.errors += 1
                    if str(Ps[-1][r]) == str(float(nan)): self.errors += 1
                    if str(Pl[-1][r]) == str(float(nan)): self.errors += 1
                    if str(U[-1][r]) == str(float(nan)): self.errors += 1 
                    if H[-1][r] <= 0: H[-1][r] = 0
                    if Ps[-1][r] <= 0: Ps[-1][r] = 0
                    if Pl[-1][r] <= 0: Pl[-1][r] = 0
                    if U[-1][r] <= 0: U[-1][r] = 0
                    
                    if ii == round(params.update/2):
                        # Hurricane forcing (acts midyear)
                        if forcid_hurr[r] == 1:
                            Cb[-1][r] -= self.p['hdam_C']*Cb[-1][r]
                            Cs[-1][r] -= self.p['hdam_C']*Cs[-1][r]
                            C[-1][r] = Cb[-1][r] + Cs[-1][r]
                            M[-1][r] -= self.p['hdam_M']*M[-1][r]
                        
                        # Coral mortality forcing (acts midyear)
                        if forcid_cm[r] == 1:
                            if forcing_cm.opt == 2:
				rand = random()
				cmort = rand*(cm[1] - cm[0]) + cm[0]
				Cb[-1][r] -= cmort*Cb[-1][r]
				Cs[-1][r] -= cmort*Cs[-1][r]
				C[-1][r] = Cb[-1][r] + Cs[-1][r]
                            else:
                                Cb[-1][r] -= self.p['cm_C']*Cb[-1][r]
                                Cs[-1][r] -= self.p['cm_C']*Cs[-1][r]
                                C[-1][r] = Cb[-1][r] + Cs[-1][r]
                                
                        # Destructive fishing forcing (acts midyear)
                        if forcid_df[r] == 1:
                            Cb[-1][r] -= self.p['dfdam_C']*params.update\
			                 *Cb[-1][r]/C[-1][r]
                            if Cb[-1][r] < 0: Cb[-1][r] = 0
                            Cs[-1][r] -= self.p['dfdam_C']*params.update\
			                 *Cs[-1][r]/C[-1][r]
                            if Cs[-1][r] < 0: Cs[-1][r] = 0
                            C[-1][r] = Cb[-1][r] + Cs[-1][r]
                                
                    # Calculate reproductive output incrementally
                    self.reproCb[transition.pc_map[r]] += \
                    self.p['l_C']*self.nut['lnut_C']\
                    *Cb[-1][r]*reefmap.cell_area
                    self.reproCs[transition.pc_map[r]] += \
                    self.p['l_C']*self.nut['lnut_C']\
                    *Cs[-1][r]*reefmap.cell_area
                    self.reproH[transition.pc_map[r]] += \
                    self.p['l_H']*H[-1][r]
                    self.reproPs[transition.pc_map[r]] += \
                    self.p['l_Ps']*Ps[-1][r]
                    self.reproPl[transition.pc_map[r]] += \
                    self.p['l_Pl']*Pl[-1][r]
                    self.reproU[transition.pc_map[r]] += \
                    self.p['l_U']*U[-1][r]
                    
                    # Catch values at the end of each year
                    if ii == params.update - 1:
                        self.Cb[i+1].append(Cb[-1][r])
                        self.Cs[i+1].append(Cs[-1][r])
                        self.C[i+1].append(C[-1][r])
                        self.T[i+1].append(T[-1][r])
                        self.M[i+1].append(M[-1][r])
                        self.E[i+1].append(E[-1][r])
                        self.H[i+1].append(H[-1][r])
                        self.Ps[i+1].append(Ps[-1][r])
                        self.Pl[i+1].append(Pl[-1][r])
                        self.U[i+1].append(U[-1][r])
			self.catchH[i+1].append(catchH[r])
			self.catchPs[i+1].append(catchPs[r])
			self.catchPl[i+1].append(catchPl[r])
                        
                        if self.errors > 0:
                            break
                    if self.errors > 0:
                        break
                    
                del(C[0]); C.append([]); del(Cb[0]); Cb.append([])
                del(Cs[0]); Cs.append([]); del(T[0]); T.append([])
                del(M[0]); M.append([]); del(E[0]); E.append([])
                del(H[0]); H.append([]); del(Ps[0]); Ps.append([])
                del(Pl[0]); Pl.append([]); del(U[0]); U.append([])
            
            if self.errors > 0:
                break
            
        # Discard equilibration years
        self.modelout = {}
	for v in variables:
	    self.modelout[v] = []
	for s in range(params.equilib+1,params.years+params.equilib+1):
	    self.modelout['C'].append(copy.deepcopy(self.C[s]))
	    self.modelout['Cb'].append(copy.deepcopy(self.Cb[s]))
	    self.modelout['Cs'].append(copy.deepcopy(self.Cs[s]))
	    self.modelout['T'].append(copy.deepcopy(self.T[s]))
	    self.modelout['M'].append(copy.deepcopy(self.M[s]))
	    self.modelout['E'].append(copy.deepcopy(self.E[s]))
	    self.modelout['H'].append(copy.deepcopy(self.H[s]))
	    self.modelout['Ps'].append(copy.deepcopy(self.Ps[s]))
	    self.modelout['Pl'].append(copy.deepcopy(self.Pl[s]))
	    self.modelout['U'].append(copy.deepcopy(self.U[s]))
	    self.modelout['catchH'].append(copy.deepcopy(self.catchH[s]))
	    self.modelout['catchPs'].append(copy.deepcopy(self.catchPs[s]))
	    self.modelout['catchPl'].append(copy.deepcopy(self.catchPl[s]))
	    
	if self.errors == 0:
	    #Calculate averages and confidence intervals across all  
	    #cells at each timestep.
	    self.avs = {}; self.stds = {}; self.CIs = {}
	    for var in variables:
		self.avs[var] = []
		self.stds[var] = []
		self.CIs[var] = [[],[]]	
	    for i in range(params.years):
		for var in ['C','Cb','Cs','T','M','E']:
		    self.avs[var].append(round(mean(self.modelout[var][i])\
					       *sc_ben,2))
		    self.stds[var].append(std(self.modelout[var][i])*sc_ben)
		    self.CIs[var][0].append(round(self.avs[var][i] 
						  - 1.96*self.stds[var][i],2))
		    self.CIs[var][1].append(round(self.avs[var][i]
						  + 1.96*self.stds[var][i],2))
		    if self.CIs[var][0][i] < 0: self.CIs[var][0][i] = 0
		for var in ['H','Ps','Pl','U','catchH','catchPs','catchPl']:
		    self.avs[var].append(round(mean(self.modelout[var][i])\
					       *sc_con/reefmap.cell_area,2))
		    self.stds[var].append(std(self.modelout[var][i])\
					       *sc_con/reefmap.cell_area)
		    self.CIs[var][0].append(round(self.avs[var][i] 
						  - 1.96*self.stds[var][i],2))
		    self.CIs[var][1].append(round(self.avs[var][i]
						  + 1.96*self.stds[var][i],2))
		    if self.CIs[var][0][i] < 0: self.CIs[var][0][i] = 0
		    
	    #Calculate averages and confidence intervals across all cells 
	    #within a subregion at each timestep.
	    self.avsSR = {}; self.stdsSR = {}; self.CIsSR = {}
	    for var in variables:
		self.avsSR[var] = []
		self.stdsSR[var] = []
		self.CIsSR[var] = [[],[]]
	    j = 1
	    calcben = {}; calccon = {}
	    while j <= reefmap.srrange:
		for i in range(params.years):
		    for var in ['C','Cb','Cs','T','M','E']:
			calcben[var] = []
			for r in range(reefmap.reeftotal):
			    if reefmap.subregid[r] == j:
				calcben[var].append(self.modelout[var][i][r])
			self.avsSR[var].append(round(mean(calcben[var])
						     *sc_ben,2))
			self.stdsSR[var].append(std(calcben[var])*sc_ben)
			self.CIsSR[var][0].append(round(self.avsSR[var][-1]
						- 1.96*self.stdsSR[var][-1],2))
			if self.CIsSR[var][0][-1] < 0: 
			    self.CIsSR[var][0][-1] = 0
			self.CIsSR[var][1].append(round(self.avsSR[var][-1]
						+ 1.96*self.stdsSR[var][-1],2))
		    for var in ['H','Ps','Pl','U','catchH','catchPs','catchPl']:
			calccon[var] = []
			for r in range(reefmap.reeftotal):
			    if reefmap.subregid[r] == j:
				calccon[var].append(self.modelout[var][i][r])
			self.avsSR[var].append(round(mean(calccon[var])*sc_con
						     /reefmap.cell_area,2))
			self.stdsSR[var].append(std(calccon[var])*sc_con
						/reefmap.cell_area)
			self.CIsSR[var][0].append(round(self.avsSR[var][-1]
						- 1.96*self.stdsSR[var][-1],2))
			if self.CIsSR[var][0][-1] < 0:
			    self.CIsSR[var][0][-1] = 0
			self.CIsSR[var][1].append(round(self.avsSR[var][-1]
						+ 1.96*self.stdsSR[var][-1],2))
		j += 1
	
	    for var in variables:
		self.avsSR[var] = (array(self.avsSR[var])).reshape(
		                   reefmap.srrange, params.years)
		self.CIsSR[var] = (array(self.CIsSR[var])).reshape(2, 
				   reefmap.srrange, params.years)
	    