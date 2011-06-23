# -*- coding: utf-8 -*-

########################################################
#
# Copyright (c) 2003-2010 by University of Queensland
# Earth Systems Science Computational Center (ESSCC)
# http://www.uq.edu.au/esscc
#
# Primary Business: Queensland, Australia
# Licensed under the Open Software License version 3.0
# http://www.opensource.org/licenses/osl-3.0.php
#
########################################################

__copyright__="""Copyright (c) 2003-2010 by University of Queensland
Earth Systems Science Computational Center (ESSCC)
http://www.uq.edu.au/esscc
Primary Business: Queensland, Australia"""
__license__="""Licensed under the Open Software License version 3.0
http://www.opensource.org/licenses/osl-3.0.php"""
__url__="https://launchpad.net/escript-finley"

"""
:var __author__: name of author
:var __copyright__: copyrights
:var __license__: licence agreement
:var __url__: url entry point on documentation
:var __version__: version
:var __date__: date of the version
"""

import numpy
from esys.escript.linearPDEs import LinearPDE, IllegalCoefficient, IllegalCoefficientValue
from esys.escript import util, Data, Symbol, Evaluator

__author__="Cihan Altinay"

class NonlinearPDE(object):
    """
    This class is used to define a general nonlinear, steady, second order PDE
    for an unknown function *u* on a given domain defined through a `Domain`
    object.

    For a single PDE having a solution with a single component the nonlinear
    PDE is defined in the following form:

    *-div(X) + Y = 0*

    where *X*,*Y*=f(*u*,*grad(u)*), *div(F)* denotes the divergence of *F* and
    *grad(F)* is the spatial derivative of *F*.

    The coefficients *X* (rank 1) and *Y* (scalar) have to be specified through
    `Symbol` objects.

    The following natural boundary conditions are considered:

    *n[j]*X[j] - y = 0*

    where *n* is the outer normal field. Notice that the coefficient *X*
    is defined in the PDE. The coefficient *y* is a scalar `Symbol`.

    Constraints for the solution prescribe the value of the solution at certain
    locations in the domain. They have the form

    *u=r* where *q>0*

    *r* and *q* are each scalar where *q* is the characteristic function
    defining where the constraint is applied. The constraints override any
    other condition set by the PDE or the boundary condition.

    For a system of PDEs and a solution with several components, *u* is rank
    one, while the PDE coefficient *X* is rank two and *Y* and *y* is rank one.

    The PDE is solved by linearising the coefficients and iteratively solving
    the corresponding linear PDE until the error is smaller than a tolerance
    or a maximum number of iterations is reached.

    Typical usage::

        u = Symbol('u', dim=dom.getDim())
        p = NonlinearPDE(dom, u)
        p.setValue(X=grad(u), Y=1.)
        v = p.getSolution(u=0.)
    """

    def __init__(self,domain,u,debug=False):
        """
        Initializes a new nonlinear PDE.

        :param domain: domain of the PDE
        :type domain: `Domain`
        :param u: The symbol for the unknown PDE function u.
        :type u: `Symbol`
        :param debug: if True debug information is printed
        """
        self.coeffs={}
        self._u=u
        self._debug=debug
        if u.getRank()==0:
            numEquations=1
        else:
            numEquations=u.getShape()[0]
        numSolutions=numEquations
        self.lpde=LinearPDE(domain,numEquations,numSolutions,debug)

    def __str__(self):
        """
        Returns the string representation of the PDE.

        :return: a simple representation of the PDE
        :rtype: ``str``
        """
        return "<NonlinearPDE %d>"%id(self)

    def trace(self, text):
        """
        Prints the text message if debug mode is switched on.

        :param text: message to be printed
        :type text: ``string``
        """
        if self._debug:
            print("%s: %s"%(str(self), text))

    def getSolution(self, **subs):
        """
        Returns the solution of the PDE.

        :param subs: Substitutions for all symbols used in the coefficients
                     including the initial value for *u*.
        :return: the solution
        :rtype: `Data`
        """

        if not subs.has_key('u'):
            raise KeyError("Initial value for 'u' missing.")

        ui=subs['u']
        if isinstance(ui,float) or isinstance(ui,int):
            ui=Data(ui, self.lpde.getFunctionSpaceForSolution())
            subs['u']=ui

        coeffs={}
        # separate symbolic expressions from other coefficients
        expressions={}
        for n, e in self.coeffs.items():
            if hasattr(e, "atoms"):
                expressions[n]=e
            else:
                coeffs[n]=e

        # evaluate symbolic expressions
        ev=Evaluator(*expressions.values())
        ev.subs(**subs)
        res=ev.evaluate()
        names=expressions.keys()
        for i in range(len(names)):
            coeffs[names[i]]=res[i]

        # solve linear PDE
        self.lpde.setValue(**coeffs)
        u_new=self.lpde.getSolution()
        n=0
        # perform Newton iterations until error small enough or
        # maximum number of iterations reached
        while util.Lsup(u_new)>self.lpde.getSolverOptions().getTolerance():
            delta_u=u_new
            ev.subs(u=ui-u_new)
            res=ev.evaluate()
            for i in range(len(names)):
                coeffs[names[i]]=res[i]

            self.lpde.setValue(**coeffs)
            u_new=self.lpde.getSolution()
            ui=delta_u
            n=n+1
            if n>self.lpde.getSolverOptions().getIterMax():
                break

        self.trace("Error after %d iterations: %g"%(n,util.Lsup(u_new)))
        return ui

    def getCoefficient(self, name):
        """
        Returns the value of the coefficient ``name``.

        :param name: name of the coefficient requested
        :type name: ``string``
        :return: the value of the coefficient
        :rtype: `Symbol`
        :raise IllegalCoefficient: if ``name`` is not a coefficient of the PDE
        """
        if self.hasCoefficient(name):
            return self.coeffs[name]
        raise IllegalCoefficient("Illegal coefficient %s requested."%name)

    def hasCoefficient(self, name):
        """
        Returns True if ``name`` is the name of a coefficient.

        :param name: name of the coefficient enquired
        :type name: ``string``
        :return: True if ``name`` is the name of a coefficient of the PDE,
                 False otherwise
        :rtype: ``bool``

        """
        return self.coeffs.has_key(name)

    def setValue(self,**coefficients):
        """
        Sets new values to one or more coefficients.

        :param coefficients: new values assigned to coefficients
        :keyword X: value for coefficient ``X``
        :type X: `Symbol` or any type that can be cast to a `Data` object
        :keyword Y: value for coefficient ``Y``
        :type Y: `Symbol` or any type that can be cast to a `Data` object
        :keyword y: value for coefficient ``y``
        :type y: `Symbol` or any type that can be cast to a `Data` object
        :keyword y_contact: value for coefficient ``y_contact``
        :type y_contact: `Symbol` or any type that can be cast to a `Data`
                         object
        :keyword r: values prescribed to the solution at the locations of
                    constraints
        :type r: `Symbol` or any type that can be cast to a `Data` object
        :keyword q: mask for location of constraints
        :type q: `Symbol` or any type that can be cast to a `Data` object

        :raise IllegalCoefficient: if an unknown coefficient keyword is used
        :raise IllegalCoefficientValue: if a supplied coefficient value has an
                                        invalid shape
        """
        u=self._u
        for name,val in coefficients.iteritems():
            shape=util.getShape(val)
            rank=len(shape)
            if name=="X":
                # DX/Du = del_X/del_u + del_X/del_grad(u)*del_grad(u)/del_u
                #            \   /         \   /
                #              B             A
                X=val
                if rank != u.getRank()+1:
                    raise IllegalCoefficientValue("X must have rank %d"%u.getRank()+1)
                if not hasattr(X, 'diff'):
                    A=numpy.zeros(shape+u.grad().getShape())
                    B=numpy.zeros(shape+u.getShape())
                elif u.getRank()==0:
                    dXdu=X.diff(u)
                    dgdu=u.grad().diff(u)
                    A=numpy.empty(shape+dgdu.getShape(), dtype=object)
                    for i in numpy.ndindex(shape):
                        for j in numpy.ndindex(dgdu.getShape()):
                            tmp=dXdu[i].coeff(dgdu[j])
                            A[i,j]=0 if tmp is None else tmp
                    A=Symbol(A).simplify()
                    B=(dXdu-util.matrix_mult(A,dgdu)).simplify()
                else:  #u.getRank()==1
                    dXdu=X.diff(u)
                    dgdu=u.grad().diff(u).transpose(2)
                    I,J=shape
                    K,L=u.grad().getShape()
                    A=numpy.empty((I,J,K,L), dtype=object)
                    for i in range(I):
                        for j in range(J):
                            for k in range(K):
                                for l in range(L):
                                    if dgdu[k,k,l]==0:
                                        A[i,j,k,l]=0
                                    else:
                                        tmp=dXdu[i,j,k].coeff(dgdu[k,k,l])
                                        A[i,j,k,l]=0 if tmp is None else tmp
                    A=Symbol(A).simplify()
                    B=(dXdu-A.tensorProduct(dgdu.transpose(1),2)).simplify()
                self.coeffs['A']=A
                self.coeffs['B']=B
                self.coeffs['X']=X
            elif name=="Y":
                # DY/Du = del_Y/del_u + del_Y/del_grad(u)*del_grad(u)/del_u
                #            \   /         \   /
                #              D             C
                Y=val
                if rank != u.getRank():
                    raise IllegalCoefficientValue("Y must have rank %d"%u.getRank())
                if not hasattr(Y, 'diff'):
                    C=numpy.zeros(shape+u.grad().getShape())
                    D=numpy.zeros(shape+u.getShape())
                elif u.getRank()==0:
                    dYdu=Y.diff(u)
                    dgdu=u.grad().diff(u)
                    C=numpy.empty(dgdu.getShape(), dtype=object)
                    for j in numpy.ndindex(dgdu.getShape()):
                        tmp=dYdu.coeff(dgdu[j])
                        C[j]=0 if tmp is None else tmp
                    C=Symbol(C).simplify()
                    D=(dYdu-util.inner(C,dgdu)).simplify()
                else:  #u.getRank()==1
                    dYdu=Y.diff(u)
                    dgdu=u.grad().diff(u).transpose(2)
                    I,=shape
                    J,K=u.grad().getShape()
                    C=numpy.empty((I,J,K), dtype=object)
                    for i in range(I):
                        for j in range(J):
                            for k in range(K):
                                if dgdu[j,j,k]==0:
                                    C[i,j,k]=0
                                else:
                                    tmp=dYdu[i,j].coeff(dgdu[j,j,k])
                                    C[i,j,k]=0 if tmp is None else tmp
                    C=Symbol(C).simplify()
                    D=(dYdu-C.tensorProduct(dgdu.transpose(1),2)).simplify()
                self.coeffs['C']=C
                self.coeffs['D']=D
                self.coeffs['Y']=Y
            elif name=="y":
                y=val
                if rank != u.getRank():
                    raise IllegalCoefficientValue("y must have rank %d"%u.getRank())
                if not hasattr(y, 'diff'):
                    d=numpy.zeros(u.getShape())
                else:
                    d=y.diff(u)
                self.coeffs['d']=d
                self.coeffs['y']=y
            elif name=="y_contact":
                y_contact=val
                if rank != u.getRank():
                    raise IllegalCoefficientValue("y_contact must have rank %d"%u.getRank())
                if not hasattr(y_contact, 'diff'):
                    d_contact=numpy.zeros(u.getShape())
                else:
                    d_contact=y_contact.diff(u)
                self.coeffs['d_contact']=d_contact
                self.coeffs['y_contact']=y_contact
            elif name=="q":
                if rank != u.getRank():
                    raise IllegalCoefficientValue("q must have rank %d"%u.getRank())
                self.coeffs['q']=val
            elif name=="r":
                if rank != u.getRank():
                    raise IllegalCoefficientValue("r must have rank %d"%u.getRank())
                self.coeffs['r']=val
            else:
                raise IllegalCoefficient("Attempt to set unknown coefficient %s"%key)

