#!/usr/bin/env python
from __future__ import division
import numpy as np# reshape
import os
from datetime import date
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from netCDF4 import Dataset
import taylorDiagram_sl as td
from matplotlib.collections import LineCollection
from td_util import *
#from collections import OrderedDict
'''
methods in taylorDiagram.py 
def taylor_ax(fig, rect, **kw): draw the transformed thera-radius basci frame
def add_contour(aux_ax, **kw): add the centered rms contour 
def add_ref_contour(aux_ax, *args, **kw): add the reference arc across the obs point 
def add_sample(aux_ax, corrcoef, ratio, samples, *args, **kwargs): add samples into the diagram
'''


var_data=cal_td()
var_samples=dict_transform(sub_regions,var_data)
# from:{casename:([cc_reg1,cc_reg_2,...cc_reg10],[ratio_reg1,...ratio_reg10])}
# to:{XinJiang:[[case1,ratio,cc],[case2,ratio,cc]...[caseN,ratio,cc]],Northwrst:[],...,WesTibet:[]}



'''
================samples from grd form====================================
nick_names=["Case%2.2d" %p for p in range(1,31)]
cc_samples=np.random.rand(len(sub_regions),len(nick_names))
ratio_samples=np.random.rand(len(sub_regions),len(nick_names))*1.5

for j, region in enumerate(sub_regions):
    samples[region]=[]
    for i, case_name in enumerate(nick_names):
        samples[region].append([case_name, cc_samples[j,i], ratio_samples[j,i]])
'''

#=================plotting loop============================================================
fig=plt.figure(figsize=(16, 8))
rects=[251,252,253,254,255,256,257,258,259,(2,5,10)]
#rects=[341,342,343,344,345,346,347,348,337,338]
plt.subplots_adjust(top=0.8,bottom=0.1,wspace=0.1, hspace = -0.1,)
left_axis=(5,6,7,8,9)  # bottom axis
right_axis=(0,5) # left axis
ms_list=set_ms_list(case_cate_num, colors, marks, fillstyles) #marker style list

for i, rect in enumerate(rects):
    if isinstance(rect,int):
        ax,aux_ax=td.taylor_ax(fig, rect, th1=0., th2=np.pi/2, rd1=0., rd2=2.5)
    else:  #5,2,10 or *(5,2,10)    
        ax,aux_ax=td.taylor_ax(fig, *rect, th1=0., th2=np.pi/2, rd1=0., rd2=2.5)
    
 # adjust the visibility of corresponding major_ticklables, major_ticks, and labels  
    ax.axis["left"].label.set_visible(i in left_axis)
    ax.axis["left"].major_ticklabels.set_visible( i in left_axis)
    ax.axis["right"].major_ticklabels.set_visible( i in right_axis)

    # add centered rms contours 
    contour=td.add_contour(aux_ax,  6, colors='black', linestyles='dashed', lw=0.4)
    #clabel: label contour plot
    #ax.clabel(contour,  fontsize=8, fmt='%.1f', inline=1 )
 
    # add the arc which pass the obs point
    td.add_ref_contour(aux_ax, 'm--',c='red', lw=1.)

    #draw reference point; l: class 'matplotlib.lines.Line2D'
    l, = aux_ax.plot(0., 1., 'ko',  ls='', ms=5, clip_on=False)

    # add samples to the diagram
    lines=[] # the sample list saving the relevant info to be used afterwards
    for j, (case_name, ratio, cc) in enumerate(var_samples[sub_regions[i]]):
        td.add_sample(aux_ax, cc, ratio, lines,ls='', ms=5, label=case_name, clip_on=True, **ms_list[j] )
    
    # add title to each axes
    ax.set_title(sub_regions[i],{'fontsize':10},position=(0.95,1.),ha='right',va='top',color='red')
    
    # add var name into the first plot
    #ax.text(0.35,1.75,VAR,fontsize=12,ha='right',va='bottom',visible=(i==0))



#handlelength=2.5, handleheight=3
labels=[p.get_label() for p in lines] # list for loop
labels=['mp_lin','mp_wsm6','mp_etamp','mp_thompson','mp_morrison','mp_morrison/ar','mp_wdm6',
        'ra_cccma','ra_cawcr','ra_cam','ra_fuliou','ra_gfdl','ra_rrtmg',
        'cu_kfeta','cu_bmj','cu_grell','cu_tiedtke','cu_nsas','cu_donner','cu_emanuel',
        'bl_ysu','bl_mynn','bl_boulac','bl_acm','bl_uw',
        'sf_noah','ctl','ens']
#print (labels)
fig.suptitle(VAR+'('+SEASON+')', fontsize=16,x=0.1,y=0.45,rotation=90,ha='center',va='center')
leg=fig.legend(lines, labels,ncol=5, numpoints=1,  
    prop=dict(size='small'), loc=(0.6,0.82), frameon=False, columnspacing=0.2)
#fig.tight_layout()
pic_name=Pattern+'_'+SEASON+'_'+VAR+'_td.pdf'
print pic_name
plt.savefig(pic_name, dpi=900)
plt.show()
