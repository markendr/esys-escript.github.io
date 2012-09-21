
##############################################################################
#
# Copyright (c) 2003-2012 by University of Queensland
# http://www.uq.edu.au
#
# Primary Business: Queensland, Australia
# Licensed under the Open Software License version 3.0
# http://www.opensource.org/licenses/osl-3.0.php
#
# Development until 2012 by Earth Systems Science Computational Center (ESSCC)
# Development since 2012 by School of Earth Sciences
#
##############################################################################

__copyright__="""Copyright (c) 2003-2012 by University of Queensland
http://www.uq.edu.au
Primary Business: Queensland, Australia"""
__license__="""Licensed under the Open Software License version 3.0
http://www.opensource.org/licenses/osl-3.0.php"""
__url__="https://launchpad.net/escript-finley"

#
#   small test problem fro temperture advection:
#
#   p=(x0+x1)*t
#

import os
from esys.escript.modelframe import Link,Simulation
from esys.modellib.geometry import RectangularDomain,VectorConstrainerOverBox
from esys.modellib.input import Sequencer
from esys.modellib.probe import Probe,EvaluateExpression
from esys.modellib.flow import SteadyIncompressibleFlow

dom=RectangularDomain()
dom.order=2

constraints=VectorConstrainerOverBox()
constraints.domain=Link(dom)
constraints.left=[1,0,0]
constraints.right=[1,0,0]
constraints.top=[0,1,0]
constraints.bottom=[0,1,0]
constraints.front=[0,0,1]
constraints.back=[0,0,1]

sqe=Sequencer()
sqe.dt_max=0.5
sqe.t_end=1.

source=EvaluateExpression()
source.domain=Link(dom)
source.t=Link(sqe)
source.expression=["t","t"]

flow=SteadyIncompressibleFlow()
flow.domain=Link(dom,"domain")
flow.internal_force=Link(source,"out")
flow.location_prescribed_velocity=Link(constraints,"location_of_constraint")
flow.prescribed_velocity=[0.,0.]

ptest=Probe()
ptest.expression="(x[0]+x[1]-1.)*t"
ptest.t=Link(sqe)
ptest.value=Link(flow,"pressure")

s=Simulation([sqe,constraints,Simulation([flow],debug=True),ptest],debug=True)
s.writeXML()
s.run()
