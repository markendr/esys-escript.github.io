
##############################################################################
#
# Copyright (c) 2003-2015 by The University of Queensland
# http://www.uq.edu.au
#
# Primary Business: Queensland, Australia
# Licensed under the Open Software License version 3.0
# http://www.opensource.org/licenses/osl-3.0.php
#
# Development until 2012 by Earth Systems Science Computational Center (ESSCC)
# Development 2012-2013 by School of Earth Sciences
# Development from 2014 by Centre for Geoscience Computing (GeoComp)
#
##############################################################################

"""Data inversion module built on escript"""

__copyright__="""Copyright (c) 2003-2015 by The University of Queensland
http://www.uq.edu.au
Primary Business: Queensland, Australia"""
__license__="""Licensed under the Open Software License version 3.0
http://www.opensource.org/licenses/osl-3.0.php"""
__url__="https://launchpad.net/escript-finley"

from .costfunctions import *
from .datasources import *
from .domainbuilder import *
from .forwardmodels import *
from .inversioncostfunctions import *
from .splitinversioncostfunctions import *
from .inversions import *
from .mappings import *
from .minimizers import *
from .regularizations import *
from .splitregularizations import *
from .coordinates import *
from .seismic import *
from .domaingeneratordcresistivity import *
from .dcresistivityforwardmodeling import *

import logging
logging.basicConfig(format='%(name)s: %(message)s', level=logging.INFO)

#prevents our doc script from processing these packages since they are already incorporated into this one
__nodocorecursion=['costfunctions', 'datasources', ' domainbuilder', 'forwardmodels', 'inversioncostfunctions',
'inversions', 'mappings', 'minimizers', 'regularizations', 'coordinates']
