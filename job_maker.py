#!/usr/bin/env python
import os,sys,optparse,logging,glob,copy,stat,numpy
logger = logging.getLogger(__name__)

# slic -x -i output/tev14_pythia8_zbbar_m3000_8_truth.slcio  -g geom/sifcch7.lcdd
#      -m geom/config/defaultILCCrossingAngle.mac  -o output/tev14_pythia8_zbbar_m3000_8.slcio  -r 5000

def main():
   ''' simple starter program that can be copied for use when starting a new script. '''
   logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

   parser = optparse.OptionParser(description='')
   parser.add_option('-i','--input',dest='input',help='input config file for generator')
   parser.add_option('-n','--nodes-per-job',dest='nodes_per_job',help='the number of nodes in a single batch job',type='int')
   parser.add_option('-p','--processes-per-node',dest='processes_per_node',help='the number of processes per node',type='int',default=68)
   parser.add_option('-e','--events',dest='events',help='the number of events to produce per process',type='int',default=100000)
   parser.add_option('-q','--queue',dest='queue',help='queue name',default='normal')
   parser.add_option('-t','--time',dest='time',help='walltime',default='01:30:00')
   #parser.add_option('-j','--jobs',dest='jobs',help='the number of jobs in total',type='int',default=100000)
   options,args = parser.parse_args()


   manditory_args = [
                     'input',
                     'nodes_per_job',
                     'processes_per_node',
                     'events',
                     'queue',
                     'time',
                  ]

   for man in manditory_args:
      if man not in options.__dict__ or options.__dict__[man] is None:
         logger.error('Must specify option: ' + man)
         parser.print_help()
         sys.exit(-1)

   
   logger.info('creating jobs for this file: %s',options.input)

   logger.info('using %s processes per node and %s nodes per job',options.processes_per_node,options.nodes_per_job)
   
   jobtype = os.path.basename(options.input).replace('.py','')
   
   processlevel_cmd = 'A_RUN %s %s %s > %s 2>&1 & \n'

   script_dir = 'runscripts_%snodes' % options.nodes_per_job
   if not os.path.exists(script_dir):
      os.makedirs(script_dir)

   # this is a script that will be created dynamically that runs <processes_per_node> 
   # convert_corescript_filename scripts on a single node with different files
   nodelevel_cmd = 'srun -N 1 -n 1 --ntasks-per-node=1 --cpu_bind=verbose,none --cpus-per-task=272 -o out/%s/%%j/node%04d.stdout -e out/%s/%%j/node%04d.stderr shifter %s & \n'
   nodescript_filename = script_dir + '/nodescript_%04d.sh'
   nodescript_start = '''#!/bin/bash -l

echo [$SECONDS] starting node job script

'''

   # this is the job submission script that launches all the nodescripts
   jobscript_filename  = script_dir + '/jobscript.sh'
   
   # this is the start of the content for the job script
   jobscript_start = '''#!/bin/bash -l
#SBATCH -N {nodes}
#SBATCH -p {queue}
#SBATCH -C knl,quad,cache
#SBATCH -t {time}
#SBATCH -L SCRATCH
#SBATCH --image=dbcooper/centos7hepsim:latest
#SBATCH --job-name={name}

echo [$SECONDS] starting conversion jobs

mkdir -p out/{type}/${{SLURM_JOBID}}

'''

   # this is the job script
   jobscript = jobscript_start
   # this is the node script
   nodescript = nodescript_start
   
   for node_num in xrange(options.nodes_per_job):

      for job_num in xrange(options.processes_per_node):


         output = 'out/' + jobtype + '/${SLURM_JOBID}/' + os.path.basename(options.input).replace('.py','') + '_node%04d_proc%04d.root' % (node_num,job_num)
         logfile = output.replace('.root','.log')
         nodescript += processlevel_cmd % (options.input,output,options.events,logfile)


      # calculate node number starting from 1 and use in filename
      filename = nodescript_filename % node_num
      logger.info('node filename %s',filename)
      # add wait to the end of the script 
      nodescript += 'wait\n'
      nodescript += 'echo [$SECONDS] done\n'
      # write script
      write_script(filename,nodescript)

      # restart nodescript
      nodescript = nodescript_start
      
      jobscript += nodelevel_cmd % (jobtype,node_num,jobtype,node_num,filename)

   # calculate node number starting from 1 and use in filename
   filename = jobscript_filename
   logger.info('filename %s',filename)
   # add wait to the end of the script 
   jobscript += 'wait\n'
   #jobscript += 'find out/' + jobtype + '/$SLURM_JOBID/ -name "*.log" -exec head {} \; | grep "RANDNUM=" > out/$SLURM_JOBID/randomseeds.txt'
   jobscript += 'echo [$SECONDS] running hadd\n'
   jobscript += 'source /global/homes/p/parton/scripts/setupROOT.sh\n'
   jobscript += 'hadd -n ' + str(options.processes_per_node) + ' out/' + jobtype + '/${{SLURM_JOBID}}_hadd_output.root out/' + jobtype + '/${{SLURM_JOBID}}/*.root\n'
   jobscript += 'echo [$SECONDS] done\n'
   # write script
   write_script(filename,jobscript.format(nodes=options.nodes_per_job,queue=options.queue,time=options.time,type=jobtype,name=jobtype))


def write_script(filename,script):
   open(filename,'w').write(script)
   make_exe(filename)

def make_exe(file):
   os.chmod(file,os.stat(file).st_mode | stat.S_IEXEC)

if __name__ == "__main__":
   main()
