from numpy import *

class Map:
    """Read in base-map of reef cell locations, and subregion ids."""
    
    def __init__(self):
        self.init_errors = 0
        self.error_text = []
    
    def reefmap(self,pathname,forc_hurr,forc_cm,hmax_sr,cmmax_sr):
        """Read in map defining location of reef cells
           and subregions for initial conditions.
        
           reefmap   -- location of reef cells
           width     -- x dimension of reefmap
           length    -- y dimension of reefmap
           srrange   -- number of subregions
           subregs   -- list containing number of reef cells
                        in each subregion
           subregid  -- list identifying which subregions cells belong to
           reeftotal -- number of reef cells in reefmap
        """
        
        inputmap = open(pathname,'U')
        try:
            self.cell_x = float(inputmap.readline()) # x dimension of cells
            self.cell_y = float(inputmap.readline()) # y dimension of cells
            self.cell_area = self.cell_x*self.cell_y # cell area
        except:
            self.error_text.append(
                '** The first two lines of "%s" should be float values' 
                %pathname)
            self.error_text.append(
                'that specify the x and y dimensions of grid cells')
            self.init_errors += 1
        
        if self.init_errors == 0:
            self.reefmap = []
            for lines in inputmap:
                try:
                    self.reefmap.append(map(int, lines.split(',')))
                except:
                    self.error_text.append(
                '** Problem with formatting of raster data in map input file:')
                    self.error_text.append(
                'see user documentation for formatting requirements')
                    self.init_errors += 1
            inputmap.close()
            self.reefmap = array(self.reefmap)
            self.reefmap.reshape
        
        if self.init_errors == 0:
            self.width = self.reefmap.shape[1]
            self.length = self.reefmap.shape[0]
            self.srrange = self.reefmap.max()
            if self.srrange > 8:
                self.error_text.append(
                    '** Number of subregions should not exceed 8')
                self.init_errors += 1
            if self.reefmap.min() != 0:
                self.error_text.append(
            '** Mapfile should include values = "0" to indicate the location')
                self.error_text.append(
            'of non-reef grid cells (all grid cell values should be')
                self.error_text.append('greater than or equal to zero)')
                self.init_errors += 1
            self.subregs = []
            self.subregid = []
            for i in range(self.srrange):
                self.subregs.append(0)
            self.reeftotal = 0
            for ii in range(self.length):
                for jj in range(self.width):
                    for i in range(self.srrange+1)[1:]:
                        if self.reefmap[ii,jj] == i:
                            self.subregs[i-1] +=1
                            self.subregid.append(i)
                            self.reeftotal +=1
            if self.reeftotal == 0:
                self.error_text.append(
                '** Mapfile does not contain any reef cells')
                self.init_errors += 1
            if self.reeftotal >= 25000:
                self.error_text.append(
                '** The number of reef cells in the mapfile (%d) is too big'
                %self.reeftotal)
                self.error_text.append('(should be less than 25 000)')
                self.init_errors += 1
            num = 0
            for i in range(1,max(self.subregid)+1):
                if i not in self.subregid:
                    num += 1
            if num != 0:
                self.error_text.append(
                    '**Numbering of subregions in the mapfile should be')
                self.error_text.append('consecutive and should start at "1"')
                self.init_errors += 1
            if forc_hurr in [1,2]:
                if hmax_sr > self.srrange:
                    self.error_text.append(
                '** Value for "hmax_sr" in the input file should be less than')
                    self.error_text.append(
                'or equal to the number of subregions in the mapfile')
                    self.error_text.append('(current value of "%s" is invalid)' 
                                           %hmax_sr)
                    self.init_errors += 1
            if forc_cm in [1,3]:
                if cmmax_sr > self.srrange:
                    self.error_text.append(
                '** Value for "cmmax_sr" in the input file should be less than')
                    self.error_text.append(
                'or equal to the number of subregions in the mapfile')
                    self.error_text.append('(current value of "%s" is invalid)' 
                                           %cmmax_sr)
                    self.init_errors += 1
                        
    def srnames(self,pathname):
        """Read in names of subregions."""
        self.srnames = {}
        names = open(pathname,'U')
        names.readline()
        for lines in names:
            l = lines.split(',')
            self.srnames[int(l[0])] = l[1]
        names.close()
        for i in range(1,max(self.subregid)+1):
            if i not in self.srnames.keys():
                self.error_text.append(
                    'Subregions listed in "%s" should correspond' %pathname)
                self.error_text.append(
                    'with subregions identified in the mapfile')
                self.error_text.append('(subregion %i is missing)' %i)
                self.init_errors += 1