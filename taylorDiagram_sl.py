#!/usr/bin/env python
# Copyright: This document has been placed in the public domain.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.projections import PolarAxes
import mpl_toolkits.axisartist.floating_axes as FA
import mpl_toolkits.axisartist as axisartist
import mpl_toolkits.axisartist.grid_finder as GF

def taylor_ax(fig, *args, **kw):
    #th1=0., th2=np.pi/3, rd1=0., rd2=1.2, tloc1=None, tloc2=None)
    tr = PolarAxes.PolarTransform()
    
    # Correlation labels
    if kw.has_key("tloc1"):
        rlocs = kw["tloc1"]
    else:
        rlocs = np.concatenate((np.arange(10)/10.,[0.95,0.99]))

    tlocs = np.arccos(rlocs)
    gl1 = GF.FixedLocator(tlocs)
    tf1 = GF.DictFormatter(dict(zip(tlocs, map(str,rlocs))))

    if kw.has_key("tloc2"):
        gl2=GF.FixedLocator(kw["tloc2"])   
    else:
        gl2=GF.MaxNLocator(10)

    if kw.has_key("th1"):
        th1=kw["th1"]
    else:
        th1=0.

    if kw.has_key("th2"):
        th2=kw["th2"]
    else:
        th2=np.pi/2

    if kw.has_key("rd1"):
        rd1=kw["rd1"]
    else:
        rd1=0.

    if kw.has_key("rd2"):
        rd2=kw["rd2"]
    else:
        rd2=1.65
        
        
    ghelper = FA.GridHelperCurveLinear(tr,
                                       extremes=(th1, th2, rd1, rd2),
                                       grid_locator1=gl1,
                                       grid_locator2=gl2,
                                       tick_formatter1=tf1,
                                       tick_formatter2=None,)

    ax = FA.FloatingSubplot(fig, *args, grid_helper=ghelper)
    fig.add_subplot(ax)
    # Adjust axes
    fontsize=9
    ax.axis["top"].set_axis_direction("bottom")  # "Angle axis"
    ax.axis["top"].toggle(ticklabels=True, label=True)
    ax.axis["top"].major_ticklabels.set_size('xx-small')
    ax.axis["top"].major_ticklabels.set_axis_direction("top")
    ax.axis["top"].label.set_axis_direction("top")
    ax.axis["top"].label.set_text("Correlation")
    ax.axis["top"].label.set_fontsize(fontsize)
    ax.axis["left"].set_axis_direction("right") # "X axis"
    ticks_font=2
    ax.axis["left"].major_ticklabels.set_size('xx-small')
    ax.axis["left"].major_ticks.set_ticksize(ticks_font) # "X axis"
    ax.axis["left"].label.set_text("Normalized standard deviation")
    ax.axis["left"].label.set_fontsize(fontsize)
    ax.axis["right"].major_ticklabels.set_size('xx-small')
    ax.axis["right"].set_axis_direction("top")   # "Y axis"
    ax.axis["right"].toggle(ticklabels=True)
    ax.axis["right"].major_ticks.set_ticksize(ticks_font) # "Y axis"
    ax.axis["right"].major_ticklabels.set_axis_direction("left")
    ax.axis["right"].label.set_fontsize(fontsize)
    ax.axis["bottom"].set_visible(False)         # turn off overlaying tickmark

    ax.grid(linewidth=0.5,color='gray')
    aux_ax = ax.get_aux_axes(tr)   # Polar coordinates
    aux_ax.th1 = th1
    aux_ax.th2 = th2
    aux_ax.rd1 = rd1
    aux_ax.rd2 = rd2
    ax.th1 = th1
    ax.th2 = th2
    ax.rd1 = rd1
    ax.rd2 = rd2
    return ax,aux_ax
    

def add_contour(aux_ax, *args, **kw):
    """Add constant centered RMS difference contours."""

    rs,ts = np.meshgrid(np.linspace(aux_ax.rd1, aux_ax.rd2, 200),
                            np.linspace(aux_ax.th1, aux_ax.th2, 200))
    # Compute centered RMS difference
    rms = np.sqrt(1.**2 + rs**2 - 2*1.*rs*np.cos(ts))
    contours = aux_ax.contour(ts, rs, rms, *args, **kw)
    return contours

def add_ref_contour(aux_ax, *args, **kw):
    refstd=1.
    t = np.linspace(0, aux_ax.th2)
    r = np.zeros_like(t) + refstd
    line=aux_ax.plot(t, r, *args,  **kw)
    return line


def add_sample(aux_ax, corrcoef, std, samples, *args, **kwargs):
    """Add sample (stddev,corrcoeff) to the Taylor diagram. args
    and kwargs are directly propagated to the Figure.plot
    command."""

    l, = aux_ax.plot(np.arccos(corrcoef), std,
                          *args, **kwargs) # (theta,radius)
    samples.append(l)

    return l

