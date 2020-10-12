#!/bin/bash -l

#SBATCH --partition=fat
#SBATCH --time=20:00:00
#SBATCH --nodes=1

#SBATCH --job-name=TPB_1
#SBATCH --ntasks-per-node=20
#SBATCH -o bo-%j.log


module purge 
#Is that necessary?
#module load mpi/openmpi/2.1.0/intel intel-studio-2017 comp/gcc/6.3.0
module load intel-studio-2018
module load software/abaqus/abaqus_2016


input_file=3PBV.inp

working_dir=./~
#working_dir=~/E11
#working_dir=./E11
cd $working_dir

### Create ABAQUS environment file for current job, you can set/add your own options (Python syntax)
env_file=custom_v6.env


#########################################################################


cat << EOF > ${env_file}
mp_file_system = (DETECT,DETECT)
EOF

node_list=$(scontrol show hostname ${SLURM_NODELIST} | sort -u)

mp_host_list="["
for host in ${node_list}; do
    mp_host_list="${mp_host_list}['$host', ${SLURM_CPUS_ON_NODE}],"
done

mp_host_list=$(echo ${mp_host_list} | sed -e "s/,$/]/")

echo "mp_host_list=${mp_host_list}"  >> ${env_file}


### Set input file and job (file prefix) name here
job_name=${SLURM_JOB_NAME}


### ABAQUS parallel execution
abaqus job=${job_name} input=${input_file} cpus=${SLURM_NTASKS} standard_parallel=all mp_mode=mpi interactive
