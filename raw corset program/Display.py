from numpy import *
from pylab import *

class Display:
    """Display and save model output using pylab.

       plotEndSR      -- Plot final cover/biomass for each subregion as a 
                         bar chart.
       plotDynamics   -- Plot changes in average cover/biomass over the time 
		         series for the entire region.
       plotDynamicsSR -- Plot changes in average cover/biomass over the time 
			 series for each subregion.
       plotCatchSR    -- Plot changes in average fish catches over the time 
		         series for each subregion.
       savePlot       -- Save plots.
    """

    def plotEndSR(self,reefmap,params,output):
	"""Plot final cover/biomass for each subregion as a bar chart."""
	self.figure1 = figure(1)
	subplot(111, axisbg='0.9')
	grid(color='w', linestyle='-', linewidth=0.5)
	title('Benthic cover: year %d' %params.years,size='large')
	labels = [0 for r in range(reefmap.srrange)]
	C = []; T = []; M = []; E = []
	CE = []; TE = []; ME = []; EE = []
	for r in range(reefmap.srrange):
	    labels[r] = reefmap.srnames[r+1]
	    C.append(output.outavsSR['C'][r][-1])
	    CE.append(output.outCIsSR['C'][r][-1][1]
			-output.outavsSR['C'][r][-1])
	    T.append(output.outavsSR['T'][r][-1])
	    TE.append(output.outCIsSR['T'][r][-1][1]
		-output.outavsSR['T'][r][-1])
	    M.append(output.outavsSR['M'][r][-1])
	    ME.append(output.outCIsSR['M'][r][-1][1]
			-output.outavsSR['M'][r][-1])
	    E.append(output.outavsSR['E'][r][-1])
	    EE.append(output.outCIsSR['E'][r][-1][1]
			-output.outavsSR['E'][r][-1])	
	ind = arange(reefmap.srrange)
	width = 0.8/4
	p1 = bar(ind+0.5*width,C,yerr=CE,width=width,color=(1,1,0.5),
		 ecolor='k')
	p2 = bar(ind+1.5*width,T,yerr=TE,width=width,color=(0,0.5,0),
		 ecolor='k')
	p3 = bar(ind+2.5*width,M,yerr=ME,width=width,color=(0.4,0.4,1),
		 ecolor='k')
	p4 = bar(ind+3.5*width,E,yerr=EE,width=width,color=(0.5,0,0),
		 ecolor='k')
	ylim(0,140)
	yticks(arange(0, 140, 20),('0','20','40','60','80','100',''))
	ylabel('Mean cover (%)')
	xticks(ind+2.5*width, labels)
	self.figure1.autofmt_xdate()
	leg=legend((p1[0],p2[0],p3[0],p4[0]),('Coral','Macroturf',
					  'Macroalgae','EAC'),loc=2,shadow=True)
	ax = gca()
	ax.set_axisbelow(True) 
	
	self.figure2 = figure(2)
	subplot(111, axisbg='0.9')
	grid(color='w', linestyle='-', linewidth=0.5)
	title('Consumer biomass: year %d' %params.years,size='large')
	H = []; Ps = []; Pl = []; U = []
	HE = []; PsE = []; PlE = []; UE = []
	for r in range(reefmap.srrange):
	    H.append(output.outavsSR['H'][r][-1])
	    HE.append(output.outCIsSR['H'][r][-1][1]
			-output.outavsSR['H'][r][-1])
	    Ps.append(output.outavsSR['Ps'][r][-1])
	    PsE.append(output.outCIsSR['Ps'][r][-1][1]
		-output.outavsSR['Ps'][r][-1])
	    Pl.append(output.outavsSR['Pl'][r][-1])
	    PlE.append(output.outCIsSR['Pl'][r][-1][1]
			-output.outavsSR['Pl'][r][-1])
	    U.append(output.outavsSR['U'][r][-1])
	    UE.append(output.outCIsSR['U'][r][-1][1]
			-output.outavsSR['U'][r][-1])	
	ind = arange(reefmap.srrange)
	width = 0.8/4
	p1 = bar(ind+0.5*width,H,yerr=HE,width=width,
		 color=(0.57,0.93,0.57),ecolor='k')
	p2 = bar(ind+1.5*width,Ps,yerr=PsE,width=width,color=(1,0.75,0.8),
		 ecolor='k')
	p3 = bar(ind+2.5*width,Pl,yerr=PlE,width=width,
		 color=(0.53,0.81,0.98),ecolor='k')
	p4 = bar(ind+3.5*width,U,yerr=UE,width=width,color=(1,0.65,0),
		 ecolor='k')
	ylim(0,70000)
	yticks(arange(0, 70000, 10000),('0','10','20','30','40','50','60',''))
	ylabel('Mean biomass (kg/km$^2$ x 10$^3$)')
	xticks(ind+2.5*width, labels)
	self.figure2.autofmt_xdate()
	leg=legend((p1[0],p2[0],p3[0],p4[0]),('Herbivores','Small piscivores',
				'Large piscivores','Urchins'),loc=2,shadow=True)
	ax = gca()
	ax.set_axisbelow(True) 
	
    def plotDynamics(self,reefmap,params,output):
	"""Plot changes in average cover/biomass over the time series."""
	figure(3)
        subplot(4,2,1, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	title('Benthic cover (%)',fontsize=12)
	if params.runs > 1:
	    plot(range(1,params.years+1),output.outCIs['C'],color='gray',
		 linestyle=':')
	plot(range(1,params.years+1),output.outavs['C'],color=(1,1,0.5),
	     linewidth=2)
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	ylim(0,100)
	yticks(arange(0, 101, 20),('0','20','40','60','80','100'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Corals',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	
	subplot(4,2,3, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	if params.runs > 1:
	    plot(range(1,params.years+1),output.outCIs['T'],color='gray',
		 linestyle=':')
	plot(range(1,params.years+1),output.outavs['T'],color=(0,0.5,0),
	     linewidth=2)
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	ylim(0,100)
	yticks(arange(0, 101, 20),('0','20','40','60','80','100'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Macroturf',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	
	subplot(4,2,5, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	if params.runs > 1:
	    plot(range(1,params.years+1),output.outCIs['M'],color='gray',
		 linestyle=':')
	plot(range(1,params.years+1),output.outavs['M'],color=(0.4,0.4,1),
	     linewidth=2)
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	ylim(0,100)
	yticks(arange(0, 101, 20),('0','20','40','60','80','100'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Macroalge',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	
	subplot(4,2,7, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	if params.runs > 1:
	    plot(range(1,params.years+1),output.outCIs['E'],color='gray',
		 linestyle=':')
	plot(range(1,params.years+1),output.outavs['E'],color=(0.5,0,0),
	     linewidth=2)
	xlabel('year')
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(xticklabels,fontsize=8)
	ylim(0,100)
	yticks(arange(0, 101, 20),('','20','40','60','80','100'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('EAC',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	
	subplot(4,2,2, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	title('Consumer biomass (kg/km$^2$ x 10$^3$)',fontsize=12)
	if params.runs > 1:
	    plot(range(1,params.years+1),output.outCIs['H'],color='gray',
		 linestyle=':')
	plot(range(1,params.years+1),output.outavs['H'],
	     color=(0.57,0.93,0.57),linewidth=2)
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	ylim(0,60000)
	yticks(arange(0, 61000, 10000),('0','10','20','30','40','50','60'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Herbivores',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	
        subplot(4,2,4, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	if params.runs > 1:
	    plot(range(1,params.years+1),output.outCIs['Ps'],color='gray',
		 linestyle=':')
	plot(range(1,params.years+1),output.outavs['Ps'],color=(1,0.75,0.8),
	     linewidth=2)
	xlim(1,params.years)
    	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	ylim(0,60000)
	yticks(arange(0, 61000, 10000),('0','10','20','30','40','50','60'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Small piscivores',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
        
        subplot(4,2,6, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	if params.runs > 1:
	    plot(range(1,params.years+1),output.outCIs['Pl'],color='gray',
		 linestyle=':')
	plot(range(1,params.years+1),output.outavs['Pl'],
	     color=(0.53,0.81,0.98),linewidth=2)
	xlim(1,params.years)
    	xticklabels = getp(gca(),'xticklabels')
	ylim(0,60000)
	yticks(arange(0, 61000, 10000),('0','10','20','30','40','50','60'))
	setp(gca(),xticklabels=[])
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Large piscivores',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
        
        subplot(4,2,8, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	if params.runs > 1:
	    plot(range(1,params.years+1),output.outCIs['U'],color='gray',
		 linestyle=':')
	plot(range(1,params.years+1),output.outavs['U'],color=(1,0.65,0),
	     linewidth=2)
	xlabel('year')
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(xticklabels,fontsize=8)
	ylim(0,60000)
	yticks(arange(0, 61000, 10000),('','10','20','30','40','50','60'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Urchins',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	self.figure3 = figure(3)
        
    def plotDynamicsSR(self,reefmap,params,output):
        """Plot changes in average cover/biomass over the time series
        for each subregion.
        """
        
        figure(4)
	labels = [0 for r in range(reefmap.srrange)]
	for r in range(1,reefmap.srrange+1):
	    labels[r-1] = reefmap.srnames[r]
	labels = tuple(labels)
	colors=['r','b','g','y','m','c','k','gray']
        subplot(4,2,1, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	title('Benthic cover (%)',fontsize=12)
	for r in range(reefmap.srrange):
	    plot(range(1,params.years+1),output.outavsSR['C'][r],
		 color=colors[r])
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	ylim(0,100)
	yticks(arange(0, 101, 20),('0','20','40','60','80','100'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Corals',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	
	subplot(4,2,3, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	for r in range(reefmap.srrange):
	    plot(range(1,params.years+1),output.outavsSR['T'][r],
		 color=colors[r])
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	ylim(0,100)
	yticks(arange(0, 101, 20),('0','20','40','60','80','100'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Macroturf',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	
	subplot(4,2,5, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	for r in range(reefmap.srrange):
	    plot(range(1,params.years+1),output.outavsSR['M'][r],
		 color=colors[r])
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	ylim(0,100)
	yticks(arange(0, 101, 20),('0','20','40','60','80','100'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Macroalge',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	
	subplot(4,2,7, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	for r in range(reefmap.srrange):
	    plot(range(1,params.years+1),output.outavsSR['E'][r],
		 color=colors[r])
	xlabel('year')
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(xticklabels,fontsize=8)
	ylim(0,100)
	yticks(arange(0, 101, 20),('','20','40','60','80','100'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('EAC',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	
	subplot(4,2,2, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	title('Consumer biomass (kg/km$^2$ x 10$^3$)',fontsize=12)
	for r in range(reefmap.srrange):
	    plot(range(1,params.years+1),output.outavsSR['H'][r],
		 color=colors[r])
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	ylim(0,60000)
	yticks(arange(0, 61000, 10000),('0','10','20','30','40','50','60'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Herbivores',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	
        subplot(4,2,4, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	for r in range(reefmap.srrange):
	    plot(range(1,params.years+1),output.outavsSR['Ps'][r],
		 color=colors[r])
	xlim(1,params.years)
    	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	ylim(0,60000)
	yticks(arange(0, 61000, 10000),('0','10','20','30','40','50','60'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Small piscivores',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
        
        subplot(4,2,6, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	for r in range(reefmap.srrange):
	    plot(range(1,params.years+1),output.outavsSR['Pl'][r],
		 color=colors[r])
	xlim(1,params.years)
    	xticklabels = getp(gca(),'xticklabels')
	ylim(0,60000)
	yticks(arange(0, 61000, 10000),('0','10','20','30','40','50','60'))
	setp(gca(),xticklabels=[])
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Large piscivores',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
        
        subplot(4,2,8, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	line = []
	for r in range(reefmap.srrange):
	    plt = plot(range(1,params.years+1),output.outavsSR['U'][r],
		       color=colors[r])
	    line.append(plt)
	xlabel('year')
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(xticklabels,fontsize=8)
	ylim(0,60000)
	yticks(arange(0, 61000, 10000),('','10','20','30','40','50','60'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Urchins',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	line=tuple(line)
	try:
	    leg = figlegend(line,labels,'center right',labelspacing=0,
			    borderpad=0)
        except:
	    leg = figlegend(line,labels,'center right',labelsep=0,pad=0)
	texts = leg.get_texts()
	leg.draw_frame(False)
	setp(texts, fontsize=8)
	subplots_adjust(right = 0.78, wspace = 0.3)
	self.figure4 = figure(4)
	
    def plotCatchSR(self,reefmap,params,output):
        """Plot changes in average fish catches over the time series
        for each subregion.
        """
        
        figure(5)
	labels = [0 for r in range(reefmap.srrange)]
	for r in range(1,reefmap.srrange+1):
	    labels[r-1] = reefmap.srnames[r]
	labels = tuple(labels)
	colors=['r','b','g','y','m','c']
	subplot(3,3,2, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	title('Fish catches (kg/km$^2$ x 10$^3$)',fontsize=12)
	for r in range(reefmap.srrange):
	    plot(range(1,params.years+1),
		 array(output.outavsSR['catchH'][r])*0.001,color=colors[r])
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	#ylim(0,10000)
	#yticks(arange(0, 11000, 2000),('0','2','4','6','8','10'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Herbivores',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	
        subplot(3,3,5, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	for r in range(reefmap.srrange):
	    plot(range(1,params.years+1),
		 array(output.outavsSR['catchPs'][r])*0.001,color=colors[r])
	xlim(1,params.years)
    	xticklabels = getp(gca(),'xticklabels')
	setp(gca(),xticklabels=[])
	#ylim(0,10000)
	#yticks(arange(0, 11000, 2000),('0','2','4','6','8','10'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Small piscivores',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
        
        subplot(3,3,8, axisbg='0.9')
	grid(color='0.95', linestyle='-', linewidth=0.5)
	line = []
	for r in range(reefmap.srrange):
	    plt = plot(range(1,params.years+1),
		  array(output.outavsSR['catchPl'][r])*0.001,color=colors[r])
	    line.append(plt)
	xlabel('year')
	xlim(1,params.years)
	xticklabels = getp(gca(),'xticklabels')
	setp(xticklabels,fontsize=8)
	#ylim(0,10000)
	#yticks(arange(0, 11000, 2000),('0','2','4','6','8','10'))
	yticklabels = getp(gca(),'yticklabels')
        setp(yticklabels,fontsize=8)
	ylabel('Large piscivores',fontsize=10)
	ax = gca()
	ax.set_axisbelow(True)
	line=tuple(line)
	try:
	    leg = legend(line,labels,'center right',labelspacing=0,
			    borderpad=0)
        except:
	    leg = legend(line,labels,'center right',labelsep=0,pad=0)
	texts = leg.get_texts()
	leg.draw_frame(False)
	setp(texts, fontsize=10)
	subplots_adjust(wspace = -0.5)
	self.figure5 = figure(5)
    
    def savePlot(self,fname,scen):
        fname1 = fname + scen + '_benthic_bar'
        self.figure1.savefig(fname1)
        fname2 = fname + scen + '_consumer_bar'
        self.figure2.savefig(fname2)
        fname3 = fname + scen + '_means'
        self.figure3.savefig(fname3)
        fname4 = fname + scen + '_meansSR'
        self.figure4.savefig(fname4)
	fname5 = fname + scen + '_catch'
	self.figure5.savefig(fname5)
        