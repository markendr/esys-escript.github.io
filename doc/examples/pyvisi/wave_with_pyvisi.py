
########################################################
#
# Copyright (c) 2003-2008 by University of Queensland
# Earth Systems Science Computational Center (ESSCC)
# http://www.uq.edu.au/esscc
#
# Primary Business: Queensland, Australia
# Licensed under the Open Software License version 3.0
# http://www.opensource.org/licenses/osl-3.0.php
#
########################################################

__copyright__="""Copyright (c) 2003-2008 by University of Queensland
Earth Systems Science Computational Center (ESSCC)
http://www.uq.edu.au/esscc
Primary Business: Queensland, Australia"""
__license__="""Licensed under the Open Software License version 3.0
http://www.opensource.org/licenses/osl-3.0.php"""
__url__="https://launchpad.net/escript-finley"

"""
Author: Lutz Gross, l.gross@uq.edu.au
Author: John Ngui, john.ngui@uq.edu.au
"""

# Import the necessary modules.
from esys.escript import *
from esys.escript.pdetools import Locator
from esys.escript.linearPDEs import LinearPDE
from esys.finley import Brick
from numpy import identity,zeros,ones
from esys.pyvisi import Scene, DataCollector, Ellipsoid, Camera
from esys.pyvisi.constant import *
import os

PYVISI_EXAMPLE_IMAGES_PATH = "data_sample_images"
X_SIZE = 400
Y_SIZE = 300
JPG_RENDERER = Renderer.ONLINE_JPG

ne=32          # number of cells in x_0 and x_1 directions
width=10000.  # length in x_0 and x_1 directions
lam=3.462e9
mu=3.462e9
rho=1154.
tend=60
h=(1./5.)*sqrt(rho/(lam+2*mu))*(width/ne)

U0=0.01 # amplitude of point source

def wavePropagation(domain,h,tend,lam,mu,rho,U0):
   x=domain.getX()
   # ... open new PDE ...
   mypde=LinearPDE(domain)
   mypde.setSolverMethod(LinearPDE.LUMPING)
   kronecker=identity(mypde.getDim())

   #  spherical source at middle of bottom face

   xc=[width/2.,width/2.,0.]
   # define small radius around point xc
   # Lsup(x) returns the maximum value of the argument x
   src_radius = 0.1*Lsup(domain.getSize())
   dunit=numpy.array([1.,0.,0.]) # defines direction of point source

   mypde.setValue(D=kronecker*rho)
   # ... set initial values ....
   n=0
   # initial value of displacement at point source is constant (U0=0.01)
   # for first two time steps
   u=U0*whereNegative(length(x-xc)-src_radius)*dunit
   u_last=U0*whereNegative(length(x-xc)-src_radius)*dunit
   t=0

   # define the location of the point source 
   L=Locator(domain,numpy.array(xc))
   # find potential at point source
   u_pc=L.getValue(u)
  
   u_pc_x = u_pc[0]
   u_pc_y = u_pc[1]
   u_pc_z = u_pc[2]

   # open file to save displacement at point source
   #u_pc_data=open('./data/U_pc.out','w')
   #u_pc_data.write("%f %f %f %f\n"%(t,u_pc_x,u_pc_y,u_pc_z))
 
   # Create a Scene.
   s = Scene(renderer = JPG_RENDERER, x_size = X_SIZE, y_size = Y_SIZE)

   # Create a DataCollector reading directly from escript objects.
   dc = DataCollector(source = Source.ESCRIPT)

   # Create an Ellipsoid.
   e = Ellipsoid(scene = s, data_collector = dc, 
           viewport = Viewport.SOUTH_WEST,
           lut = Lut.COLOR, cell_to_point = True, outline = True)
   e.setScaleFactor(scale_factor = 0.7)
   e.setMaxScaleFactor(max_scale_factor = 1000)
   e.setRatio(ratio = 10)

   # Create a Camera.
   c = Camera(scene = s, viewport = Viewport.SOUTH_WEST)
   c.isometricView()

   while t<0.4:
     # ... get current stress ....
     g=grad(u)
     stress=lam*trace(g)*kronecker+mu*(g+transpose(g))
     # ... get new acceleration ....
     mypde.setValue(X=-stress)          
     a=mypde.getSolution()
     # ... get new displacement ...
     u_new=2*u-u_last+h**2*a
     # ... shift displacements ....
     u_last=u
     u=u_new
     t+=h
     n+=1
     u_pc=L.getValue(u)
     
     u_pc_x=u_pc[0]
     u_pc_y=u_pc[1]
     u_pc_z=u_pc[2]
      
     # ... save current acceleration in units of gravity and displacements 
     if n==1 or n%10==0: 

         dc.setData(acceleration = length(a)/9.81, displacement = u, 
                 tensor = stress, Ux = u[0])
        
          # Render the object.
         s.render(image_name = os.path.join(PYVISI_EXAMPLE_IMAGES_PATH, \
                 "wave%02d.jpg") % (n/10))
  
mydomain=Brick(ne,ne,10,l0=width,l1=width,l2=10.*width/32.)
wavePropagation(mydomain,h,tend,lam,mu,rho,U0)

