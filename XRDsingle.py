# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 21:00:03 2018

@author: garci
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from XRD_functions import *

'write the name of your csv file below:'
name = "MIL53-021ht.csv"

def data( filename = name ):
    
    
    '''if the csv file is in a subfolder to this script's, specify path'''
    fname_path='XRD_files/'
    
    with open(fname_path+filename, 'r') as f:
        X = list(csv.reader(f, delimiter=","))        
    Xc=np.array(X[1:], dtype=np.float)        

    return Xc, np.shape(Xc)


xi=data()[0][:,0]
yi=data()[0][:,1]
ybi=bacsub(xi,yi,tol=1)
plt.figure()
#plt.plot(xi,yi,color='darkorange',label='not treated')
plt.plot(xi,ybi,color='navy',label='subtracted background')

emission_lines_plt(xi, ybi,twothet_range_Ka=[9,10])
emission_lines_plt(xi, ybi,twothet_range_Ka=[10,17])
emission_lines_plt(xi, ybi,twothet_range_Ka=[17,18])
emission_lines_plt(xi, ybi,twothet_range_Ka=[20,30])



plt.title(name[:-4])
plt.xlabel(r'$2\theta$ / deg')
plt.ylabel('Intensity / a.u.')
plt.legend(loc='best')


import xlwings as xw

def excel(x,y):
    wb=xw.Book()
    xw.Range((1,1)).options(transpose=True).value=x
    xw.Range((1,2)).options(transpose=True).value=y

excel(xi,ybi)