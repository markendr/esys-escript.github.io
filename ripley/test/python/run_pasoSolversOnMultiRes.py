
##############################################################################
#
# Copyright (c) 2003-2016 by The University of Queensland
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

from __future__ import print_function, division

__copyright__="""Copyright (c) 2003-2016 by The University of Queensland
http://www.uq.edu.au
Primary Business: Queensland, Australia"""
__license__="""Licensed under the Open Software License version 3.0
http://www.opensource.org/licenses/osl-3.0.php"""
__url__="https://launchpad.net/escript-finley"

"""
Test suite for PDE solvers on ripley multiresolution domains
"""

from test_simplesolve import SimpleSolveTestCase
import esys.escriptcore.utestselect as unittest
from esys.escriptcore.testing import *

from esys.escript import getMPISizeWorld, sqrt
from esys.ripley import MultiResolutionDomain
from esys.escript.linearPDEs import SolverOptions

# number of elements in the spatial directions
NE0=12
NE1=12
NE2=8
mpiSize=getMPISizeWorld()
for x in [int(sqrt(mpiSize)),2,3,5,7,1]:
    NX=x
    NY=mpiSize//x
    if NX*NY == mpiSize:
        break

for x in [(int(mpiSize**(1/3.)),int(mpiSize**(1/3.))),(2,3),(2,2),(1,2),(1,1)]:
    NXb=x[0]
    NYb=x[1]
    NZb=mpiSize//(x[0]*x[1])
    if NXb*NYb*NZb == mpiSize:
        break

def Rectangle(**kwargs):
    m = MultiResolutionDomain(2, **kwargs)
    return m.getLevel(1)

def Brick(**kwargs):
    m = MultiResolutionDomain(3, **kwargs)
    return m.getLevel(1)

class Test_SimpleSolveMultires2D_Paso_BICGSTAB_Jacobi(SimpleSolveTestCase):
    def setUp(self):
        self.domain = Rectangle(n0=NE0*NX-1, n1=NE1*NY-1, d0=NX, d1=NY)
        self.package = SolverOptions.PASO
        self.method = SolverOptions.BICGSTAB
        self.preconditioner = SolverOptions.JACOBI

    def tearDown(self):
        del self.domain

@unittest.skipIf(mpiSize > 1, "3D Multiresolution domains require single process")
class Test_SimpleSolveMultires3D_Paso_BICGSTAB_Jacobi(SimpleSolveTestCase):
    def setUp(self):
        self.domain = Brick(n0=NE0*NXb-1, n1=NE1*NYb-1, n2=NE2*NZb-1, d0=NXb, d1=NYb, d2=NZb)
        self.package = SolverOptions.PASO
        self.method = SolverOptions.BICGSTAB
        self.preconditioner = SolverOptions.JACOBI

    def tearDown(self):
        del self.domain

class Test_SimpleSolveMultires2D_Paso_PCG_Jacobi(SimpleSolveTestCase):
    def setUp(self):
        self.domain = Rectangle(n0=NE0*NX-1, n1=NE1*NY-1, d0=NX, d1=NY)
        self.package = SolverOptions.PASO
        self.method = SolverOptions.PCG
        self.preconditioner = SolverOptions.JACOBI

    def tearDown(self):
        del self.domain

@unittest.skipIf(mpiSize > 1, "3D Multiresolution domains require single process")
class Test_SimpleSolveMultires3D_Paso_PCG_Jacobi(SimpleSolveTestCase):
    def setUp(self):
        self.domain = Brick(n0=NE0*NXb-1, n1=NE1*NYb-1, n2=NE2*NZb-1, d0=NXb, d1=NYb, d2=NZb)
        self.package = SolverOptions.PASO
        self.method = SolverOptions.PCG
        self.preconditioner = SolverOptions.JACOBI

    def tearDown(self):
        del self.domain

class Test_SimpleSolveMultires2D_Paso_MINRES_Jacobi(SimpleSolveTestCase):
    def setUp(self):
        self.domain = Rectangle(n0=NE0*NX-1, n1=NE1*NY-1, d0=NX, d1=NY)
        self.package = SolverOptions.PASO
        self.method = SolverOptions.MINRES
        self.preconditioner = SolverOptions.JACOBI

    def tearDown(self):
        del self.domain

@unittest.skipIf(mpiSize > 1, "3D Multiresolution domains require single process")
class Test_SimpleSolveMultires3D_Paso_MINRES_Jacobi(SimpleSolveTestCase):
    def setUp(self):
        self.domain = Brick(n0=NE0*NXb-1, n1=NE1*NYb-1, n2=NE2*NZb-1, d0=NXb, d1=NYb, d2=NZb)
        self.package = SolverOptions.PASO
        self.method = SolverOptions.MINRES
        self.preconditioner = SolverOptions.JACOBI

    def tearDown(self):
        del self.domain

class Test_SimpleSolveMultires2D_Paso_TFQMR_RILU(SimpleSolveTestCase):
    def setUp(self):
        self.domain = Rectangle(n0=NE0*NX-1, n1=NE1*NY-1, d0=NX, d1=NY)
        self.package = SolverOptions.PASO
        self.method = SolverOptions.TFQMR
        self.preconditioner = SolverOptions.RILU

    def tearDown(self):
        del self.domain

@unittest.skipIf(mpiSize > 1, "3D Multiresolution domains require single process")
class Test_SimpleSolveMultires3D_Paso_TFQMR_RILU(SimpleSolveTestCase):
    def setUp(self):
        self.domain = Brick(n0=NE0*NXb-1, n1=NE1*NYb-1, n2=NE2*NZb-1, d0=NXb, d1=NYb, d2=NZb)
        self.package = SolverOptions.PASO
        self.method = SolverOptions.TFQMR
        self.preconditioner = SolverOptions.RILU

    def tearDown(self):
        del self.domain


if __name__ == '__main__':
   run_tests(__name__, exit_on_failure=True)
