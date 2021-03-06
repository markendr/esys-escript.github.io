
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
from __future__ import print_function, division
import py_compile
from sys import * 

if len(argv)!=3:
    print("%s source dest"%argv[0], file=stderr)
    exit(2)
try:
    py_compile.compile(argv[1], argv[2], argv[1], True)
except Exception as e:
   print(e.args)
   exit(1)

