#!/bin/bash
#SBATCH -n 1                # Number of cores
#SBATCH -N 1                # Ensure that all cores are on one machine
#SBATCH -t 1-5:00          # Runtime in D-HH:MM, minimum of 10 minutes
#SBATCH -p serial_requeue   # Partition to submit to
#SBATCH --mem=40000          # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o out/myoutput_edges_qbb.out  # File to which STDOUT will be written, %j inserts jobid
#SBATCH -e err/myerrors_edges_qbb.err  # File to which STDERR will be written, %j inserts jobid

source /n/holystore01/LABS/guenette_lab/Users/tcontreras/IC_setup2020.sh

python3  /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/eres_taylor/sipmstudy_edges_qbb.py
