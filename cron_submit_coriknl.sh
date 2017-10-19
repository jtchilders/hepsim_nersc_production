#/bin/bash


WORKING_DIR=/global/cscratch1/sd/parton/anl_hl_lhc_analysis/lepton_dijet-master
# submit script
echo WORKING_DIR:     $WORKING_DIR
echo HOST:            $(/bin/hostname)

MAX_QUEUED_JOBS=10
MAX_RUNNING_NODES=400

NODES=1
MYRANDOM=$(( RANDOM % 5 ))
if [[ $MYRANDOM -eq 0 ]] || [[ $MYRANDOM -eq 1 ]]; then
   NODES=10
elif [[ $MYRANDOM -eq 2 ]] || [[ $MYRANDOM -eq 3 ]]; then
   NODES=20
else
   NODES=50
fi
#module load slurm/cori
NODES=10

SUBMIT_SCRIPT=$WORKING_DIR/runscripts_${NODES}nodes/jobscript.sh

echo MAX_QUEUED_JOBS: $MAX_QUEUED_JOBS
echo MAX_RUNNING_NODES: $MAX_RUNNING_NODES
echo SUBMIT_SCRIPT: $SUBMIT_SCRIPT
echo NODES: $NODES


cd $WORKING_DIR

PROJECT=m2015

echo PROJECT: $PROJECT

# currently queued
QUEUED_JOBS=$(squeue -A $PROJECT -t PD -p knl  | wc -l)
RUNNING_NODES=$(squeue -A $PROJECT -t R -p knl -o "%.6D" -u parton --noheader | paste -sd+ | bc)
if [ -z $RUNNING_NODES ]; then
   RUNNING_NODES=0
fi
echo QUEUED_JOBS: $QUEUED_JOBS
echo RUNNING_NODES: $RUNNING_NODES
if (( $QUEUED_JOBS < $MAX_QUEUED_JOBS && $RUNNING_NODES < $MAX_RUNNING_NODES )); then
   sbatch -A $PROJECT $SUBMIT_SCRIPT 
fi


