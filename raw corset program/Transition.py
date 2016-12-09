from numpy import *
from random import *
from Map import Map

class Transition:
    """Format transition matrices for larval transport.

       makeTMR     -- Make a transition matrix for retention only (no 
                      dispersal).
       readTM      -- Read a transition matrix from file.
       polytocell  -- Define the transition polygon to reef cell mapping.
       adjustTM    -- Remove empty and illegal (boundary affected) polygons
                      as sources.
       adjustPCmap -- Remove empty and illegal (boundary affected) polygons 
	              from the polygon-cell mapping.
    """
    
    def __init__(self):
        self.init_errors = 0
        self.error_text = []

    def makeTMR(self,pctotal,dlarv,run):
        """Make a transition matrix for retention only (no dispersal)."""
	
        self.transition = identity(pctotal)
        for i in range(pctotal):
            if self.transition[i,i] == 1:
		for j in range(run+1):
                    rand = uniform(0.0,1.0)
		if type(dlarv) == list:
		    d = rand*(dlarv[1] - dlarv[0]) + dlarv[0]
		else: d = dlarv
                self.transition[i,i] = (1-d)
        return self.transition
    
    def readTM(self,pathname):
        """Read a transition matrix from file.
        
	   ext_num     -- number of cells in the fixed external source
	   ext_source  -- larval inputs from fixed external source
           transitionp -- transition matrix for reef polygons
	   ptotal      -- the number of transition polygons
        """
        inputmatrix = open(pathname,'U')
	try:
	    ext = inputmatrix.readline().strip().split(',')
	    self.ext_num = int(ext[1])
	    if self.ext_num not in [0,1]:
		self.error_text.append(
		'** The value for "external_source" in "%s"' %pathname)
		self.error_text.append('should be either 0 (default) or 1')
		self.init_errors += 1
	except:
	    self.error_text.append(
	    '**The first line of "%s" should be either of' %pathname)
	    self.error_text.append(
		'"external_source,0" (default) or "external_source,1"')
	    self.init_errors += 1
	if self.init_errors == 0:
	    self.transitionp = []
	    try:
		for lines in inputmatrix:
		    self.transitionp.append(map(float, lines.split(',')))
		for l in self.transitionp:
		    for p in l:
			if p < 0:
			    self.error_text.append(
			    '** All transition probabilities in "%s"' %pathname)
			    self.error_text.append(
			    'should be positive values')
			    self.init_errors += 1
			if p > 1:
			    self.error_text.append(
			    '** All transition probabilities in "%s"' %pathname)
			    self.error_text.append(
			    'should be less than or equal to 1')
			    self.init_errors += 1
		self.transitionp = array(self.transitionp)
		if self.ext_num == 0:
		    if shape(self.transitionp)[0] != shape(self.transitionp)[1]:
			self.error_text.append(
			'** The number of rows and columns in "%s"' %pathname)
			self.error_text.append(
			'should be equal given "external_source,0"')
			self.init_errors += 1
		if self.ext_num == 1:
		    if shape(self.transitionp)[0] != \
		       shape(self.transitionp)[1] + 1:
			self.error_text.append(
		'** The number of rows should be one greater than the number')
			self.error_text.append(
		'of columns in "%s" given "external_source,1"' %pathname)
			self.init_errors += 1
		    else:
			self.ext_source = self.transitionp[-1,:]
		self.ptotal = shape(self.transitionp)[1]
	    except:
		self.error_text.append(
		'** "%s" should contain rows of comma-separated values' 
		%pathname)
		self.error_text.append(
		'where each row has the same number of values')
		self.init_errors += 1
	inputmatrix.close()
        
    def polytocell(self,pathname,reeftotal,ptotalc,ptotalf,ptotalu):
        """Define the transition polygon to reef cell mapping.
        
           rm_source -- list of polygon IDS to remove as sources
		    (due to boundary conditions)
	   ptotal    -- the number of transition polygons
	   pctotal   -- the number of polygons that contain reef cells
	   pc_list   -- list of polygon IDs that contain reef cells
           pc_map    -- dictionary mapping polygon IDs to reef cell IDs
           pc_scale  -- dictionary defining the number of cells 
		     in each reef polygon
	   rm_empty  -- polygon IDs that contain no reef cells
        """
        
	if ptotalc != ptotalf or ptotalc != ptotalu or ptotalf != ptotalu:
	    self.error_text.append(
	'** The number of columns in transition matrices for corals, fish and')
	    self.error_text.append(
	'should be equal (#cols_corals=%d, #cols_fish=%d, #cols_urchins=%d in'
	%(ptotalc,ptotalf,ptotalu))
	    self.error_text.append('current input files')
	    self.init_errors += 1
	else:
	    self.ptotal = ptotalc
	    input = open(pathname, 'r')
	    try:
		rm = input.readline().strip().split(',')
		if rm[1] == 'none':
		    self.rm_source = []
		else:
		    self.rm_source = range(int(rm[1])-1,int(rm[2]))
	    except:
		self.error_text.append(
	    '** The first line of "%s" is formatted incorreclty:' %pathname)
		self.error_text.append(
	    'see user documentation for formatting requirements for this file')
		self.init_errors += 1
	    if self.init_errors == 0:
		input.readline(), input.readline()
		self.pc_list = []
		self.pc_map = {}
		self.pc_scale = {}
		self.pc_count = {}
		try:
		    for lines in input:
			line = lines.split(',')
			self.pc_map[int(line[0])-1] = int(line[1])-1
			if int(line[1])-1 not in self.pc_list:
			    self.pc_list.append(int(line[1])-1)
		    check_cells = []
		    for cell in range(reeftotal):
			if cell not in self.pc_map.keys():
			    check_cells.append(cell + 1)
		    if len(check_cells) > 0:
			self.error_text.append(
		    '** "%s" should contain a listing for all %d reef cells'
		    %(pathname,reeftotal))
			self.error_text.append(
		    'identified in the map input file: missing cells are %s' 
		    %check_cells)
			self.init_errors += 1
		    check_cells = []
		    for cell in self.pc_map.keys():
			if cell not in range(reeftotal):
			    check_cells.append(cell + 1)
		    if len(check_cells) > 0:
			self.error_text.append(
		'** "%s" contains cell identification numbers that do not'
		%pathname)
			self.error_text.append(
		'correspond with reef cells identified in the map input file:')
			self.error_text.append(
		'invalid cell identification numbers are %s' %check_cells)
			self.init_errors += 1
		    check_p = []
		    for p in self.pc_map.values():
			if p not in range(self.ptotal):
			    check_p.append(p + 1)
		    if len(check_p) > 0:
			self.error_text.append(
	'** "%s" contains connectivity node identification'
	%pathname)
			self.error_text.append(
	'numbers that do not correspond with the number of connectivity nodes')
			self.error_text.append(
	'identified in transition matrix inputs: invalid connectivity node')
			self.error_text.append(
	'identification numbers are %s' %check_p)
			self.init_errors += 1
		    if self.init_errors == 0:
			self.pctotal = len(self.pc_list)
			for vals in sort(self.pc_map.values()):
			    if vals not in self.pc_count.keys():
				self.pc_count[vals] = 1
			    else: self.pc_count[vals] += 1
			for cell in range(reeftotal):
			    self.pc_scale[cell] = \
				self.pc_count[self.pc_map[cell]]
			self.rm_empty = []
			for i in range(self.ptotal):
			    if i not in self.pc_map.values():
				self.rm_empty.append(i)	
		except:
		    self.error_text.append(
		    '** "%s" is formatted incorreclty: see user' %pathname)
		    self.error_text.append(
		    'documentation for formatting requirements for this file')
		    self.init_errors += 1
	    input.close()
        
    def adjustTM(self,transition):
	"""Remove empty and illegal (boundary affected) polygons as sources."""	
	for i in transition.rm_source:
	    for j in range(self.ptotal):
                self.transitionp[i][j] = 0
        index = range(self.ptotal)
        for i in range(len(index)):
	    if i in transition.rm_empty:
	        index.remove(i)
        self.transition = self.transitionp[index]
	index = range(shape(self.transition)[1])
        for i in range(len(index)):
	    if i in transition.rm_empty:
	        index.remove(i)
        self.transition = self.transition[:,index]
	
    def adjustPCmap(self,transition):
	"""Remove empty and illegal (boundary affected) polygons from the
	   polygon-cell mapping.	
        """
        poly_map = {}
	pc_list = sort(self.pc_list)
	for i in range(shape(transition)[1]):
	    poly_map[pc_list[i]] = i
	for key in self.pc_map.keys():
	    self.pc_map[key] = poly_map[self.pc_map[key]]
