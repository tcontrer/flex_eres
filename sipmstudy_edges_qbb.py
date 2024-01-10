"""
Written by: Taylor Contreras, taylorcontreras@g.harvard.edu

This script uses output from the NEXT simulation software NEXUS,
and analyzes the number of photons seen by the SiPMs, ranking
the SiPMs by the ammount of photons it sees.
"""

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rcParams
rcParams['mathtext.fontset'] = 'stix'
rcParams['font.family'] = 'STIXGeneral'
rcParams['figure.figsize'] = [11, 8]
rcParams['font.size'] = 22

print("Starting")
nfiles = 50 # will fail if too few events
event_type = '0vbb'


mcs = {'s1.3mmp3.5mm':
        {'size':1.3, 'pitch':3.5, 'teflon':False, 'nsipms':61053,  'run':True, 'color':'red'},
      #'s1.3mmp2.4mm':
      #  {'size':1.3, 'pitch':2.4, 'teflon':False, 'nsipms':129889, 'run':True},
    's3mmp5.5mm':
        {'size':3,   'pitch':5.5, 'teflon':False, 'nsipms':24748,  'run':True, 'color':'orange'},
    's6mmp11mm':
        {'size':6,   'pitch':11,  'teflon':False, 'nsipms':6181,   'run':True, 'color':'purple'}#,
    #'s6mmp7.8mm':
    #    {'size':6,   'pitch':7.8, 'teflon':False, 'nsipms':12304,   'run':True}
    }

outdir = '/n/home12/tcontreras/plots/trackingplane/'
indir = "/n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/full_sims/"

for mc in mcs:
    if mcs[mc]['run']:
        sipms_mean = np.array([])
        sipms_max = np.array([])

        if event_type == 'kr83m':
            files = [indir + mc + f'/kr83m/nexus/hdf5/flex.0vbb.{i}.nexus.h5' for i in range(0,nfiles)]
        else:
            files = [indir + mc + f'/0vbb/nexus/hdf5/flex.0vbb.{i}.nexus.h5' for i in range(0,nfiles)]

        for file in files:

            print('Running: '+file)
            try:
                sns_response = pd.read_hdf(file, 'MC/sns_response')
            except:
                print("Couldn't open file: "+file)
                continue

            # Sort to sum up all charges for each sipms
            sns_response_sorted = sns_response.sort_values(by=['sensor_id'])
            sipm_response = sns_response_sorted.loc[sns_response_sorted["sensor_id"] >999]
            sipms_mean = np.append(sipms_mean, sipm_response.groupby('event_id').apply(lambda grp: np.mean(grp.charge)))
            sipms_max = np.append(sipms_max, sipm_response.groupby('event_id').apply(lambda grp: np.max(grp.charge)))

        mcs[mc]['sipms_mean'] = sipms_mean
        mcs[mc]['sipms_max'] = sipms_max
            
        plt.hist(mcs[mc]['sipms_max'])
        plt.xlabel('max SiPM charge [PE] / microsecond / event')
        plt.title(mc)
        plt.yscale('log')
        plt.savefig(outdir+'edges_max_'+mc+'.png')
        plt.close()

        plt.hist(mcs[mc]['sipms_mean'])
        plt.xlabel('mean SiPM charge [PE] / microsecond / event')
        plt.title(mc)
        plt.yscale('log')
        plt.savefig(outdir+'edges_mean_'+mc+'.png')
        plt.close()

mcs_by_size = [[], [], []]
for mc in mcs:
    if mcs[mc]['run']:
        if mcs[mc]['size'] == 1.3:
            mcs_by_size[0].append(mcs[mc])
            mcs[mc]['r_max'] = (0,1500)
            mcs[mc]['r_mean'] = (0,8)
            mcs[mc]['est'] = 283
        elif mcs[mc]['size'] == 3:
            mcs_by_size[1].append(mcs[mc])
            mcs[mc]['r_max'] = (0, 10000)
            mcs[mc]['r_mean'] = (0,25)
            mcs[mc]['est'] = 1487
        elif mcs[mc]['size'] == 6:
            mcs_by_size[2].append(mcs[mc])
            mcs[mc]['r_max'] = (0, 35000)
            mcs[mc]['r_mean'] = (0,60)
            mcs[mc]['est'] = 5645

bins = 100
for mcs in mcs_by_size:
    bins_mean = 0
    if len(mcs) > 0:
        for mc in mcs:
            if mc['run']:
                plt.hist(mc['sipms_max'], label=f"{mc['size']}mm SiPMs, {mc['pitch']} pitch", 
                        range=mc['r_max'], bins=bins, color=mc['color'])
                bins_mean = max(bins_mean, mc['r_mean'][1])
                print(f"{mc['size']} SiPM, {mc['pitch']} pitch, min of max charges: {min(mc['sipms_max'])}")
        plt.xlabel(r'max SiPM charge [PE] / $\mu s$ / event')
        plt.ylabel('Events')
        plt.title('NextFlex MC')
        plt.yscale('log')
        plt.legend()
        plt.savefig(outdir+'edges_max_'+str(mc['size'])+'mm.png')
        plt.vlines(mc['est'], 0, 200, 'r', label='Estimate')
        plt.savefig(outdir+'edges_max_'+str(mc['size'])+'mm_est.png')
        plt.close()