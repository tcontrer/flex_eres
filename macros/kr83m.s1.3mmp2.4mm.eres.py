import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import AutoMinorLocator
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import norm
from fit_functions import fit_energy, plot_fit_energy, print_fit_energy, get_fit_params
from ic_functions import *
from invisible_cities.core.core_functions  import shift_to_bin_centers
import invisible_cities.database.load_db as db
import json
import glob
 
SiPMsize     = 1.3
SiPMpitch    = 2.4
mc_name      = 's1.3mmp2.4mm'
teflon       = False
event_type   = 'kr83m'
rcut         = 300
zcut         = 1200
sipm_thresh  = 2
outdir       = '/n/home12/tcontreras/plots/FlexEresStudies/kr83m/'
if teflon:
    mc_teflon = 'teflon'
    mc_file_name = mc_name[0:-7]
else:
    mc_teflon = 'no_teflon'
    mc_file_name = mc_name
 
num_sipms = 129889
num_files = 100

def Center_of_Event(sipmtable_df, sipm_thresh=0):
    event_id = sipmtable_df.event_id.values[0]
    sipmtable_df = sipmtable_df[sipmtable_df.charge > sipm_thresh]
    x = np.sum(sipmtable_df.charge*sipmtable_df.X)/np.sum(sipmtable_df.charge)
    y = np.sum(sipmtable_df.charge*sipmtable_df.Y)/np.sum(sipmtable_df.charge)
    z = np.sum(sipmtable_df.charge*sipmtable_df.Z)/np.sum(sipmtable_df.charge)
    charge = np.sum(sipmtable_df.charge)
    r = np.sqrt(x**2 + y**2)
    return pd.Series({'event_id':event_id, 'charge':charge, 'X':x, 'Y':y, 'Z':z, 'r':r})
 
active_diam = 984.
tp_area = np.pi * (active_diam/2.)**2  # mm^2
coverage = 100 * num_sipms * SiPMsize**2 / tp_area
data_dir = '/n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/full_sims/'+mc_name+'/'+event_type+'/buffy/reduced_hdf5/'
fast_sims = glob.glob(data_dir+'/*')
num_files  = len(fast_sims)

fast_data = pd.DataFrame()
mc = {'size':SiPMsize, 'pitch':SiPMpitch,
      'teflon':mc_teflon, 'name': f'{SiPMsize} mm size, {SiPMpitch} pitch, {mc_teflon}',
      'num_sipms': num_sipms, 'coverage': coverage, 'rcut':rcut, 'sthresh':sipm_thresh}
for j in range(0, num_files): 
    this_data = pd.read_hdf(fast_sims[j], 'SiPM/Waveforms')
    event_centers = this_data.groupby('event_id').apply(lambda grp: Center_of_Event(grp, sipm_thresh))
    event_centers = event_centers[event_centers.r < rcut]
    event_centers = event_centers[event_centers.Z < zcut]
    fast_data = fast_data.append(event_centers)

#####################
##### Eres Plot #####
#####################

bins_fit = 50
if event_type == 'kr83m':
    fit_range_sipms = (np.min(fast_data.charge), np.max(fast_data.charge))
else:
    y, b = np.histogram(fast_data.charge, bins= bins_fit, range=[np.min(fast_data.charge), np.max(fast_data.charge)])
    x = shift_to_bin_centers(b)
    peak = x[np.argmax(y)]
    fit_range_sipms = (peak - np.std(fast_data.charge)*3, peak + np.std(fast_data.charge)*3)

sipm_fit = fit_energy(fast_data.charge, bins_fit, fit_range_sipms)
mc['sipm_eres'], mc['sipm_fwhm'], mc['sipm_mean'], mc['sipm_eres_err'], mc['sipm_fwhm_err'], mc['sipm_mean_err'], mc['sipm_chi2'] = get_fit_params(sipm_fit)
print(mc['name']+'-------------------')
print('Coverage = '+str(mc['coverage']))
print('Mean and std', np.mean(event_centers.charge), np.std(event_centers.charge))
print('Eres err', mc['sipm_eres_err'])
print_fit_energy(sipm_fit)
plot_fit_energy(sipm_fit)
plt.xlabel('Charge [pes]')
plt.title('Energy Resolution Fit, '+mc['name'])
plt.savefig(outdir+f'eres_r{rcut}_sthresh{sipm_thresh}_'+mc_name+'.png')
plt.close()

plt.hist(fast_data.charge, bins=50, label=f'R < 300, SiPM Charge > 2')
plt.title(mc['name']+', '+event_type)
plt.xlabel('Total SiPM Charge [pes]')
plt.savefig(outdir+f'charge_r{rcut}_sthresh{sipm_thresh}_'+mc_name+'.png')
plt.close()

plt.hist(fast_data.X, bins=50, label=f'R < 300, SiPM Charge > 2')
plt.title(mc['name']+', '+event_type)
plt.xlabel('X [mm]')
plt.savefig(outdir+f'x_r{rcut}_sthresh{sipm_thresh}_'+mc_name+'.png')
plt.close() 

plt.hist(fast_data.Y, bins=50, label=f'R < 300, SiPM Charge > 2')
plt.title(mc['name']+', '+event_type)
plt.xlabel('Y [mm]')
plt.savefig(outdir+f'y_r{rcut}_sthresh{sipm_thresh}_'+mc_name+'.png')
plt.close()

plt.hist(fast_data.r, bins=50, label=f'R < 300, SiPM Charge > 2')
plt.title(mc['name']+', '+event_type)
plt.xlabel('R [mm]')
plt.savefig(outdir+f'r_r{rcut}_sthresh{sipm_thresh}_'+mc_name+'.png')
plt.close()

plt.hist(fast_data.Z, bins=50, label=f'R < 300, SiPM Charge > 2')
plt.title(mc['name']+', '+event_type)
plt.xlabel('Z [mm]')
plt.savefig(outdir+f'z_r{rcut}_sthresh{sipm_thresh}_'+mc_name+'.png')
plt.close()

# Save eres numbers to a file

json.dump(mc, open('data_eres_kr83m_rcut300_sthresh2_zcut1200/'+mc_name+'.txt', 'w'))
