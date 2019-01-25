
##############################################################################
#
# Copyright (c) 2003-2018 by The University of Queensland
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

# This is a template configuration file for escript on Debian/GNU Linux.
# Refer to README_FIRST for usage instructions.

from scons.templates.sid_py3_options import *

mpi = 'OPENMPI'
import sysconfig
multiarch = sysconfig.get_config_var('MULTIARCH')
mpi_include = '/usr/lib/' + multiarch + '/openmpi/include'
mpi_lib = '/usr/lib/' + multiarch + '/openmpi/lib'
mpi_prefix = [mpi_include,mpi_lib]

cxx_extra=' -Wno-stringop-truncation'