# Script to make scripts to run distribution plots for each configuration                                                                              # Deletes old scripts if they exist already                                                                                                           
import os

event_type = 'kr83m'
nfiles = 101 # 101 total for kr83m, 1001 total for 0vbb
rcut = 400 # mm
sipm_thresh = 1 # pes
bins = 50
outdir = f'/n/home12/tcontreras/plots/FlexEresStudies/{event_type}/'
mcs = {'s1.3mmp15mm':
           {'size':1.3, 'pitch':15., 'teflon':False, 'nsipms':3308,   'run':True},
       's1.3mmp7mm':
           {'size':1.3, 'pitch':7,   'teflon':False, 'nsipms':15268,  'run':True},
       's1.3mmp1.3mm':
           {'size':1.3, 'pitch':1.3, 'teflon':False, 'nsipms':442705, 'run':True},
       's3mmp15mm':
           {'size':3,   'pitch':15,  'teflon':False, 'nsipms':3308,   'run':True},
       's3mmp7mm':
           {'size':3,   'pitch':7,   'teflon':False, 'nsipms':15268,  'run':True},
       's3mmp3mm':
           {'size':3,   'pitch':3,   'teflon':False, 'nsipms':83124,  'run':True},
       's6mmp15mm':
           {'size':6,   'pitch':15,  'teflon':False, 'nsipms':3308,   'run':True},
       's6mmp6mm':
           {'size':6,   'pitch':6,   'teflon':False, 'nsipms': 20785, 'run':True},
       's1.3mmp15mm_teflon':
           {'size':1.3, 'pitch':15,  'teflon':True,  'nsipms':3308,   'run':True},
       's1.3mmp7mm_teflon':
           {'size':1.3, 'pitch':7,   'teflon':True,  'nsipms':15268,  'run':True},
       's3mmp15mm_teflon':
           {'size':3,   'pitch':15,  'teflon':True,  'nsipms':3308,   'run':True},
       's3mmp7mm_teflon':
           {'size':3,   'pitch':7,   'teflon':True,  'nsipms':15268,  'run':True},
       's6mmp15mm_teflon':
           {'size':6,   'pitch':15,  'teflon':True,  'nsipms':3308,   'run':True}}

jobfile_name = 'jobids_'+event_type+'.txt'
with open(jobfile_name, 'w') as jf:
    jf.write(f'Job IDs for Distributions of {event_type} Simulations:\n')
    for name in mcs:
        mc = mcs[name]
        if mc['run']:
            jf.write(name+'\n')
            pyfile_name = event_type + '.' + name + '.distr.py'
            batchfile_name = 'run_distr_'+event_type+'_'+name+'.sh'

            with open('macros/'+pyfile_name, 'w') as f:
                f.write("import pandas as pd\n")
                f.write("import matplotlib as mpl\n")
                f.write("mpl.use('Agg')\n")
                f.write("import matplotlib.pyplot as plt\n")
                f.write("from matplotlib.offsetbox import AnchoredText\n")
                f.write("from matplotlib.ticker import AutoMinorLocator\n")
                f.write("import numpy as np\n")
                f.write("from scipy.optimize import curve_fit\n")
                f.write("from scipy.stats import norm\n")
                f.write("from invisible_cities.core.core_functions  import shift_to_bin_centers\n")
                f.write(" \n")
                f.write(f"SiPMsize     = {mc['size']}\n")
                f.write(f"SiPMpitch    = {mc['pitch']}\n")
                f.write(f"mc_name      = '{name}'\n")
                f.write(f"teflon       = {mc['teflon']}\n")
                f.write(f"event_type   = '{event_type}'\n")
                f.write(f"rcut         = {rcut}\n") 
                f.write(f"sipm_thresh  = {sipm_thresh}\n") 
                f.write(f"outdir       = '{outdir}'\n") 
                f.write("if teflon:\n") 
                f.write("    mc_teflon = 'teflon'\n")
                f.write("    mc_file_name = mc_name[0:-7]\n") 
                f.write("else:\n") 
                f.write("    mc_teflon = 'no_teflon'\n")
                f.write("    mc_file_name = mc_name\n") 
                f.write(" \n") 
                f.write(f"num_sipms = {mc['nsipms']}\n") 
                f.write(f"num_files = {nfiles}\n") 
                f.write("\n") 
                f.write("def Center_of_Event(sipmtable_df, sipm_thresh=0):\n") 
                f.write("    event_id = sipmtable_df.event_id.values[0]\n") 
                f.write("    sipmtable_df = sipmtable_df[sipmtable_df.charge > sipm_thresh]\n") 
                f.write("    x = np.sum(sipmtable_df.charge*sipmtable_df.X)/np.sum(sipmtable_df.charge)\n") 
                f.write("    y = np.sum(sipmtable_df.charge*sipmtable_df.Y)/np.sum(sipmtable_df.charge)\n") 
                f.write("    charge = np.sum(sipmtable_df.charge)\n") 
                f.write("    r = np.sqrt(x**2 + y**2)\n") 
                f.write("    return pd.Series({'event_id':event_id, 'charge':charge, 'X':x, 'Y':y, 'r':r})\n") 
                f.write(" \n") 
                f.write("active_diam = 984.\n") 
                f.write("tp_area = np.pi * (active_diam/2.)**2  # mm^2\n") 
                f.write("coverage = 100 * num_sipms * SiPMsize**2 / tp_area\n") 
                f.write("data_dir = '/n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/'+mc_name+'/'+event_type+'/detsim/reduced_hdf5/'\n") 
                f.write("fast_sims = [data_dir + f'{event_type}.'+mc_file_name+'.' + str(i) + '.detsim.waveforms.h5' for i in range(0, num_files)]\n") 
                f.write("fast_data = pd.DataFrame()\n") 
                f.write("mc = {'size':SiPMsize, 'pitch':SiPMpitch,\n") 
                f.write("      'teflon':mc_teflon, 'name': f'{SiPMsize} mm size, {SiPMpitch} pitch, {mc_teflon}',\n") 
                f.write("      'num_sipms': num_sipms, 'coverage': coverage}\n") 
                f.write("for j in range(0, num_files): \n") 
                f.write("    this_data = pd.read_hdf(fast_sims[j], 'SiPM/Waveforms')\n") 
                f.write("    event_centers = this_data.groupby('event_id').apply(lambda grp: Center_of_Event(grp, sipm_thresh))\n") 
                f.write("    event_centers = event_centers[event_centers.r < rcut]\n") 
                f.write("    fast_data = fast_data.append(event_centers)\n") 
                f.write("\n") 
                f.write(f"plt.hist(fast_data.charge, bins={bins}, label=f'R < {rcut}, SiPM Charge > {sipm_thresh}')\n") 
                f.write("plt.title(mc['name']+', '+event_type)\n") 
                f.write("plt.xlabel('Total SiPM Charge [pes]')\n") 
                f.write("plt.savefig(outdir+f'charge_r{rcut}_sthresh{sipm_thresh}_'+mc_name+'.png')\n") 
                f.write("plt.close()\n") 
                f.write("\n") 
                f.write(f"plt.hist(fast_data.X, bins={bins}, label=f'R < {rcut}, SiPM Charge > {sipm_thresh}')\n") 
                f.write("plt.title(mc['name']+', '+event_type)\n") 
                f.write("plt.xlabel('X [mm]')\n") 
                f.write("plt.savefig(outdir+f'x_r{rcut}_sthresh{sipm_thresh}_'+mc_name+'.png')\n") 
                f.write("plt.close() \n") 
                f.write("\n") 
                f.write(f"plt.hist(fast_data.Y, bins={bins}, label=f'R < {rcut}, SiPM Charge > {sipm_thresh}')\n") 
                f.write("plt.title(mc['name']+', '+event_type)\n") 
                f.write("plt.xlabel('Y [mm]')\n") 
                f.write("plt.savefig(outdir+f'y_r{rcut}_sthresh{sipm_thresh}_'+mc_name+'.png')\n") 
                f.write("plt.close()\n") 
                f.write("\n") 
                f.write(f"plt.hist(fast_data.r, bins={bins}, label=f'R < {rcut}, SiPM Charge > {sipm_thresh}')\n") 
                f.write("plt.title(mc['name']+', '+event_type)\n") 
                f.write("plt.xlabel('R [mm]')\n") 
                f.write("plt.savefig(outdir+f'r_r{rcut}_sthresh{sipm_thresh}_'+mc_name+'.png')\n") 
                f.write("plt.close()\n") 
                f.write("\n") 
                f.write("print(mc['name'])\n") 
                f.write("print('Events after cuts = '+str(fast_data.charge.count()))\n") 
                f.write("print('Outdir = '+outdir)\n") 
                f.write("print('Coverge = '+str(mc['coverage']))\n") 
                f.write("print('Charge mean = '+str(fast_data.charge.mean()))\n") 
                f.write("print('Charge std = '+str(fast_data.charge.std()))\n") 
                f.write("print('Charge mean/std = '+str(fast_data.charge.mean() / fast_data.charge.std()))\n")
                
            with open('macros/'+batchfile_name, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write("#SBATCH -n 1                                   # Number of cores\n")
                f.write("#SBATCH -N 1                                   # Ensure that all cores are on one machine\n")           
                f.write("#SBATCH -t 0-1:00                              # Runtime in D-HH:MM, minimum of 10 minutes\n")
                f.write("#SBATCH -p guenette                            # Partition to submit to\n")
                f.write("#SBATCH --mem=5000                             # Memory pool for all cores (see also --mem-per-cpu)\n")
                f.write(f"#SBATCH -o out/{event_type}_{name}_distr.out  # File to which STDOUT will be written, %j inserts jobid\n")
                f.write(f"#SBATCH -e err/{event_type}_{name}_distr.err  # File to which STDERR will be written, %j inserts jobid\n")                 
                f.write("\n")
                f.write("source /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/IC_setup.sh\n")
                f.write("\n")
                f.write(f"python  /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/eres_taylor/macros/{pyfile_name}\n")

            os.system(f"sbatch macros/{batchfile_name} > out/temp.txt")
            with open('out/temp.txt', 'r') as f:
                jf.write(f.readlines()[0])
