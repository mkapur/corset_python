from random import *

class Params:
    """Import and manipulate parameters.

       __init__    -- Read in parameter ranges from file.
       initVals    -- Read in initial conditions from file.
       paramScale  -- Define scaling for parameters dependent on reef cell area.
       calcParams  -- For parameters defined by ranges, select a value 
                      from the range according to the uniform distribution.
    """

    def __init__(self,path,region,years,equilib,runs,seed,foptions):
        self.init_errors = 0
        self.error_text = []
        self.region = region
        self.years = years
        self.equilib = equilib
        self.runs = runs
        self.seed = seed
        self.update = 52
        self.pmethod = 3     
        
        # Set up parameter dictionaries
        self.parambenthos = {}; self.paramconsumers = {}; self.paramlist = {}
        self.paramscaled = {}; self.paramrec = {}
        self.paramforc = {}
        rate_params = ['r_C','d_C','zeta_T','g_T','r_M','g_M',
                       'd_H','g_Ps','d_Ps','g_Pl','d_Pl','d_U','q_U',
                       'mu_M','mu_T','mu_E','l_C','l_H','l_Ps','l_Pl','l_U',
                       'drec_C','drec_F','drec_U','dfdam_C','dsed_C']
        params = open(path,'U')
        
        # Benthic parameters                    
        params.readline()
        while 1:
            p = params.readline()
            if not p or p == '\n':
                break
            try:
                if len(p.split(',')) == 2:
                    if p.split(',')[0] in rate_params:
                        self.parambenthos[p.split(',')[0]] =\
                        float(p.split(',')[1])/self.update
                    else:
                        self.parambenthos[p.split(',')[0]] =\
                        float(p.split(',')[1])
                else:
                    if p.split(',')[0] in rate_params:
                        self.parambenthos[p.split(',')[0]] =\
                        [float(p.split(',')[1])/self.update,\
                        float(p.split(',')[2])/self.update]
                    else:
                        self.parambenthos[p.split(',')[0]] =\
                        [float(p.split(',')[1]), float(p.split(',')[2])]
            except:
                self.error_text.append(
                '** Parameters should be specified as comma-separated values')
                self.error_text.append(
                'check the format of parameter file line "%s"' %p.strip())
                self.init_errors += 1
        for keys in ['r_C','alpha_C','d_C','epsilon_C','zeta_T','g_T',
                     'beta_M','r_M','g_M','gamma_MC','gamma_MT']:
            if keys not in self.parambenthos.keys():
                self.error_text.append(
                '** "%s" is missing from the benthic parameter list' %keys)
                self.error_text.append(
                'check that the parameter file meets formatting requirements')
                self.init_errors += 1

        #  Consumer parameters
        params.readline()
        while 1:
            p = params.readline()
            if not p or p == '\n':
                break
            try:
                if len(p.split(',')) == 2:
                    if p.split(',')[0] in rate_params:
                        self.paramconsumers[p.split(',')[0]] =\
                        float(p.split(',')[1])/self.update
                    else:
                        self.paramconsumers[p.split(',')[0]] =\
                        float(p.split(',')[1])
                else:
                    if p.split(',')[0] in rate_params:
                        self.paramconsumers[p.split(',')[0]] =\
                        [float(p.split(',')[1])/self.update,\
                        float(p.split(',')[2])/self.update]
                    else:
                        self.paramconsumers[p.split(',')[0]] =\
                        [float(p.split(',')[1]), float(p.split(',')[2])]
            except:
                self.error_text.append(
                '** Parameters should be specified as comma-separated values')
                self.error_text.append(
                'check the format of parameter file line "%s"' %p.strip())
                self.init_errors += 1
        for keys in ['d_H','lambda_H','phi_Ps','r_Ps','g_Ps','d_Ps','r_Pl',
                     'g_Pl','psi_Pl','d_Pl','kappa_U','d_U','q_U']:
            if keys not in self.paramconsumers.keys():
                self.error_text.append(
                '** "%s" is missing from the consumer parameter list' %keys)
                self.error_text.append(
                'check that the parameter file meets formatting requirements')
                self.init_errors += 1        
        try:
            if type(self.paramconsumers['lambda_H']) == list:
                self.error_text.append(
                '** A single value for "lambda_H" should be specified in the')
                self.error_text.append(
                'parameter file, not a range of values')
                self.init_errors += 1
            if self.paramconsumers['lambda_H'] < 0.6 or \
            self.paramconsumers['lambda_H'] > 1.0:
                self.error_text.append(
                '** "lambda_H" should be a single value between 0.6 - 1.0')
                self.init_errors += 1
            self.paramconsumers['lambda_U'] = 1-self.paramconsumers['lambda_H']        
        except:
            self.init_errors += 1
        self.paramlist.update(self.parambenthos)
        self.paramlist.update(self.paramconsumers)
        
        # Scale-dependent parameters
        params.readline()
        while 1:
            p = params.readline()
            if not p or p == '\n':
                break
            try:
                if len(p.split(',')) == 2:
                    if p.split(',')[0] in rate_params:
                        self.paramscaled[p.split(',')[0]] =\
                        float(p.split(',')[1])/self.update
                    else:
                        self.paramscaled[p.split(',')[0]] =\
                        float(p.split(',')[1])
                else:
                    if p.split(',')[0] in rate_params:
                        self.paramscaled[p.split(',')[0]] =\
                        [float(p.split(',')[1])/self.update,\
                        float(p.split(',')[2])/self.update]
                    else:
                        self.paramscaled[p.split(',')[0]] =\
                        [float(p.split(',')[1]), float(p.split(',')[2])]
            except:
                self.error_text.append(
                '** Parameters should be specified as comma-separated values')
                self.error_text.append(
                'check the format of parameter file line "%s"' %p.strip())
                self.init_errors += 1
        for keys in ['mu_M','mu_T','mu_E','i_H','i_U','i_PH','i_PlPs',
                     'i_FH','i_FPs','i_FPl']:
            if keys not in self.paramscaled.keys():
                self.error_text.append(
                '** "%s" is missing from the scale-dependent parameter list' 
                %keys)
                self.error_text.append(
                'check that the parameter file meets formatting requirements')
                self.init_errors += 1        
            
        # Recruitment parameters
        params.readline()
        while 1:
            p = params.readline()
            if not p or p == '\n':
                break
            try:
                if len(p.split(',')) == 2:
                    if p.split(',')[0] in rate_params:
                        self.paramrec[p.split(',')[0]] =\
                        float(p.split(',')[1])/self.update
                    else:
                        self.paramrec[p.split(',')[0]] =\
                        float(p.split(',')[1])
                else:
                    if p.split(',')[0] in rate_params:
                        self.paramrec[p.split(',')[0]] =\
                        [float(p.split(',')[1])/self.update,\
                        float(p.split(',')[2])/self.update]
                    else:
                        self.paramrec[p.split(',')[0]] =\
                        [float(p.split(',')[1]), float(p.split(',')[2])]
            except:
                self.error_text.append(
                '** Parameters should be specified as comma-separated values')
                self.error_text.append(
                'check the format of parameter file line "%s"' %p.strip())
                self.init_errors += 1        
        for keys in ['l_C','l_H','l_Ps','l_Pl','l_U','dlarv_Cb','drec_C',
                     'drec_F','drec_U','arec_C','brec_H','brec_P','brec_U']:
            if keys not in self.paramrec.keys():
                self.error_text.append(
                '** "%s" is missing from the recruitment parameter list' %keys)
                self.error_text.append(
                'check that the parameter file meets formatting requirements')
                self.init_errors += 1        
            
        # Forcing parameters
        params.readline()
        while 1:
            p = params.readline()
            if not p or p == '\n':
                break
            try:
                if len(p.split(',')) == 2:
                    if p.split(',')[0] in rate_params:
                        self.paramforc[p.split(',')[0]] =\
                        float(p.split(',')[1])/self.update
                    else:
                        self.paramforc[p.split(',')[0]] =\
                        float(p.split(',')[1])
                else:
                    if p.split(',')[0] in rate_params:
                        self.paramforc[p.split(',')[0]] =\
                        [float(p.split(',')[1])/self.update,\
                        float(p.split(',')[2])/self.update]
                    else:
                        self.paramforc[p.split(',')[0]] =\
                        [float(p.split(',')[1]), float(p.split(',')[2])]
            except:
                self.error_text.append(
                '** Parameters should be specified as comma-separated values')
                self.error_text.append(
                'check the format of parameter file line "%s"' %p.strip())
                self.init_errors += 1     
        for keys in ['hdam_C','hdam_M','cm_C','dfdam_C','rnut_M','lnut_C',
                     'rsed_C','dsed_C','drecsed_C','epsilonsed_C']:
            if keys not in self.paramforc.keys():
                self.error_text.append(
                '** "%s" is missing from the forcing parameter list' %keys)
                self.error_text.append(
                'check that the parameter file meets formatting requirements')
                self.init_errors += 1        
        self.paramforc['hfreq'] = float(foptions['hfreq'])
        self.paramforc['hmax_sr'] = foptions['hmax_sr']
        self.paramforc['hmin_cat'] = foptions['hmin_cat']
        self.paramforc['hmax_cat'] = foptions['hmax_cat']
        self.paramforc['cmfreq'] = float(foptions['cmfreq'])
        self.paramforc['cmmax_sr'] = foptions['cmmax_sr']
        self.paramforc['f'] = [foptions['f'][0]/self.update,
                            foptions['f'][1]/self.update]   
        params.close()
    
    def initVals(self,path,subregs,cell_area):
        self.init_vals = []
        valid_keys = ['Cb','Cs','T','M','H','Ps','Pl','U']
        vals = open(path,'r')
        keys = vals.readline().strip().split(',')
        if keys == valid_keys:
            i = -1
            while 1:
                p = vals.readline().strip().split(',')
                i += 1
                if not p or p == ['']:
                    break
                self.init_vals.append({})
                if len(p) == len(keys):
                    for j in range(len(keys)):
                        self.init_vals[i][keys[j]] = float(p[j])/100 
                else:
                    self.error_text.append(
            '** Incorrect number of initial values provided for subregion %d' 
            %(i+1))
                    self.init_errors += 1
            vals.close()
            if len(self.init_vals) != subregs:
                self.error_text.append(
            '** The number of rows in the initial values file should')
                self.error_text.append(
            'correspond with the number of subregions specified in map inputs')
                self.init_errors += 1
            try:
                check_iv = []
                for i in range(len(self.init_vals)):
                    check_iv.append(self.init_vals[i]['Cb'] 
                    + self.init_vals[i]['Cs'] + self.init_vals[i]['T']
                    + self.init_vals[i]['M'])
                    if check_iv[i] > 1:
                        self.error_text.append(
                '** Sum of inital values for benthic cover should not be > 100')
                        self.error_text.append('subregion %d' %(i+1))
                        self.init_errors += 1
                for i in range(subregs):
                    for keys in self.init_vals[i]:
                        if keys in ['H','Ps','Pl','U']:
                            self.init_vals[i][keys] = \
                                self.init_vals[i][keys]*cell_area*100
            except:
                self.init_errors += 1
        else:
            self.error_text.append(
                '** The first line of the initial values file should contain')
            self.error_text.append('the following text: "Cb,Cs,T,M,H,Ps,Pl,U"')
            self.init_errors += 1
          
    def paramScale(self,paramscaled,cell_area):
        for key in paramscaled.keys():
            if type(paramscaled[key]) == list:
                paramscaled[key] = [paramscaled[key][0]*cell_area,
                paramscaled[key][1]*cell_area]
            else:
                paramscaled[key] = paramscaled[key]*cell_area

    def calcParams(self,paramlist,cell_area,run=0,i=0,r=0):        
        params = paramlist.copy()
        if self.pmethod == 3: seed()
        else: seed(self.seed)
        for keys in params:
            if type(params[keys]) == list:
                if self.pmethod == 0:
                    for j in range(run+1):
                        rand = uniform(0.0,1.0)
                elif self.pmethod == 1:
                    for j in range(run+1):
                        for k in range(r+1):
                            rand = uniform(0.0,1.0)
                elif self.pmethod == 2:
                    for j in range(run+1):
                        for k in range(i+1):
                            rand = uniform(0.0,1.0)
                else: rand = uniform(0.0,1.0)
                if keys not in ['g_M','i_H','i_U','mu_T','mu_M','mu_E',
                                'd_H','d_U','d_Ps','d_Pl']:
                    params[keys] = rand*(max(params[keys])
                    - min(params[keys])) + min(params[keys])
        
        # Restrictions for 'g_M'
        params['g_M'] = [0.01*params['g_T'],params['g_T']]
        if self.pmethod == 0:
            for j in range(run+1):
                rand = uniform(0.0,1.0)
        elif self.pmethod == 1:
            for j in range(run+1):
                for k in range(r+1):
                    rand = uniform(0.0,1.0)
        elif self.pmethod == 2:
            for j in range(run+1):
                for k in range(i+1):
                    rand = uniform(0.0,1.0)
        else: rand = uniform(0.0,1.0)
        params['g_M'] = rand*(max(params['g_M'])
        - min(params['g_M'])) + min(params['g_M'])
        
        # Restrictions for 'i_H' and 'i_U'
        min_i_H = max(params['i_H'][0],max(params['g_T'],
        params['zeta_T'])*self.update*params['mu_T'][0]/(params['d_H'][1]
        *self.update - 0.000001))
        params['i_H'] = [min_i_H,params['i_H'][1]]
        if self.pmethod == 0:
            for j in range(run+1):
                rand = uniform(0.0,1.0)
        elif self.pmethod == 1:
            for j in range(run+1):
                for k in range(r+1):
                    rand = uniform(0.0,1.0)
        elif self.pmethod == 2:
            for j in range(run+1):
                for k in range(i+1):
                    rand = uniform(0.0,1.0)
        else: rand = uniform(0.0,1.0)
        params['i_H'] = rand*(max(params['i_H'])
        - min(params['i_H'])) + min(params['i_H'])
        min_i_U = max(params['i_U'][0],params['kappa_U']
        *max(params['g_T'],params['zeta_T'])*self.update*params['mu_T'][0]
        /(params['d_U'][1]*self.update - 0.000001))
        params['i_U'] = [min_i_U,params['i_U'][1]]
        if self.pmethod == 0:
            for j in range(run+1):
                rand = uniform(0.0,1.0)
        elif self.pmethod == 1:
            for j in range(run+1):
                for k in range(r+1):
                    rand = uniform(0.0,1.0)
        elif self.pmethod == 2:
            for j in range(run+1):
                for k in range(i+1):
                    rand = uniform(0.0,1.0)
        else: rand = uniform(0.0,1.0)
        params['i_U'] = rand*(max(params['i_U'])
        - min(params['i_U'])) + min(params['i_U'])
        
        # Restrictions on 'mu_T','mu_M','mu_E'
        mu_max = min(params['mu_T'][1]*self.update,min(params['i_H']*
        (params['d_H'][1]*self.update - 0.000001)/(max(params['g_T'],
        params['zeta_T'])*self.update),params['i_U']*(params['d_U'][1]*
        self.update - 0.000001)/(params['kappa_U']*max(params['g_T'],
        params['zeta_T'])*self.update)))  
        params['mu_T'] = [params['mu_T'][0],mu_max/self.update]
        params['mu_M'] = [params['mu_M'][0],mu_max/self.update]
        params['mu_E'] = [params['mu_E'][0],mu_max/self.update]
        if self.pmethod == 0:
            for j in range(run+1):
                rand = uniform(0.0,1.0)
        elif self.pmethod == 1:
            for j in range(run+1):
                for k in range(r+1):
                    rand = uniform(0.0,1.0)
        elif self.pmethod == 2:
            for j in range(run+1):
                for k in range(i+1):
                    rand = uniform(0.0,1.0)
        else: rand = uniform(0.0,1.0)
        params['mu_T'] = rand*(max(params['mu_T'])
        - min(params['mu_T'])) + min(params['mu_T'])
        if self.pmethod == 0:
            for j in range(run+1):
                rand = uniform(0.0,1.0)
        elif self.pmethod == 1:
            for j in range(run+1):
                for k in range(r+1):
                    rand = uniform(0.0,1.0)
        elif self.pmethod == 2:
            for j in range(run+1):
                for k in range(i+1):
                    rand = uniform(0.0,1.0)
        else: rand = uniform(0.0,1.0)
        params['mu_M'] = rand*(max(params['mu_M'])
        - min(params['mu_M'])) + min(params['mu_M'])
        if self.pmethod == 0:
            for j in range(run+1):
                rand = uniform(0.0,1.0)
        elif self.pmethod == 1:
            for j in range(run+1):
                for k in range(r+1):
                    rand = uniform(0.0,1.0)
        elif self.pmethod == 2:
            for j in range(run+1):
                for k in range(i+1):
                    rand = uniform(0.0,1.0)
        else: rand = uniform(0.0,1.0)
        params['mu_E'] = rand*(max(params['mu_E'])
        - min(params['mu_E'])) + min(params['mu_E'])
        
        # Restrictions on 'd_H','d_U','d_Ps','d_Pl'
        min_d_H = max(params['d_H'][0]*self.update,max(params['g_T'],
        params['zeta_T'])*self.update*params['mu_T']/params['i_H'] + 0.000001)
        params['d_H'] = [min_d_H/self.update,params['d_H'][1]]
        min_d_U = max(params['d_U'][0]*self.update,(params['kappa_U']
        *params['mu_T']*max(params['g_T'],params['zeta_T'])*self.update
        /params['i_U']) + 0.000001)
        params['d_U'] = [min_d_U/self.update,params['d_U'][1]]
        min_d_Ps = max(params['d_Ps'][0]*self.update,(1 - params['phi_Ps'])
        *params['r_Ps']*params['g_Ps']*self.update)
        params['d_Ps'] = [min_d_Ps/self.update,params['d_Ps'][1]]
        min_d_Pl = max(params['d_Pl'][0]*self.update,params['r_Pl']
        *params['g_Pl']*self.update*(1 + params['psi_Pl']) + 0.000001)
        params['d_Pl'] = [min_d_Ps/self.update,params['d_Pl'][1]]
        if self.pmethod == 0:
            for j in range(run+1):
                rand = uniform(0.0,1.0)
        elif self.pmethod == 1:
            for j in range(run+1):
                for k in range(r+1):
                    rand = uniform(0.0,1.0)
        elif self.pmethod == 2:
            for j in range(run+1):
                for k in range(i+1):
                    rand = uniform(0.0,1.0)
        else: rand = uniform(0.0,1.0)
        params['d_H'] = rand*(max(params['d_H'])
        - min(params['d_H'])) + min(params['d_H'])
        if self.pmethod == 0:
            for j in range(run+1):
                rand = uniform(0.0,1.0)
        elif self.pmethod == 1:
            for j in range(run+1):
                for k in range(r+1):
                    rand = uniform(0.0,1.0)
        elif self.pmethod == 2:
            for j in range(run+1):
                for k in range(i+1):
                    rand = uniform(0.0,1.0)
        else: rand = uniform(0.0,1.0)
        params['d_U'] = rand*(max(params['d_U'])
        - min(params['d_U'])) + min(params['d_U'])
        if self.pmethod == 0:
            for j in range(run+1):
                rand = uniform(0.0,1.0)
        elif self.pmethod == 1:
            for j in range(run+1):
                for k in range(r+1):
                    rand = uniform(0.0,1.0)
        elif self.pmethod == 2:
            for j in range(run+1):
                for k in range(i+1):
                    rand = uniform(0.0,1.0)
        else: rand = uniform(0.0,1.0)
        params['d_Ps'] = rand*(max(params['d_Ps'])
        - min(params['d_Ps'])) + min(params['d_Ps'])
        if self.pmethod == 0:
            for j in range(run+1):
                rand = uniform(0.0,1.0)
        elif self.pmethod == 1:
            for j in range(run+1):
                for k in range(r+1):
                    rand = uniform(0.0,1.0)
        elif self.pmethod == 2:
            for j in range(run+1):
                for k in range(i+1):
                    rand = uniform(0.0,1.0)
        else: rand = uniform(0.0,1.0)
        params['d_Pl'] = rand*(max(params['d_Pl'])
        - min(params['d_Pl'])) + min(params['d_Pl'])
        
        return params
