### Plotting script for Diamond data, February 2024

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib_scalebar.scalebar import ScaleBar

from plotting_script_v0 import *



# def plot_maps_thiol(filepath_pre, filepath_post):
    


def plot_spectra_thiol(filepath_pre, filepath_post, filepath_bkgd):
    CDpre, CBpre, LDpre, LDppre, LBpre, LBppre, gfacpre, absorbpre = read_plot_spectra(filepath_pre)
    CDpost, CBpost, LDpost, LDppost, LBpost, LBppost, gfacpost, absorbpost = read_plot_spectra(filepath_post)
    CDbkgd, CBbkgd, LDbkgd, LDpbkgd, LBbkgd, LBpbkgd, gfacbkgd, absorbbkgd = read_plot_spectra(filepath_bkgd)
    
    
    # Plotting circular effects
    fig,axs = plt.subplots(ncols=1, nrows=3, figsize=(3,7), sharex=True)
    for ax in axs.flat:
        ax.tick_params(axis='both', direction='in')
    
    for i in range(len(CDpre.columns) - 2):
        axs[0].plot(CDpre[0], CDpre[i+1], color='k')
        axs[1].plot(gfacpre[0], gfacpre[i+1], color='k')
        axs[2].plot(CBpre[0], CBpre[i+1], color='k')
        
        axs[0].plot(CDpost[0], CDpost[i+1], color='darkorange')
        axs[1].plot(gfacpost[0], gfacpost[i+1], color='darkorange')
        axs[2].plot(CBpost[0], CBpost[i+1], color='darkorange')
        
    axt = axs[0].twinx()
    axt.plot(absorbpre[0], absorbpre[1] - absorbbkgd[1].iloc[:181], color='k', ls='--') # NEED TO ADD BKGD SUBTRACTION HERE
    axt.plot(absorbpost[0], absorbpost[1]- absorbbkgd[1].iloc[:181], color='darkorange', ls='--') # NEED TO ADD BKGD SUBTRACTION HERE

    axt.set_ylim(0,5)
    axt.set_yticks([], labels=[])
    axt.set_ylabel('')
    
    axs[0].set_ylabel('CD (mdeg)')
    axs[1].set_ylabel('g-factor')
    axs[2].set_ylabel('CB (mdeg)')
    
    axs[2].set_xlim(220, 400)
    axs[2].set_xticks([250, 300, 350, 400])
    axs[2].set_xlabel('Wavelength (nm)')

    plt.suptitle('Circular Effects')
    plt.show()
    
    # Plotting linear effects
    fig,axs = plt.subplots(ncols=2, nrows=2, figsize=(7,5), sharex=True)
    for ax in axs.flat:
        ax.tick_params(axis='both', direction='in')
    
    for i in range(len(CDpre.columns) - 2):
        axs[0,0].plot(LDpre[0], LDpre[i+1], color='k')
        axs[1,0].plot(LDppre[0], LDppre[i+1], color='k')
        axs[0,1].plot(LBpre[0], LBpre[i+1], color='k')
        axs[1,1].plot(LBppre[0], LBppre[i+1], color='k')
        
        axs[0,0].plot(LDpost[0], LDpost[i+1], color='darkorange')
        axs[1,0].plot(LDppost[0], LDppost[i+1], color='darkorange')
        axs[0,1].plot(LBpost[0], LBpost[i+1], color='darkorange')
        axs[1,1].plot(LBppost[0], LBppost[i+1], color='darkorange')
        
    # axt = axs[0].twinx()
    # axt.plot(absorbpre[0], absorbpre[1] - absorbbkgd[1].iloc[:181], color='k', ls='--') # NEED TO ADD BKGD SUBTRACTION HERE
    # axt.plot(absorbpost[0], absorbpost[1]- absorbbkgd[1].iloc[:181], color='darkorange', ls='--') # NEED TO ADD BKGD SUBTRACTION HERE
    # axt.set_ylim(0,5)
    # axt.set_yticks([], labels=[])
    # axt.set_ylabel('')
    
    axs[0,0].set_ylabel('LD')
    axs[1,0].set_ylabel('LD`')
    axs[0,1].set_ylabel('LB')
    axs[1,1].set_ylabel('LB`')
    
    axs[1,1].set_xlim(220, 400)
    axs[1,1].set_xticks([250, 300, 350, 400])
    axs[1,0].set_xlabel('Wavelength (nm)')
    axs[1,1].set_xlabel('Wavelength (nm)')

    plt.suptitle('Linear Effects')
    plt.show()
    
    # Plotting LDLB overlay
    fig,axs = plt.subplots(ncols=2, nrows=1, figsize=(7,3), sharex=True)
    for ax in axs.flat:
        ax.tick_params(axis='both', direction='in')
    
    for i in range(len(CDpre.columns) - 2):
        axs[0].plot(LBpre[0], LBpre[i+1]*LDppre[i+1], color='k')
        axs[0].plot(LBpost[0], LBpost[i+1]*LDppost[i+1], color='darkorange')
        axs[1].plot(LDpre[0], LDpre[i+1]*LBppre[i+1], color='k')
        axs[1].plot(LDpost[0], LDpost[i+1]*LBppost[i+1], color='darkorange')
    
    axs[0].set_ylabel('LBLD`')
    axs[1].set_ylabel('LDLB`')
    
    axs[1].set_xlim(220, 400)
    axs[1].set_xticks([250, 300, 350, 400])
    axs[0].set_xlabel('Wavelength (nm)')
    axs[1].set_xlabel('Wavelength (nm)')

    plt.suptitle('LDLB Effects')
    plt.show()
    
    
    # Plotting LDLB overlay v2
    fig,axs = plt.subplots(ncols=2, nrows=1, figsize=(7,3), sharex=True)
    for ax in axs.flat:
        ax.tick_params(axis='both', direction='in')
    
    for i in range(len(CDpre.columns) - 2):
        axs[0].plot(LBpre[0], (LBpre[i+1] + LBpost[i+1])/2*(LDppre[i+1] + LDppost[i+1])/2, color='red')
        axs[1].plot(LDpre[0], (LDpre[i+1]+LDpost[i+1])/2*(LBppre[i+1]+LBppost[i+1])/2, color='red')
    
    axs[0].set_ylabel('LBLD`')
    axs[1].set_ylabel('LDLB`')
    
    axs[1].set_xlim(220, 400)
    axs[1].set_xticks([250, 300, 350, 400])
    axs[0].set_xlabel('Wavelength (nm)')
    axs[1].set_xlabel('Wavelength (nm)')

    plt.suptitle('LDLB Effects')
    plt.show()
    



DE_1x5_LH_prethiol = r"processing\quick_and_goodscans_DE_prethiol\DE_LH_1x5_highgspectra_Mueller_2024_02_09_08_50_17_v1.xlsx"
DE_1x5_LH_postthiol = r"processing\goodscans_DE_midthiol\DE_LH_1x5_highgspectra_Mueller_2024_02_09_18_50_07_v1.xlsx"

DE_1x5_RH_prethiol = r"processing\quick_and_goodscans_DE_prethiol\DE_RH_1x5_highgspectra_Mueller_2024_02_09_07_53_12_v1.xlsx"
DE_1x5_RH_postthiol = "processing\goodscans_DE_midthiol\DE_RH_1x5_highgspectra_Mueller_2024_02_09_17_55_38_v1.xlsx"

bkgd_new = r"processing\blank_substrate_spectra_200_400nm\blank_substrate_new_Mueller_2024_02_12_08_19_25_v1.xlsx"
bkgd_old = r"processing\blank_substrate_spectra_200_400nm\blank_substrate_old_Mueller_2024_02_12_08_35_25_v1.xlsx"

plot_spectra_thiol(DE_1x5_LH_prethiol, DE_1x5_LH_postthiol, bkgd_old)
plot_spectra_thiol(DE_1x5_RH_prethiol, DE_1x5_RH_postthiol, bkgd_old)


















