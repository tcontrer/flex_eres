#!/bin/bash
#SBATCH -J update_width    # A single job name for the array
#SBATCH -n 1                                   # Number of cores
#SBATCH -N 1                                   # Ensure that all cores are on one machine
#SBATCH -t 0-1:00                              # Runtime in D-HH:MM, minimum of 10 minutes
#SBATCH -p shared                            # Partition to submit to
#SBATCH --mem=5000                             # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o out/width_%a.out  # File to which STDOUT will be written, %j inserts jobid
#SBATCH -e err/width_%a.err  # File to which STDERR will be written, %j inserts jobid

source /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/IC_setup.sh

RUNNUM=0
TRIGGER=trigger1
STARTDIR=/n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/full_sims/
KDST=/kr83m/kdsts/sthresh/hdf5/flex.kr83m.${SLURM_ARRAY_TASK_ID}.kdsts.h5
PMAP=/kr83m/hypathia/sthresh/hdf5/flex.kr83m.${SLURM_ARRAY_TASK_ID}.pmaps.h5
OUTFILE=/kr83m/kdsts/sthresh/kdsts_w/flex.kr83m.${SLURM_ARRAY_TASK_ID}.kdst.h5

python /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/eres_taylor/update_width.py ${STARTDIR} ${PMAP} ${KDST} ${OUTFILE}