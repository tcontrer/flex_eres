#!/bin/bash
#SBATCH -n 1                                   # Number of cores
#SBATCH -N 1                                   # Ensure that all cores are on one machine
#SBATCH -t 0-1:00                              # Runtime in D-HH:MM, minimum of 10 minutes
#SBATCH -p serial_requeue                          # Partition to submit to
#SBATCH --mem=5000                             # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o out/nexus_0vbb_s3mmp5.5mm.out  # File to which STDOUT will be written, %j inserts jobid
#SBATCH -e err/nexus_0vbb_s3mmp5.5mm.err  # File to which STDERR will be written, %j inserts jobid

source /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/IC_setup.sh

python  /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/eres_taylor/macros/test_nexus.py s3mmp5.5mm 0vbb /n/home12/tcontreras/plots/FlexEresStudies/0vbb/
