#!/usr/bin/env python

import os,sys

jobid = sys.argv[2]

infile = open(sys.argv[1])
outfile = open(sys.argv[1]+'.tmp','w')

for l in infile:
   if jobid in l: continue
   outfile.write(l)

outfile.close()
infile.close()


os.rename(outfile.name,infile.name)

