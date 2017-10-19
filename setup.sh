#!/bin/bash

echo "Pythia8 setup on atlas1"
# run it as: source ./setup.sh

#source /share/grid/app/asc_app/asc_rel/1.0/setup-script/set_asc.sh

#export PYTHIA8_DIR=/share/sl6/pythia8
export PYTHIA8DATA=$PYTHIA8_DIR/share/Pythia8/xmldoc
# LHAPDF6 configuration.
export LHAPDF6_USE=true
#export LHAPDF6_BIN=/share/sl6/lhapdf6/bin/
export PATH=$LHAPDF6_BIN:$PATH
#export LHAPDF6_INCLUDE=/share/sl6/lhapdf6/include/
#export LHAPDF6_LIB=/share/sl6/lhapdf6/lib
export LHAPDF_DATA_PATH=/global/cscratch1/sd/parton/anl_hl_lhc_analysis/lepton_dijet-master/lhapdf

export LD_LIBRARY_PATH=$LHAPDF6_LIB/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$PYTHIA8_DIR/lib:$LD_LIBRARY_PATH

#export HEPMC=/share/sl6/HEPMC
export LD_LIBRARY_PATH=$HEPMC/lib:$LD_LIBRARY_PATH

#export PROMC=/share/sl6/promc
export LD_LIBRARY_PATH=$PROMC/lib:$LD_LIBRARY_PATH
export PATH=$PROMC/bin:$PATH
export PKG_CONFIG_PATH=${PROMC}/lib/pkgconfig:${PKG_CONFIG_PATH}
export PYTHONPATH=${PROMC}/python/lib/python2.4/site-packages:$PYTHONPATH

