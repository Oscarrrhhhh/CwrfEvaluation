#!/usr/bin/env python
import numpy as np
from  netCDF4 import Dataset,date2num,num2date 
import glob
import numpy.ma as ma
from datetime import datetime
from collections import OrderedDict

'''
Imporvements:
1. calculate the obs variables directly from the raw data
2. add the spacial pattern of taylor diagram
3. provide an alternative to deal with different subregions (m1: mask array; m2: np.where)

Seies difference between Spacial & Temporal
Spacial pattern (t,y,x)=>t; Temporal pattern (t,y,x)=>(y,x)
'''

#VAR="AT2M"
VAR="PRAVG" 
#Pattern="Spatial"
Pattern="Temporal"
#SEASON="MAM";b_yyyymmdd=20010301;e_yyyymmdd=20010531
#SEASON="JJA";b_yyyymmdd=20010601;e_yyyymmdd=20010831
SEASON="SON";b_yyyymmdd=20010901;e_yyyymmdd=20011130
#b_yyyymmdd=20010301;e_yyyymmdd=20011130
#===============marker dict setting==========================================
case_cate_num=(7,6,7,5,1,2)
colors=('green', 'magenta', 'blue', 'purple', 'yellow', 'red')
marks=('o','o','s','s','*','*','^','^','D','D')
fillstyles=('full','none','full','none','full','none','full','none','full','none')

#=====================================================================
sub_regions=["XinJiang","Northwest","Sichuan","Southwest","Northeast", \
          "North","Yangtze","Southeast","EastTibet","WestTibet"]
case_dir='/home/export/online1/sunlei/scripts/python/taylor/case_comparison/cwrf_case_filter/'
obs_daily_dir='/home/export/online1/CWRF_DATA/SBCs/OBS_data/Version3/'

def cal_td():

    b_year=int(str(b_yyyymmdd)[0:4])
    b_mon=int(str(b_yyyymmdd)[4:6])
    b_day=int(str(b_yyyymmdd)[6:8])
    e_year=int(str(e_yyyymmdd)[0:4])
    e_mon=int(str(e_yyyymmdd)[4:6])
    e_day=int(str(e_yyyymmdd)[6:8])

    mask_value=range(1,11,1)

    caselist = sorted(glob.glob(case_dir +VAR+"*.nc"))
    fmask=Dataset(obs_daily_dir+'CN_subregion_mask.nc','r')
    reg_mask=np.array(fmask.variables["reg_mask"][:])

    f_obs=Dataset(glob.glob(obs_daily_dir + "CN_OBS_"+VAR+"*daily.nc")[0])
    obs_time=f_obs.variables["time"]
    time_unit=obs_time.__getattr__('units')
    time_calendar=obs_time.__getattr__('calendar')
    
    b_gre=int(date2num(datetime(b_year,b_mon,b_day),time_unit,time_calendar))
    e_gre=int(date2num(datetime(e_year,e_mon,e_day),time_unit,time_calendar))
    obs_b_i=int(np.argwhere(np.array(obs_time)==b_gre))
    obs_e_i=int(np.argwhere(np.array(obs_time)==e_gre)+1)
    
    var_samples=OrderedDict() # {casename:([ratio_reg1,...ratio_reg10],cc_reg1,cc_reg_2,...cc_reg10])} 
    varnames=["PRAVG","AT2M"]
    
    if Pattern=="Spatial":
        print "Taylor diagram pattern:",Pattern
        obs_var=np.mean(f_obs.variables[VAR][obs_b_i:obs_e_i,:,:],axis=0)
        obs_use=OrderedDict() #{region1:[v1,v2,...vn],region2:[v1,v2,...vn]}

        for i,mv in enumerate(mask_value):
            obs_use[sub_regions[i]]=[]
            ind_y,ind_x=np.where(reg_mask==mv)
            obs_use[sub_regions[i]]=obs_var[ind_y,ind_x]
    
        obs_std=[]
        for key in obs_use:
            obs_std.append(np.std(obs_use[key]))


        for i,fname in enumerate(caselist):
            var_name=fname.split("/")[-1].split("_")[0]
            case_name=fname.split("/")[-1].split("_")[-1].split(".")[0]
            if (var_name in varnames):
                print "it is processing files====>"+fname.split("/")[-1]
                var_samples[case_name]=[],[]
                i_data=np.array(Dataset(fname,"r").variables[var_name])
                if var_name == "PRAVG":
                    i_data=i_data*86400
                i_time=np.array(list(Dataset(fname,"r").variables['time']),dtype='int32')
                case_b_i=int(np.argwhere(i_time==b_gre))
                case_e_i=int(np.argwhere(i_time==e_gre)+1)
                i_data_use=np.mean(i_data[case_b_i:case_e_i,:,:],axis=0)
                for j,mv in enumerate(mask_value):
                    ind_y,ind_x=np.where(reg_mask==mv)
                    i_data_reg=i_data_use[ind_y,ind_x]
                    reg_std=np.std(i_data_reg)
                    var_samples[case_name][0].append(reg_std/obs_std[j])
                    var_samples[case_name][1].append(np.corrcoef(i_data_reg,obs_use[sub_regions[j]])[0,1])




    if Pattern=="Temporal":
        print "Taylor diagram pattern:",Pattern
        obs_var=np.array(f_obs.variables[VAR][obs_b_i:obs_e_i,:,:])

        obs_use=[]
        for i,mv in enumerate(mask_value):
            ind_y,ind_x=np.where(reg_mask==mv)
            obs_use.append(np.mean(obs_var[:,ind_y,ind_x],axis=1))
   
        obs_use=np.array(obs_use)
        obs_std=np.std(obs_use,axis=1,dtype=np.float64)
    

        for i,fname in enumerate(caselist):
            var_name=fname.split("/")[-1].split("_")[0]
            case_name=fname.split("/")[-1].split("_")[-1].split(".")[0]
            if (var_name in varnames):
                print "it is processing files====>"+fname.split("/")[-1]
                var_samples[case_name]=[],[]
                i_data=np.array(Dataset(fname,"r").variables[var_name])
                if var_name == "PRAVG":
                    i_data=i_data*86400
                i_time=np.array(list(Dataset(fname,"r").variables['time']),dtype='int32')
                case_b_i=int(np.argwhere(i_time==b_gre))
                case_e_i=int(np.argwhere(i_time==e_gre)+1)
                i_data_use=i_data[case_b_i:case_e_i,:,:]
                for j,mv in enumerate(mask_value):
                    #v1: create 3d mask array through broadcast
                    #mask_2D=(reg_mask!=mv) 
                    #mask_3D=np.broadcast_arrays(i_data_use,mask_2D)[1]
                    #mask_data=ma.masked_array(i_data_use, mask=mask_3D)
                    #reg_mean=np.mean(np.mean(mask_data,axis=1),axis=1)
                    #v2: directly use the np.where to pick up the right coordinates
                    ind_y,ind_x=np.where(reg_mask==mv)
                    reg_mean=np.mean(i_data_use[:,ind_y,ind_x],axis=1)
                    reg_std=np.std(reg_mean)
                    var_samples[case_name][0].append(reg_std/obs_std[j])
                    var_samples[case_name][1].append(np.corrcoef(reg_mean,obs_use[j,:])[0,1])
        
    return var_samples


def set_ms_list(case_cate_num, colors, marks, fillstyles):
    ms_list=[]
    k=0
    for i,num1 in enumerate(case_cate_num):
        color=colors[i]
        for j in range(0,num1):
            if fillstyles[j]=='none':
                ms_list.append(dict(mec=color, mew=1., marker=marks[j], fillstyle='none'))
            else:
                ms_list.append(dict(mfc=color, mec=color, marker=marks[j], fillstyle='full'))
            k=k+1
    return ms_list


def dict_transform(key_names, i_dict):
    o_dict=OrderedDict()
    for keyname in key_names:
        o_dict[keyname]=[]
    for key in i_dict:
        list1,list2=i_dict[key]
        for i,(var1,var2) in enumerate(zip(list1,list2)):
            o_dict[key_names[i]].append([key, var1, var2])
    return o_dict
