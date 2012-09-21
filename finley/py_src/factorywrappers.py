
##############################################################################
#
# Copyright (c) 2011-2012 by University of Queensland
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

__copyright__="""Copyright (c) 2011-2012 by University of Queensland
http://www.uq.edu.au
Primary Business: Queensland, Australia"""
__license__="""Licensed under the Open Software License version 3.0
http://www.opensource.org/licenses/osl-3.0.php"""
__url__="https://launchpad.net/escript-finley"


from .finleycpp import __Brick_driver, __Rectangle_driver


def Rectangle(n0=1, n1=1, order=1, l0=1.0, l1=1.0, periodic0=False, periodic1=False, integrationOrder=-1, 
      reducedIntegrationOrder=-1, useElementsOnFace=None, useFullElementOrder=0, optimize=0, **kwargs):
    points=[]
    tags=[]
    if 'diracPoints' in kwargs:
        points=kwargs['diracPoints']
    if 'diracTags' in kwargs:
        tags=kwargs['diracTags']
    faceon=useElementsOnFace
    if useElementsOnFace is None:	#We want to use 1 as the default, but only where it makes sense
        if useFullElementOrder or order==-1:
	    faceon=0	#Don't use it
	else:
	    faceon=1
    return __Rectangle_driver([n0, n1, order, l0, l1, periodic0, periodic1, integrationOrder, 
      reducedIntegrationOrder, faceon, useFullElementOrder, optimize, points, tags])

def Brick(n0=1, n1=1, n2=1, order=1, l0=1.0, l1=1.0, l2=1.0, periodic0=0, periodic1=0, periodic2=0,
    integrationOrder=-1, reducedIntegrationOrder=-1, useElementsOnFace=1, useFullElementOrder=0,
    optimize=0, **kwargs):
    points=[]
    tags=[]
    if 'diracPoints' in kwargs:
        points=kwargs['diracPoints']
    if 'diracTags' in kwargs:
        tags=kwargs['diracTags']
    faceon=useElementsOnFace
    if useElementsOnFace is None:	#We want to use 1 as the default, but only where it makes sense
        if useFullElementOrder or order==-1:
	    faceon=0	#Don't use it
	else:
	    faceon=1        
    return __Brick_driver([n0, n1, n2, order, l0, l1, l2, periodic0,  periodic1, periodic2,
    integrationOrder, reducedIntegrationOrder, faceon, useFullElementOrder,
    optimize, points, tags])
