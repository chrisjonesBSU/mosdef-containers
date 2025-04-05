#!/bin/bash
#SBATCH --job-name=gpu_job_example
#SBATCH --partition=shortgpu
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=job_%j.out
#SBATCH --error=job_%j.err

# Load any necessary modules
source ~/.bashrc

# Run your script
apptainer exec --nv --bind /bsuscratch/cjones $MOSDEF_IMG python /bsuscratch/cjones/test-containers/mosdef-containers/examples/slurm/test.py

