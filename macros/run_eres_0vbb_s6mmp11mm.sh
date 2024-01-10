#!/bin/bash
#SBATCH -n 1                                   # Number of cores
#SBATCH -N 1                                   # Ensure that all cores are on one machine
#SBATCH -t 0-1:00                              # Runtime in D-HH:MM, minimum of 10 minutes
#SBATCH -p shared                          # Partition to submit to
#SBATCH --mem=5000                             # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o out/0vbb_s6mmp11mm_eres.out  # File to which STDOUT will be written, %j inserts jobid
#SBATCH -e err/0vbb_s6mmp11mm_eres.err  # File to which STDERR will be written, %j inserts jobid

source /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/IC_setup.sh

python  /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/eres_taylor/macros/GetEres.py 1000 6 11 s6mmp11mm 6181 0vbb 300.0 1200.0 0 /n/home12/tcontreras/plots/FlexEresStudies/0vbb/ data_eres_0vbb_rcut300.0_sthresh0_zcut1200.0_test
