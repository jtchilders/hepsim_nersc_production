#!/usr/bin/env python
import os,sys,optparse,logging,glob,subprocess
logger = logging.getLogger(__name__)

def main():
   ''' simple starter program that can be copied for use when starting a new script. '''
   logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

   parser = optparse.OptionParser(description='')
   parser.add_option('-i','--input',dest='input',help='input')
   options,args = parser.parse_args()

   
   manditory_args = [
                     'input',
                  ]

   for man in manditory_args:
      if man not in options.__dict__ or options.__dict__[man] is None:
         logger.error('Must specify option: ' + man)
         parser.print_help()
         sys.exit(-1)
   
   
   filelist = glob.glob(options.input)

   random_seeds = []
   total_events = 0

   for filename in filelist:
      with open(filename) as file:
         for line in file:
            parts = line.split()
            if len(parts) == 2:
               seed = int(parts[0])
               if seed not in random_seeds:
                  random_seeds.append(seed)
                  total_events += int(parts[1])
               else:
                  logger.warning('%s %s is a duplicate',seed,filename)
                  duplicate_removal(seed,filename)
            else:
               parts = line.split('=')
               if len(parts) == 2:
                  seed = int(parts[1])
                  if seed not in random_seeds:
                     random_seeds.append(seed)
                  else:
                     logger.warning('%s %s is a duplicate',seed,filename)
                     duplicate_removal(seed,filename)

   print len(random_seeds)
   print len(set(random_seeds))
   print total_events

def duplicate_removal(seed,filename):
   cmd = 'head %s/*.log | grep -B 5 %s' % (os.path.dirname(filename),seed)
   logger.info('running %s',cmd)
   p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
   stdout,stderr = p.communicate()

   start = stdout.find('==> ') + 4
   end = stdout.find(' <==')

   tmpfile = stdout[start:end]

   cmd = 'rm %s' % tmpfile.replace('.log','.*')
   logger.info('would have deleted %s',cmd)
   os.system('rm %s' % tmpfile.replace('.log','.*') )

   # remove random number seeed from seed file
   newfile = open(filename+'.new','w')
   for line in open(filename):
      if str(seed) in line: continue
      newfile.write(line)

   newfile.close()
   logger.info('created new file: %s',newfile.name)
   os.rename(newfile.name,filename)



if __name__ == "__main__":
   main()
