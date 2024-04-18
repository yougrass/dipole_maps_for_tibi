import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plotting_script_v0 import *

filepath_DE_LH = r"processing\quick_and_goodscans_DE_prethiol\DE_LH_1x5_highgspectra_Mueller_2024_02_09_08_50_17_v1.xlsx"
filepath_bkgd_old = r"processing\blank_substrate_spectra_200_400nm\blank_substrate_old_Mueller_2024_02_12_08_35_25_v1.xlsx"


CD, CB, LD, LDp, LB, LBp, gfac, absorb = read_plot_spectra(filepath_DE_LH)
CDb, CBb, LDb, LDpb, LBb, LBpb, gfacb, absorbb = read_plot_spectra(filepath_bkgd_old)

# Plotting CD, g-factor
fig,axs = plt.subplots(ncols=1, nrows=2, figsize=(3,5), sharex=True)
for ax in axs.flat:
    ax.tick_params(axis='both', direction='in')

for i in range(len(CD.columns) - 2):
    axs[0].plot(CD[0], CD[i+1], color='k')
    axs[1].plot(gfac[0], gfac[i+1], color='k')
    
# axt = axs[0].twinx()
# axt.plot(absorb[0], absorb[1] - absorbbkgd[1].iloc[:181], color='k', ls='--') # NEED TO ADD BKGD SUBTRACTION HERE
# axt.plot(absorbpost[0], absorbpost[1]- absorbbkgd[1].iloc[:181], color='darkorange', ls='--') # NEED TO ADD BKGD SUBTRACTION HERE

# axt.set_ylim(0,5)
# axt.set_yticks([], labels=[])
# axt.set_ylabel('')

axs[0].set_ylabel('CD (mdeg)')
axs[1].set_ylabel('g-factor')

axs[1].set_xlim(220, 400)
axs[1].set_xticks([250, 300, 350, 400])
axs[1].set_xlabel('Wavelength (nm)')
plt.show()


# Here, plotting CD, g-factor, and absorbance
fig,ax = plt.subplots(figsize=(5.5,4))

color1 = 'limegreen'
pl1 = ax.plot(CD[0], CD[1] / 1000, color=color1, label='CD')
ax.tick_params(axis='both', direction='in')
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('CD (degrees)')

color2 = 'magenta'
ax2 = ax.twinx()
pl2 = ax2.plot(gfac[0], gfac[1], color=color2, ls='--', label='g-factor')
ax2.tick_params(axis='both', direction='in')
ax2.set_ylabel ('g-factor')
ax2.set_yticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5], labels=['-1', '', '-0.5', '', '0', '', '0.5'])


ax3 = ax.twinx()
pl3 = ax3.plot(absorb[0], absorb[1] - absorbb[1].iloc[:181], ls='--', color='k', label='Abs')
ax3.set_ylim(0,7)
ax3.set_yticks([], labels=[])
ax3.set_ylabel('')

ax3.set_xlabel('Wavelength')
ax3.set_xticks([225, 250, 275,300,325,350,375,400], labels=['','250','','300','','350','','400'])
ax3.set_xlim(220,400)

# Making combined label
lns = pl1 + pl2 + pl3
# lns = pl1 + pl2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0, frameon=False)

plt.tight_layout()    
plt.savefig('high_g_posterplot_v1.png', dpi=600, bbox_inches = "tight")