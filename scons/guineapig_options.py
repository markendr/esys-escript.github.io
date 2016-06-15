
##############################################################################
#
# Copyright (c) 2003-2016 by The University of Queensland
# http://www.uq.edu.au
#
# Primary Business: Queensland, Australia
# Licensed under the Apache License, version 2.0
# http://www.apache.org/licenses/LICENSE-2.0
#
# Development until 2012 by Earth Systems Science Computational Center (ESSCC)
# Development 2012-2013 by School of Earth Sciences
# Development from 2014 by Centre for Geoscience Computing (GeoComp)
#
##############################################################################

from templates.sid_py3_mpi_options import *

# disabled until the boost issue is fixed.
#cuda = True
nvccflags = "-ccbin=g++-4.9 -arch=sm_30 -DBOOST_NOINLINE='__attribute__((noinline))'"

parmetis = True
umfpack = True
silo = True
trilinos = True
trilinos_prefix = '/opt/trilinos_hybrid_eti'
cxx_extra += " -Wextra -Wno-deprecated-declarations -Wno-unused-parameter"
launcher = "mpirun ${AGENTOVERRIDE} ${EE} --host %h --map-by node:pe=%t -bind-to none -np %N %b"

