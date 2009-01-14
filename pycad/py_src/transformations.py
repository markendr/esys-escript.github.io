
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
__url__="http://www.uq.edu.au/esscc/escript-finley"

"""
transformations

@var __author__: name of author
@var __copyright__: copyrights
@var __license__: licence agreement
@var __url__: url entry point on documentation
@var __version__: version
@var __date__: date of the version
@var DEG: unit of degree
@var RAD: unit of radiant
"""

__author__="Lutz Gross, l.gross@uq.edu.au"

import numarray
import math

_TYPE=numarray.Float64
DEG=math.pi/180.
RAD=1.
class Transformation(object):
   """
   General class to define an affine transformation M{x->Ax+b}.
   """
   def __init__(self):
       """
       Creates a linear transformation.
       """
       pass

   def __call__(self,x=numarray.zeros((3,))):
       """
       Applies transformation to C{x}.
       """
       raise NotImplementeError()

class Translation(Transformation):
    """
    Defines a translation M{x->x+b}.
    """
    def __init__(self,b=numarray.zeros((3,),type=_TYPE)):
       """
       Creates the linear transformation M{x->x+b}.
       """
       super(Translation, self).__init__()
       self.__b=numarray.array(b,_TYPE)

    def __call__(self,x=numarray.zeros((3,))):
       """
       Applies translation to C{x}.
       """
       return numarray.array(x,_TYPE)+self.__b

class Rotatation(Transformation):
    """
    Defines a rotation.
    """
    def __init__(self,axis=numarray.ones((3,),type=_TYPE),point=numarray.zeros((3,),type=_TYPE),angle=0.*RAD):
       """
       Creates a rotation using an axis and a point on the axis.
       """
       self.__axis=numarray.array(axis,type=_TYPE)
       self.__point=numarray.array(point,type=_TYPE)
       lax=numarray.dot(self.__axis,self.__axis)
       if not lax>0:
          raise ValueError("points must be distinct.")
       self.__axis/=math.sqrt(lax)
       self.__angle=float(angle)

    def __call__(self,x=numarray.zeros((3,))):
       """
       Applies the rotation to C{x}.
       """
       x=numarray.array(x,_TYPE)
       z=x-self.__point
       z0=numarray.dot(z,self.__axis)
       z_per=z-z0*self.__axis
       lz_per=numarray.dot(z_per,z_per)
       if lz_per>0:
         axis1=z_per/math.sqrt(lz_per)
         axis2=_cross(axis1,self.__axis)
         lax2=numarray.dot(axis2,axis2)
         if lax2>0:
            axis2/=math.sqrt(lax2)
            return z0*self.__axis+math.sqrt(lz_per)*(math.cos(self.__angle)*axis1-math.sin(self.__angle)*axis2)+self.__point
         else:
            return x
       else:
         return x

def _cross(x, y):
    """
    Returns the cross product of C{x} and C{y}.
    """
    return numarray.array([x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0]], _TYPE)

class Dilation(Transformation):
    """
    Defines a dilation.
    """
    def __init__(self,factor=1.,center=numarray.zeros((3,),type=_TYPE)):
       """
       Creates a dilation with a center and a given expansion/contraction
       factor.
       """
       if not abs(factor)>0:
          raise ValueError("factor must be non-zero.")
       self.__factor=factor
       self.__center=numarray.array(center,type=_TYPE)

    def __call__(self,x=numarray.zeros((3,))):
       """
       Applies dilation to C{x}.
       """
       x=numarray.array(x,_TYPE)
       return self.__factor*(x-self.__center)+self.__center

class Reflection(Transformation):
    """
    Defines a reflection on a plane.
    """
    def __init__(self,normal=numarray.ones((3,),type=_TYPE),offset=0.):
       """
       Defines a reflection on a plane defined in normal form.
       """
       self.__normal=numarray.array(normal,type=_TYPE)
       ln=math.sqrt(numarray.dot(self.__normal,self.__normal))
       if not ln>0.:
          raise ValueError("normal must have positive length.")
       self.__normal/=ln
       if isinstance(offset,float) or isinstance(offset,int):
          self.__offset=offset/ln
       else:
          self.__offset=numarray.dot(numarray.array(offset,type=_TYPE),self.__normal)

    def __call__(self,x=numarray.zeros((3,))):
       """
       Applies reflection to C{x}.
       """
       x=numarray.array(x,_TYPE)
       return x - 2*(numarray.dot(x,self.__normal)-self.__offset)*self.__normal

