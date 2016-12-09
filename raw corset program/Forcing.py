from random import *

class Forcing:
    """Format nutrification, sedimentation, hurricane, coral mortality
       and fishing forcing schedules.

       nsSched   -- Read nutrification/sedimentation forcing schedule from file.
       nsforcID  -- Allocate spatial distributions of nutrification/
                    sedimentation forcing effects at the specified timestep 'i'.
       hSched    -- read hurricane forcing schedule from file
       hforcID   -- Allocate spatial distributions of hurricane forcing effects  
                    at the specified timestep 'i'.
       cmSched   -- Read coral mortality schedule from file.
       cmforcID  -- Allocate spatial distributions of coral mortality forcing 
                    effects at the specified timestep 'i'.
       fSched    -- Read fishing pressure schedule from file.
       dfSched   -- Read destructive fishing pressure schedule from file.
       dfforcID  -- Allocate spatial distributions of destructive fishing effect
                    at the specified timestep 'i'.
    """
    
    def __init__(self,opt,name):
        self.opt = opt
        self.name = name
        self.init_errors = 0
        self.error_text = []
        self.warnings = 0
        self.warning_text = []
        
    def nsSched(self,file,reefmap,years):
        """Read nutrification/sedimentation forcing schedule from file."""
        if self.opt != 0:
            f = open(file,'U')
            if self.opt == 1:
                sched = {}
                self.sched = {} 
                f.readline()
                try: 
                    for lines in f:
                        l = lines.split('\t')
                        if len(l) == reefmap.srrange + 1:
                            self.sched[int(l[0])] = []
                            for sr in range(1,len(l)):
                                self.sched[int(l[0])].append(float(l[sr]))
                        else:
                            self.error_text.append(
                '** The number of columns in the input file for %s' %self.name)
                            self.error_text.append(
                'option 1 is incorrect: please check the user documentation')
                            self.error_text.append(
                'for formatting requirements for this file')
                            self.init_errors += 1
                except:
                    self.error_text.append(
                '** There are formatting errors in the input file for %s'
                %self.name)
                    self.error_text.append(
                'option 1: please check the user documentation for formatting')
                    self.error_text.append(
                'requirements for this file')
                    self.init_errors += 1
                f.close()
                if self.init_errors == 0:
                    check_years = []
                    for i in range(1,years+1):
                        if i not in self.sched.keys():
                            check_years.append(i)
                    if len(check_years) > 0:
                        self.error_text.append(
                    '** The input file for %s forcing option 1 is missing' 
                    %self.name)
                        self.error_text.append(
                    '%s values for years %s' %(self.name,check_years)) 
                        self.init_errors += 1
                    check_years = []
                    for i in self.sched.keys():
                        if i not in range(1,years+1):
                            check_years.append(i)
                    if len(check_years) > 0:
                        self.warning_text.append(
                    '** The input file for %s forcing option 1 contains entries'
                    %self.name)
                        self.warning_text.append(
                    'for years outside the %d-year simulation period: years %s'
                    %(years,check_years)) 
                        self.warnings += 1
                    check_ns = []
                    for key in self.sched.keys():
                        for ns in self.sched[key]:
                            if ns < 0 or ns > 1:
                                check_ns.append(ns)
                    if len(check_ns) > 0:
                        self.error_text.append(
                    '** All values for %s in the input file for %s' 
                    %(self.name,self.name))
                        self.error_text.append(
                    'forcing option 1 should be in the range 0 - 1')
                        self.init_errors += 1                
            elif self.opt == 2:
                sched = {}
                self.sched = {}            
                f.readline()
                try:
                    for lines in f:
                        l = lines.strip().split('\t')
                        sched[int(l[0])] = map(int,l[1][1:-1].split(','))
                    for key in sched.keys():
                        if min(sched[key]) < 0:
                            self.error_text.append(
                    '** Invalid value(s) for cell identification numbers in %s'
                    %self.name)
                            self.error_text.append(
                    'option 2 input file: cell identification numbers should')
                            self.error_text.append('be positive integers')
                            self.init_errors += 1
                        elif max(sched[key]) > reefmap.reeftotal - 1:
                            self.error_text.append(
                    '** Invalid value(s) for cell identification numbers in %s'
                    %self.name)
                            self.error_text.append(
                    'option 2 input file: cell identification numbers should')
                            self.error_text.append(
                    'not exceed the number of reef cells in the input map (%d)'
                    %reefmap.reeftotal)
                            self.init_errors += 1
                        else:
                            self.sched[key] = []
                            for r in range(reefmap.reeftotal):
                                if r+1 in sched[key]:
                                    self.sched[key].append(1)
                                else:
                                    self.sched[key].append(0)
                except:
                    self.error_text.append(
                '** There are formatting errors in the input file for %s' 
                %self.name)
                    self.error_text.append(
                'option 2: please check the user documentation for formatting')
                    self.error_text.append('requirements for this file')
                    self.init_errors += 1
                f.close()
                if self.init_errors == 0:
                    check_years = []
                    for i in self.sched.keys():
                        if i > years:
                            check_years.append(i)
                    check_years.sort()
                    if len(check_years) > 0:
                        self.warning_text.append(
                    '** The input file for %s forcing option 2 contain entries'
                    %self.name)
                        self.warning_text.append(
                    'for years outside the %d-year simulation period: years %s' 
                    %(years,check_years))
                        self.warnings += 1            
        else:
            pass
        
    def nsforcID(self,reefmap,i):
        """Allocate spatial distributions of nutrification/sedimentation
        forcing effects at the specified timestep 'i'.
        """
        forcid = [0 for c in range(reefmap.reeftotal)]
        if self.opt == 1:
            forclist = {}
            for sr in range(len(self.sched[i])):
                forclist[sr] = []
                forc_cells = round(reefmap.subregs[sr]*self.sched[i][sr])
                r = 0
                while r < forc_cells:
                    id = randint(1,reefmap.subregs[sr])
                    if id not in forclist[sr]:
                        forclist[sr].append(id)
                        r += 1
            for sr in range(1,reefmap.srrange+1):
                if sr in self.sched[i]:
                    r = 0
                    for c in range(reefmap.reeftotal):
                        if reefmap.subregid[c] == sr:
                            r += 1
                            if r in forclist[sr]:
                                forcid[c] = 1
        self.forcid = forcid
    
    def hSched(self,file,reefmap,years):
        """Read hurricane forcing schedule from file."""
        if self.opt == 3:
            self.sched = {}; self.strength = {}
            sched = {}; cat = {}; prop = {}; forclist = {}
            f = open(file,'U')        
            f.readline()
            try:
                for lines in f:
                    l = lines.strip().split('\t')
                    cat[int(l[0])] = int(l[1])
                    sched[int(l[0])] = map(int,l[2][1:-1].split(','))
                for key in cat.keys():
                    if cat[key] == 1 or cat[key] == 2:
                        prop[key] = 0.33
                    elif cat[key] == 3:
                        prop[key] = 0.66
                    elif cat[key] == 4 or cat[key] == 5:
                        prop[key] = 1.0
                    else:
                        self.error_text.append(
                '**Invalid values(s) for hurricane categories in hurricane')
                        self.error_text.append(
                'forcing option 3 (all categories should be in the range 1 - 5)'
                        )
                        self.init_errors += 1
                check_sr = 0
                for i in sched.values():
                    for sr in i:
                        if sr > reefmap.srrange:
                            check_sr += 1
                if check_sr > 0:
                    self.error_text.append(
                '** Invalid value(s) for affected subregions in hurricane')
                    self.error_text.append(
                'forcing option 3 input file (subregions should be within the')
                    self.error_text.append('range 1 - %d)' %reefmap.srrange)
                    self.init_errors += 1
                if self.init_errors == 0:
                    for i in sched.keys():
                        forclist[i] = {}
                        self.sched[i] = [0 for c in range(reefmap.reeftotal)]
                        for s in sched[i]:
                            forclist[i][s] = []
                            forc_cells = round(reefmap.subregs[s-1]*prop[i])
                            r = 0
                            while r < forc_cells:
                                id = randint(1,reefmap.subregs[s-1])
                                if id not in forclist[i][s]:
                                    forclist[i][s].append(id)
                                    r += 1
                        for sr in range(1,reefmap.srrange+1):
                            if sr in sched[i]:
                                r = 0
                                for c in range(reefmap.reeftotal):
                                    if reefmap.subregid[c] == sr:
                                        r += 1
                                        if r in forclist[i][sr]:
                                            self.sched[i][c] = 1
            except:
                self.error_text.append(
            '** There are formatting errors in the input for hurricane forcing')
                self.error_text.append(
            'option 3: please check the user documentation for formatting')
                self.error_text.append('requirements for this file')
                self.init_errors += 1
            f.close()    
            if self.init_errors == 0:
                check_years = []
                for i in self.sched.keys():
                    if i > years:
                        check_years.append(i)
                check_years.sort()
                if len(check_years) > 0:
                    self.warning_text.append(
            '** The input file for hurricane forcing option 3 contains entries')
                    self.warning_text.append(
            'for years outside the %d-year simulation period: years %s'
                %(years,check_years))
                    self.warnings += 1
        else:
            pass
        
    def hforcID(self,reefmap,max_sr,min_cat,max_cat,years,i):
        """Allocate spatial distributions of hurricane forcing effects 
        at the specified timestep 'i'.
        """
        forcid = [0 for c in range(reefmap.reeftotal)]
        forclist = {}
        strength = randint(min_cat,max_cat)
        if self.opt == 2:
            p = float(i)/float(years)
            r = random()
            if r < p and strength != max_cat:
                strength += 1
        if strength == 1: prop = 0.33
        elif strength == 2: prop = 0.33
        elif strength == 3: prop = 0.66
        elif strength == 4: prop = 1.0
        elif strength == 5: prop = 1.0
        sregs = randint(1,max_sr)
        rand_sr = []
        r = 0
        while r < sregs:
            sr = randint(1,reefmap.srrange)
            if sr not in rand_sr:
                rand_sr.append(sr)
                r += 1
        for sr in rand_sr:
            forclist[sr] = []
            forc_cells = round(reefmap.subregs[sr-1]*prop)
            r = 0
            while r < forc_cells:
                id = randint(1,reefmap.subregs[sr-1])
                if id not in forclist[sr]:
                    forclist[sr].append(id)
                    r += 1
        for sr in range(1,reefmap.srrange+1):
            if sr in rand_sr:
                r = 0
                for c in range(reefmap.reeftotal):
                    if reefmap.subregid[c] == sr:
                        r += 1
                        if r in forclist[sr]:
                            forcid[c] = 1
        self.forcid = forcid 
        self.rand_sr = rand_sr
        self.strength = strength
        
    def cmSched(self,cmfile,reefmap,years):
        """Read coral mortality schedule from file."""
        if self.opt == 2:
            sched = {}; self.cm_C = []
            f = open(cmfile,'U')        
            f.readline()
            try:
                for lines in f:
                    l = lines.strip().split('\t')
                    sched[int(l[0])] = map(int,l[2][1:-1].split(','))
                    self.cm_C.append(map(float,l[1][1:-1].split(',')))
                self.sched = {}
                for i in sched.keys():
                    self.sched[i] = [0 for c in range(reefmap.reeftotal)]
                    for sr in range(1,reefmap.srrange+1):
                        if sr in sched[i]:
                            for c in range(reefmap.reeftotal):
                                if reefmap.subregid[c] == sr:
                                    self.sched[i][c] = 1 
            except:
                self.error_text.append(
            '** There are formatting errors in the input for coral mortality')
                self.error_text.append(
            'forcing option 2: please check the user documentation for')
                self.error_text.append('formatting requirements for this file')
                self.init_errors += 1
            f.close()
            if self.init_errors == 0:
                check_years = []
                for i in self.sched.keys():
                    if i > years:
                        check_years.append(i)
                check_years.sort()
                if len(check_years) > 0:
                    self.warning_text.append(
            '** The input file for coral mortality forcing option 2 contains')
                    self.warning_text.append(
            'entries for years outside the %d-year simulation period: years %s'
                %(years,check_years))
                    self.warnings += 1
                check_cm_C = []
                check_minmax = 0
                for i in self.cm_C:
                    if i[0] > 1.0 or i[0] < 0.0:
                        check_cm_C.append(i[0])
                    if len(i) == 2:
                        if i[1] > 1.0 or i[1] < 0.0:
                            check_cm_C.append(i[1])
                        if i[1] < i[0]:
                            check_minmax += 1
                if len(check_cm_C) > 0:
                    self.error_text.append(
                '** Invalid value(s) for damage in coral mortality option 2')
                    self.error_text.append(
                'input file (all values should be in the range 0 - 1)')
                    self.init_errors += 1
                if check_minmax > 0:
                    self.error_text.append(
                '** Invalid value(s) for damage in coral mortality option 2')
                    self.error_text.append(
                'input file (maximum mortality should be greater than minimum')
                    self.error_text.append(
                'mortality for each event)')
                    self.init_errors += 1
                check_sr = 0
                for i in sched.values():
                    for sr in i:
                        if sr > reefmap.srrange:
                            check_sr += 1
                if check_sr > 0:
                    self.error_text.append(
        '** Invalid value(s) for affected subregions in coral')
                    self.error_text.append(
        'mortality 2 input file (subregions should be within the range 1 - %d)'
                    %reefmap.srrange)
                    self.init_errors += 1
        elif self.opt == 3:
            f = open(cmfile,'U')
            self.cmcells = []
            try:
                for lines in f:
                    self.cmcells.append(int(lines)-1)
                if min(self.cmcells) < 0:
                    self.error_text.append(
                '** Invalid value(s) for cell identification numbers in coral')
                    self.error_text.append(
                'mortality 3 input file: cell identification numbers should be')
                    self.error_text.append(
                'positive integers')
                    self.init_errors += 1
                if max(self.cmcells) > reefmap.reeftotal - 1:
                    self.error_text.append(
                '** Invalid value(s) for cell identification numbers in coral')
                    self.error_text.append(
                'mortality 3 input file: cell identification numbers should')
                    self.error_text.append(
                'not exceed the number of reef cells in the input map (%d)'
                    %reefmap.reeftotal)
                    self.init_errors += 1
            except:
                self.error_text.append(
            '** There are formatting errors in the input for coral mortality')
                self.error_text.append(
            'forcing option 3: please check the user documentation for')
                self.error_text.append('formatting requirements for this file')
                self.init_errors += 1
            f.close()
        else:
            pass
        
    def cmforcID(self,reefmap,max_sr):
        """Allocate spatial distributions of coral mortality forcing 
        effects at the specified timestep 'i'.
        """
        forcid = [0 for c in range(reefmap.reeftotal)]       
        rand_sr = []
        if self.opt == 1:
            sregs = randint(1,max_sr)
            r = 0
            while r < sregs:
                sr = randint(1,reefmap.srrange)
                if sr not in rand_sr:
                    rand_sr.append(sr)
                    r += 1
            for sr in range(1,reefmap.srrange+1):
                if sr in rand_sr:
                    r = 0
                    for c in range(reefmap.reeftotal):
                        if reefmap.subregid[c] == sr:
                            forcid[c] = 1
        elif self.opt == 3:
            for i in range(reefmap.reeftotal):
                if i in self.cmcells:
                    forcid[i] = 1
        self.forcid = forcid
        self.rand_sr = rand_sr
        
    def fSched(self,ffile,reefmap,years):
        """Read fishing pressure schedule from file."""
        if self.opt == 2:
            f = open(ffile,'U')
            f.readline()
            self.sched = {}
            try:
                for lines in f:
                    l = lines.split('\t')
                    if len(l) == reefmap.srrange + 1:
                        self.sched[int(l[0])] = []
                        for sr in range(1,len(l)):
                            self.sched[int(l[0])].append(float(l[sr]))
                    else:
                        self.error_text.append(
                '** The number of columns in the input file for fishing')
                        self.error_text.append(
                'pressure option 2 is incorrect: please check the user')
                        self.error_text.append(
                'documentation for formatting requirements for this file')
                        self.init_errors += 1
            except:
                self.error_text.append(
                '** There are formatting errors in the input file for fishing')
                self.error_text.append(
                'pressure option 2: please check the user documentation for')
                self.error_text.append('formatting requirements for this file')
                self.init_errors += 1
            f.close()
            if self.init_errors == 0:
                check_years = []
                for i in range(1,years+1):
                    if i not in self.sched.keys():
                        check_years.append(i)
                if len(check_years) > 0:
                    self.error_text.append(
                '** The input file for fishing pressure option 2 is missing')
                    self.error_text.append(
                'fishing pressure values for years %s' %check_years) 
                    self.init_errors += 1
                check_years = []
                for i in self.sched.keys():
                    if i not in range(1,years+1):
                        check_years.append(i)
                if len(check_years) > 0:
                    self.warning_text.append(
            '** The input file for fishing pressure option 2 contains entries')
                    self.warning_text.append(
            'for years outside the %d-year simulation period: years %s'
                %(years,check_years)) 
                    self.warnings += 1
                check_fish = []
                for key in self.sched.keys():
                    for fish in self.sched[key]:
                        if fish < 0:
                            check_fish.append(fish)
                if len(check_fish) > 0:
                    self.error_text.append(
            '** All values for fishing pressure in the input file for fishing')
                    self.error_text.append(
            'pressure option 2 should be positive')
                    self.init_errors += 1
        elif self.opt == 3:
            f = open(ffile,'U')
            self.mpa = []
            try:
                for lines in f:
                    self.mpa.append(int(lines)-1)
                if min(self.mpa) < 0:
                    self.error_text.append(
            '** Invalid value(s) for cell identification numbers in fishing')
                    self.error_text.append(
            'pressure option 3 input file: cell identification numbers should')
                    self.error_text.append(
            'be positive integers')
                    self.init_errors += 1
                if max(self.mpa) > reefmap.reeftotal - 1:
                    self.error_text.append(
            '** Invalid value(s) for cell identification numbers in fishing')
                    self.error_text.append(
            'pressure option 3 input file: cell identification numbers should')
                    self.error_text.append(
            'not exceed the number of reef cells in the input map (%d)'
                    %reefmap.reeftotal)
                    self.init_errors += 1
            except:
                self.error_text.append(
            '** There are formatting errors in the input for fishing pressure')
                self.error_text.append(
            'option 3: please check the user documentation for formatting')
                self.error_text.append('requirements for this file')
                self.init_errors += 1
            f.close()
        else:
            pass
    
    def dfSched(self,dffile,reefmap,years):
        """Read destructive fishing pressure schedule from file."""
        if self.opt == 1:
            f = open(dffile,'U')
            f.readline()
            self.sched = {}
            try:
                for lines in f:
                    l = lines.split('\t')
                    if len(l) == reefmap.srrange + 1:
                        self.sched[int(l[0])] = []
                        for sr in range(1,len(l)):
                            self.sched[int(l[0])].append(float(l[sr]))
                    else:
                        self.error_text.append(
                '** The number of columns in the input file for destructive')
                        self.error_text.append(
                'fishing forcing option 1 is incorrect: please check the user')
                        self.error_text.append(
                'documentation for formatting requirements for this file')
                        self.init_errors += 1
            except:
                self.error_text.append(
            '** There are formatting errors in the input file for destructive')
                self.error_text.append(
            'fishing forcing option 1: please check the user documentation for')
                self.error_text.append(
            'formatting requirements for this file')
                self.init_errors += 1
            f.close()
            if self.init_errors == 0:
                check_years = []
                for i in range(1,years+1):
                    if i not in self.sched.keys():
                        check_years.append(i)
                if len(check_years) > 0:
                    self.error_text.append(
                '** The input file for destructive fishing forcing option 1 is')
                    self.error_text.append(
                'missing values for years %s' %check_years) 
                    self.init_errors += 1
                check_years = []
                for i in self.sched.keys():
                    if i not in range(1,years+1):
                        check_years.append(i)
                if len(check_years) > 0:
                    self.warning_text.append(
        '** The input file for destructive fishing forcing option 1 contains')
                    self.warning_text.append(
        'entries for years outside the %d-year simulation period: yeras %s'
            %(years,check_years))
                    self.warnings += 1
        else:
            pass
                                
    def dfforcID(self,reefmap,i):
        """Allocate spatial distributions of destructive fishing effect
        at the specified timestep 'i'.
        """
        forcid = [0 for c in range(reefmap.reeftotal)]
        forclist = {}
        for sr in range(len(self.sched[i])):
            forclist[sr] = []
            forc_cells = round(reefmap.subregs[sr]*self.sched[i][sr])
            r = 0
            while r < forc_cells:
                id = randint(1,reefmap.subregs[sr])
                if id not in forclist[sr]:
                    forclist[sr].append(id)
                    r += 1
        for sr in range(1,reefmap.srrange+1):
                if sr in self.sched[i]:
                    r = 0
                    for c in range(reefmap.reeftotal):
                        if reefmap.subregid[c] == sr:
                            r += 1
                            if r in forclist[sr]:
                                forcid[c] = 1
        self.forcid = forcid
    
            
                
            
            
            
    
