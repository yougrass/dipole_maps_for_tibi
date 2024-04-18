### Plotting script for Diamond data, February 2024

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib_scalebar.scalebar import ScaleBar


filepath1 = r"processing\D2_postthiol_goodscans\D2new_2mmdense_2D matrix_from map_361nm_Mueller_2024_02_11_21_51_15_v1.xlsx"
filepath2 = r"processing\D2_postthiol_goodscans\D2new_2x2specLH_postthiol_Mueller_2024_02_11_20_56_17_v1.xlsx"

filepath_ordered = "processing\goodscans_DE_midthiol\DEmidthiol4mmdense_329nm_2D matrix_from map_361nm_Mueller_2024_02_10_00_07_25_v1.xlsx"

# test = pd.read_excel(filepath2, sheet_name='aCD (mdeg)', header=0, index_col=0)
# print(test)
# plt.plot(test[0], test[1])
# plt.plot(test[0], test[2])
# plt.plot(test[0], test[3])
# plt.plot(test[0], test[4])
# plt.plot(test[0], test[5])

# plt.imshow(test, origin='lower',cmap='seismic')

def compute_plot_dipoles(LD, LDp, subsample=True, subsample_factor=4): 
    LD = LD.to_numpy()
    LDp = LDp.to_numpy()
    dipoles = -1*LD + 1j * LDp # I don't know why the egative sign in front of LD worked. The sign of the dipole maps was wrong until I added that...
    magnitude = np.abs(dipoles)
    orientation = np.angle(dipoles)
    # orientation = np.arctan2(LD,LDp)
    angle = np.arctan2(LD, LDp)
    angle_correction = np.degrees(np.arctan2(np.sin(angle), np.cos(angle)))
    
    x = np.linspace(0, len(LD)-1, dipoles.shape[1])
    y = np.linspace(0, len(LD)-1, dipoles.shape[0])
    X, Y = np.meshgrid(x, y)   
               
    LDmax = np.max(np.abs(LD.flatten()))
    LDpmax = np.max(np.abs(LDp.flatten()))
    
    fig,axs = plt.subplots(ncols=1, nrows=3, figsize=(3,7))
    for ax in axs.flat:
        ax.set(xticks=[],yticks=[])
        ax.tick_params(axis='both', direction='in', top=True, right=True)
        scalebar = ScaleBar(5e-5, length_fraction=0.15, box_alpha=0, 
                            location='upper left', label_formatter = lambda x,y:'', 
                            pad=0.5, sep=0)
    
    LDplot=axs[0].imshow(LD, origin='lower', cmap='PiYG', vmin=-1*LDmax, vmax=LDmax)
    divider = make_axes_locatable(axs[0])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(LDplot, cax=cax)
    cax.set_title('LD')
    
    LDpplot=axs[1].imshow(LDp, origin='lower', cmap='PiYG', vmin=-1*LDpmax, vmax=LDpmax)
    divider = make_axes_locatable(axs[1])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(LDpplot, cax=cax)
    cax.set_title('LD`')
    
    dip = axs[2].imshow(0.5*np.angle(dipoles), origin='lower', cmap='PiYG', alpha=1)
    
    if subsample == True:
        X = X[::subsample_factor, ::subsample_factor]
        Y = Y[::subsample_factor, ::subsample_factor]
        LD = LD[::subsample_factor, ::subsample_factor]
        LDp = LDp[::subsample_factor, ::subsample_factor]
        orientation = orientation[::subsample_factor, ::subsample_factor]
        magnitude = np.abs(dipoles[::subsample_factor, ::subsample_factor])
        angle_correction = np.degrees(np.arctan2(np.sin(orientation), np.cos(orientation)))
    
    axs[2].quiver(
        X, Y, -1*(magnitude * np.cos(np.radians(0.5 * angle_correction))),
        magnitude * np.sin(np.radians(0.5 * angle_correction)),
        angles='xy', scale_units='xy', scale=5e3, cmap='hsv', pivot='middle', headaxislength=4, headlength=5, headwidth=3.5)
    axs[2].quiver(
        X, Y, 1*(magnitude * np.cos(np.radians(0.5 * angle_correction))),
        -1*(magnitude * np.sin(np.radians(0.5 * angle_correction))),
        angles='xy', scale_units='xy', scale=5e3, cmap='hsv', pivot='middle', headaxislength=4, headlength=5, headwidth=3.5)

    plt.suptitle('Linear Effects')
    plt.show()
    
    return magnitude, angle

def read_plot_maps(filepath):
    aCD = pd.read_excel(filepath, sheet_name='aCD (mdeg)', header=0, index_col=0)
    CDmax = np.max(np.abs(aCD.to_numpy().flatten()))
    aCB = pd.read_excel(filepath, sheet_name='aCB (mdeg)', header=0, index_col=0)
    CBmax = np.max(np.abs(aCB.to_numpy().flatten()))
    aLD = pd.read_excel(filepath, sheet_name='aLD (mdeg)', header=0, index_col=0)
    LDmax = np.max(np.abs(aLD.to_numpy().flatten()))
    aLDp = pd.read_excel(filepath, sheet_name='aLDp (mdeg)', header=0, index_col=0)
    LDpmax = np.max(np.abs(aLDp.to_numpy().flatten()))
    aLB = pd.read_excel(filepath, sheet_name='aLD (mdeg)', header=0, index_col=0)
    LBmax = np.max(np.abs(aLB.to_numpy().flatten()))
    aLBp = pd.read_excel(filepath, sheet_name='aLBp (mdeg)', header=0, index_col=0)
    LBpmax = np.max(np.abs(aLBp.to_numpy().flatten()))
    agfac = pd.read_excel(filepath, sheet_name='aG-factor', header=0, index_col=0)
    gmax = np.max(np.abs(agfac.to_numpy().flatten()))
    absorb = pd.read_excel(filepath, sheet_name='Abs (au) (from M00)', header=0, index_col=0)
    
    # First, plotting circular effects
    fig,axs = plt.subplots(ncols=1, nrows=3, figsize=(3,7))
    for ax in axs.flat:
        ax.set(xticks=[],yticks=[])
        ax.tick_params(axis='both', direction='in', top=True, right=True)
        scalebar = ScaleBar(5e-5, length_fraction=0.15, box_alpha=0, 
                            location='upper left', label_formatter = lambda x,y:'', 
                            pad=0.5, sep=0)
    
    CD=axs[0].imshow(aCD, origin='lower', cmap='seismic', vmin=-1*CDmax, vmax=CDmax)
    divider = make_axes_locatable(axs[0])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(CD, cax=cax)
    cax.set_title('CD')
    
    G=axs[1].imshow(agfac, origin='lower', cmap='seismic', vmin=-1*gmax, vmax=gmax)
    divider = make_axes_locatable(axs[1])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(G, cax=cax)
    cax.set_title('g-factor')
    
    CB=axs[2].imshow(aCB, origin='lower', cmap='seismic', vmin=-1*CBmax, vmax=CBmax)
    divider = make_axes_locatable(axs[2])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(CB, cax=cax)
    cax.set_title('CB')
    
    plt.suptitle('Circular Effects')
    plt.show()
    
    return aCD, aCB, aLD, aLDp, aLB, aLBp, agfac, absorb

def read_plot_spectra(filepath):
    aCD = pd.read_excel(filepath, sheet_name='aCD (mdeg)', header=0, index_col=0)
    aCB = pd.read_excel(filepath, sheet_name='aCB (mdeg)', header=0, index_col=0)
    aLD = pd.read_excel(filepath, sheet_name='aLD (mdeg)', header=0, index_col=0)
    aLDp = pd.read_excel(filepath, sheet_name='aLDp (mdeg)', header=0, index_col=0)
    aLB = pd.read_excel(filepath, sheet_name='aLB (mdeg)', header=0, index_col=0)
    aLBp = pd.read_excel(filepath, sheet_name='aLBp (mdeg)', header=0, index_col=0)
    agfac = pd.read_excel(filepath, sheet_name='aG-factor', header=0, index_col=0)
    absorb = pd.read_excel(filepath, sheet_name='Abs (au) (from M00)', header=0, index_col=0)
    
    # # Plotting circular effects
    # fig,axs = plt.subplots(ncols=1, nrows=3, figsize=(3,7))
    # for ax in axs.flat:
    #     ax.tick_params(axis='both', direction='in', top=True, right=True)
    
    # for i in range(len(aCD.columns) - 2):
    #     axs[0].plot(aCD[0], aCD[i+1])
    #     axs[1].plot(agfac[0], agfac[i+1])
    #     axs[2].plot(aCB[0], aCB[i+1])
        
    # axs[0].set_ylabel('CD')
    # axs[1].set_ylabel('g-factor')
    # axs[2].set_ylabel('CB')

    # plt.suptitle('Circular Effects')
    # plt.show()
    
    return aCD, aCB, aLD, aLDp, aLB, aLBp, agfac, absorb






aCD, aCB, aLD, aLDp, aLB, aLBp, agfac, absorb = read_plot_maps(filepath_ordered)
compute_plot_dipoles(aLD, aLDp)
compute_plot_dipoles(aLB, aLBp)
# read_plot_spectra(filepath2)


















