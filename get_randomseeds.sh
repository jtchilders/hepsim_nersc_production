#!/usr/bin/env bash

DIR=$1
echo DIR=$DIR
echo number of directories $(find $DIR/* -type d -maxdepth 1 | wc -l)
for dir in `find $DIR/* -type d -maxdepth 1`; do
   if [ ! -e $dir/randomseeds.txt ]; then
      echo getting $dir
      find $dir -name "*.log" -exec head {} \; | grep "RANDNUM=" > $dir/randomseeds.txt
   else
      echo skipping $dir
   fi
done
#find $DIR -name "*.log" -exec head {} \; | grep "RANDNUM=" > $DIR/randomseeds.txt
echo done

