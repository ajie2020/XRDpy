# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 15:06:48 2018

@author: garci
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize



'''Local maxima finder'''
def local_max(x,y,xrange=[12,13]):
    x1,x2=xrange
    xsearch_index=[]
    for n in x:
        if n >= x1 and  n <= x2:
            xsearch_index.append(list(x).index(n))

    max_y = 0
    max_x = 0
    for i in xsearch_index:
        if y[i] > max_y:
            max_y = y[i]
            max_x = x[i]

    return max_x, max_y

'''Emission lines arising from different types of radiation i.e. K_beta radiation
wavelength of K_beta == 0.139 nm'''
def emission_lines(x, y, twothet_range_Ka=[10,20], lmda_Ka = 0.154,lmda_Ki=0.139):

    twothet_Ka_deg, int_Ka = local_max(x,y,xrange=twothet_range_Ka)
    twothet_Ka=twothet_Ka_deg*np.pi/180

    twothet_Ki = 2*np.arcsin((lmda_Ki/lmda_Ka)*np.sin(twothet_Ka/2))
    twothet_Ki_deg = twothet_Ki*180/np.pi

    return twothet_Ka_deg, int_Ka, twothet_Ki_deg

def emission_lines_plt(x, y, twothet_range_Ka=[10,20], lmda_Ka = 0.154,lmda_Ki=0.139,plt='y'):

    twothet_Ka_deg, int_Ka, twothet_Ki_deg = emission_lines(x, y, twothet_range_Ka, lmda_Ka ,lmda_Ki)
##
    if plt == 'y':
        plt.vlines(twothet_Ka_deg,0,int_Ka, colors='k', linestyles='solid', \
                   label=r'K$\alpha$; $\theta$ = {} '.format(round(twothet_Ka_deg,2)))
        plt.vlines((twothet_Ka_deg+twothet_Ki_deg)/2,0,int_Ka, colors='k', linestyles='--', label='')
        plt.vlines(twothet_Ki_deg,0,int_Ka, colors='r', linestyles='solid',\
                   label=r'K$\beta$; $\theta$ = {} '.format(round(twothet_Ki_deg,2)))
    if plt=='n':

        return twothet_Ki_deg

'''interplanar spacing "d_hkl" from Braggs law'''
def braggs(twotheta,lmda=1.54):
    'lambda in Angstroms'
    twothet_rad=twotheta*np.pi/180
    
#    dhkl = lmda /(2*np.sin(twothet_rad/2))
    
    if twotheta.any() < 5:
        L =len(twotheta)
        dhkl = np.zeros(L)
        dhkl[0] = 'inf'
        
        k =1
        while k < L:
            dhkl[k] = lmda /(2*np.sin(twothet_rad[k]/2))
            k+=1
    else:
        dhkl = lmda /(2*np.sin(twothet_rad/2))
    
    dhkl = np.round(dhkl,2)
    return dhkl

def braggs_s(twotheta,lmda=1.54):
    'lambda in Angstroms'
    twothet_rad=twotheta*np.pi/180
    
    
    if twotheta < 5:
        dhkl = 'inf'
    else:
        dhkl = lmda /(2*np.sin(twothet_rad/2))
        dhkl = np.round(dhkl,2)
    

    return dhkl


'''Scherrer equation'''
def scherrer(K,lmda,beta,theta):

    print('Scherrer Width == K*lmda / (FWHM*cos(theta))')
    return K*lmda / (beta*np.cos(theta))    #tau

'''Gaussian fit for FWHM'''
def funcgauss(x,y0,a,mean,sigma):
    
    return y0+(a/(sigma*np.sqrt(2*np.pi)))*np.exp(-(x-mean)**2/(2*sigma*sigma))

#def funcgauss(x,y0,a,mean,fwhm):

#    return y0 + (a/(fwhm*np.sqrt(np.pi/(4*np.log(2)) )))*np.exp(-(4*np.log(2))*(x-mean)**2/(fwhm*fwhm))


def gaussfit(xdata,ydata):
    meanest = xdata[ydata.index(max(ydata))]
    sigest = meanest - min(xdata)
#    print('estimates',meanest,sigest)
    popt, pcov = optimize.curve_fit(funcgauss,xdata,ydata,p0 = [min(ydata),max(ydata),meanest,sigest])
    print('-Gaussian fit results-')
#    print('amplitude {}\nmean {}\nsigma {}'.format(*popt))
    print('y-shift {}\namplitude {}\nmean {}\nsigma {}'.format(*popt))

    print('covariance matrix \n{}'.format(pcov))
#    print('pcov',pcov)
    return popt
    
def schw_peakcal(x,y,K,lambdaKa,xrange=[12,13]):

    x1,x2=xrange
    'xseg and yseg:x and y segments of data in selected xrange'
    xseg,yseg = [],[]
    for n in x:
        if n >= x1 and  n <= x2:
            xseg.append(n)
            yseg.append(y[list(x).index(n)]) 
    
    
    y0,a,mean,sigma = gaussfit(xseg,yseg)
    ysegfit = funcgauss(np.array(xseg),y0,a,mean,sigma)
    
    'FULL WIDTH AT HALF MAXIMUM'
    FWHM_deg = sigma*2*np.sqrt(2*np.log(2))
    FWHM = FWHM_deg*np.pi/180
    print('\nFWHM == sigma*2*sqrt(2*ln(2)): {} degrees'.format(FWHM_deg))

    'scherrer width peak calculations'
    max_twotheta = xseg[list(yseg).index(max(yseg))]

    theta=max_twotheta/2
    theta=theta*np.pi/180

    print('K (shape factor): {}\nK-alpha: {} nm \nmax 2-theta: {} degrees'.\
          format(K,lambdaKa,max_twotheta))
    
    s=scherrer(K,lambdaKa,FWHM,theta)
    X,Y = xseg,ysegfit
    
    return s,X,Y

def schw_peakcal_old(x,y,xrange=[12,13]):
    x1,x2=xrange
    xsearch_index=[]
    for n in x:
        if n >= x1 and  n <= x2:
            xsearch_index.append(list(x).index(n))
    max_y = 0
    max_x = 0
    for i in xsearch_index:
        if y[i] > max_y:
            max_y = y[i]
            max_x = x[i]
#    'scherrer width peak calculations'
    max_twotheta,max_y = max_x,max_y
    hm = max_y/2
    theta=max_twotheta/2
    theta=theta*np.pi/180

    FWHM_range = []
    for i in xsearch_index:
        if y[i] > hm :
            FWHM_range.append(x[i])
    FWHM_range = [max(FWHM_range), min(FWHM_range)]
    FWHM = max(FWHM_range) - min(FWHM_range)
    FWHM = FWHM*np.pi/180
    s=scherrer(0.9,0.154,FWHM,theta)
    return s, np.linspace(min(FWHM_range),max(FWHM_range),10), hm*np.ones(10)

'''Background subtraction operation:'''
def backsub(xdata,ydata,tol=1):
    'approx. # points for half width of peaks'
    L=len(ydata)
    lmda = int(0.50*L/(xdata[0]-xdata[L-1]))

    newdat=np.zeros(L)
    for i in range(L):
        if ydata[(i+lmda)%L] > tol*ydata[i]:          #tolerance 'tol'
            newdat[(i+lmda)%L] = ydata[(i+lmda)%L] - ydata[i]
        else:
            if ydata[(i+lmda)%L] < ydata[i]:
                newdat[(i+lmda)%L] = 0

    return newdat


'''Function for an "n" point moving average: '''
def movnavg(xdata,ydata,n=1):

    L=int(len(xdata)//n)
    newy=np.zeros(L)
    for i in range(L):
        k=0
        while k < n:
           newy[i] += ydata[(i*n)+k]
           k += 1
#           print(i)
        newy[i]=newy[i]/n

    newx=np.zeros(L)
    for i in range(L):
        newx[i] = xdata[i*n]

    return newx,newy


'''Calculate relative peak intensity (i.e. comparing one peak to another)'''
def XRD_int_ratio(x,y,xR1=[8.88,9.6],xR2=[10.81,11.52]):
    'XRD b/t two intensities ratio'
    return local_max(x,y,xR2)[1]/local_max(x,y,xR1)[1]
