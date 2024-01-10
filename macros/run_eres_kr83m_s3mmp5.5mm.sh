#!/bin/bash
#SBATCH -n 1                                   # Number of cores
#SBATCH -N 1                                   # Ensure that all cores are on one machine
#SBATCH -t 0-1:00                              # Runtime in D-HH:MM, minimum of 10 minutes
#SBATCH -p shared                          # Partition to submit to
#SBATCH --mem=5000                             # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o out/kr83m_s3mmp5.5mm_eres.out  # File to which STDOUT will be written, %j inserts jobid
#SBATCH -e err/kr83m_s3mmp5.5mm_eres.err  # File to which STDERR will be written, %j inserts jobid

source /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/IC_setup.sh

python  /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/eres_taylor/macros/GetEres.py 100 3 5.5 s3mmp5.5mm 24748 kr83m 300.0 1200.0 0 /n/home12/tcontreras/plots/FlexEresStudies/kr83m/ data_eres_kr83m_rcut300.0_sthresh0_zcut1200.0_test
