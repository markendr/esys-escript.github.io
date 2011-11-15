
########################################################
#
# Copyright (c) 2009-2010 by University of Queensland
# Earth Systems Science Computational Center (ESSCC)
# http://www.uq.edu.au/esscc
#
# Primary Business: Queensland, Australia
# Licensed under the Open Software License version 3.0
# http://www.opensource.org/licenses/osl-3.0.php
#
########################################################

__copyright__="""Copyright (c) 2009-2010 by University of Queensland
Earth Systems Science Computational Center (ESSCC)
http://www.uq.edu.au/esscc
Primary Business: Queensland, Australia"""
__license__="""Licensed under the Open Software License version 3.0
http://www.opensource.org/licenses/osl-3.0.php"""
__url__="https://launchpad.net/escript-finley"

"""
Author: Antony Hallam antony.hallam@uqconnect.edu.au
"""


############################################################FILE HEADER
# example04a.py
# Create either a 2D mesh for a rectangle model using pycad meshing 
# tools.
#
#######################################################EXTERNAL MODULES
from esys.pycad import * #domain constructor
from esys.pycad.gmsh import Design #Finite Element meshing package
from esys.finley import MakeDomain #Converter for escript
from esys.escript import mkDir, getMPISizeWorld
from esys.escript.unitsSI import *
import os
########################################################MPI WORLD CHECK
if getMPISizeWorld() > 1:
	import sys
	print("This example will not run in an MPI world.")
	sys.exit(0)

# make sure path exists 
save_path= os.path.join("data","example04") 
mkDir(save_path)

################################################ESTABLISHING PARAMETERS
#Model Parameters
width=5000.0*m   #width of model
depth=-6000.0*m  #depth of model

####################################################DOMAIN CONSTRUCTION
# Domain Corners
p0=Point(0.0,      0.0, 0.0)
p1=Point(0.0,    depth, 0.0)
p2=Point(width, depth, 0.0)
p3=Point(width,   0.0, 0.0)
# Join corners in anti-clockwise manner.
l01=Line(p0, p1)
l12=Line(p1, p2)
l23=Line(p2, p3)
l30=Line(p3, p0)
# Join line segments to create domain boundary.
c=CurveLoop(l01, l12, l23, l30)
# surface
rec = PlaneSurface(c)

#############################################EXPORTING MESH FOR ESCRIPT
# Create a Design which can make the mesh
d=Design(dim=2, element_size=200*m)
# Add the subdomains and flux boundaries.
d.addItems(rec, PropertySet("linebottom",l12) )
d.addItems(l23, l30, l01) # just in case we need them.

# this is the name of gmsh input file generated by pycad
#
# >> gmsh example04.geo
#
# to show the mesh.
#
d.setScriptFileName(os.path.join(save_path,"example04.geo"))

# this is the name of mesh file generated gmsh. Use
#
# >> gmsh example04.msh
#
# to show the mesh.
#
d.setMeshFileName(os.path.join(save_path,"example04.msh"))
#
#  make the domain:
#
domain=MakeDomain(d)
# Create a file that can be read back in to python with
# mesh=ReadMesh(fileName)
domain.write(os.path.join(save_path,"example04.fly"))


