#!/bin/python
import random,os,sys

output = sys.argv[1]
type_randfile = os.path.join(os.path.dirname(os.path.dirname(output)),'randomseeds.txt')

#print 'type_randfile =',type_randfile

while True:
   rand = random.randint(0,9e8)
   found = False
   if os.path.exists(type_randfile):
      for line in open(type_randfile):
         if str(rand) in line:
            rand = random.randint(0,9e8)
            found = True
            break

   if not found: break

#print 'rand =',rand

print(str(rand))

