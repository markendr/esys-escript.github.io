
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
extra functions that can be used in symbolic expressions
"""

import sympy
from sympy.functions import *
from sympy import S

class wherePositive(sympy.Function):
    """Returns:
         1 where expr > 0
         0 else
    """
    nargs = 1
    is_bounded = True
    is_negative = False
    is_real = True

    @classmethod
    def eval(cls, arg):
        if arg is S.NaN:
            return S.NaN
        if arg.is_positive: return S.One
        if arg.is_negative or arg is S.Zero: return S.Zero
        if arg.is_Function:
            if arg.func is wherePositive: return arg
            if arg.func is whereNegative: return arg

    def _eval_conjugate(self):
        return self

    def _eval_derivative(self, x):
        return S.Zero

class whereNonPositive(sympy.Function):
    """Returns:
         0 where expr > 0
         1 else
    """
    nargs = 1
    is_bounded = True
    is_negative = False
    is_real = True

    @classmethod
    def eval(cls, arg):
        return 1-wherePositive(arg)

    def _eval_conjugate(self):
        return self

    def _eval_derivative(self, x):
        return S.Zero

class whereNegative(sympy.Function):
    """Returns:
         1 where expr < 0
         0 else
    """
    nargs = 1
    is_bounded = True
    is_negative = False
    is_real = True

    @classmethod
    def eval(cls, arg):
        if arg is S.NaN:
            return S.NaN
        if arg.is_nonnegative: return S.Zero
        if arg.is_negative: return S.One
        if arg.is_Function:
            if arg.func is wherePositive: return S.Zero

    def _eval_conjugate(self):
        return self

    def _eval_derivative(self, x):
        return S.Zero

class whereNonNegative(sympy.Function):
    """Returns:
         0 where expr < 0
         1 else
    """
    nargs = 1
    is_bounded = True
    is_negative = False
    is_real = True

    @classmethod
    def eval(cls, arg):
        return 1-whereNegative(arg)

    def _eval_conjugate(self):
        return self

    def _eval_derivative(self, x):
        return S.Zero

class whereZero(sympy.Function):
    """Returns:
         1 where expr == 0
         0 else
    """
    nargs = 1
    is_bounded = True
    is_negative = False
    is_real = True

    @classmethod
    def eval(cls, arg):
        if arg is S.NaN:
            return S.NaN
        if arg.is_zero: return S.One
        if arg.is_nonzero: return S.Zero
        if arg.is_Function:
            if arg.func is whereZero: return 1-arg

    def _eval_conjugate(self):
        return self

    def _eval_derivative(self, x):
        return S.Zero

class whereNonZero(sympy.Function):
    """Returns:
         0 where expr == 0
         1 else
    """
    nargs = 1
    is_bounded = True
    is_negative = False
    is_real = True

    @classmethod
    def eval(cls, arg):
        return 1-whereZero(arg)

    def _eval_conjugate(self):
        return self

    def _eval_derivative(self, x):
        return S.Zero

class log10(sympy.Function):
    """Returns the base-10 logarithm of the argument (same as log(x,10))
    """
    nargs = 1

    @classmethod
    def eval(cls, arg):
        from sympy.functions.elementary.exponential import log
        return log(arg,10)

class inverse(sympy.Function):
    """Returns the inverse of the argument
    """
    nargs = 1

    @classmethod
    def eval(cls, arg):
        if isinstance(arg,sympy.Basic):
            if arg.is_Number:
                return 1./arg

class minval(sympy.Function):
    """Returns the minimum value over all components of the argument
    """
    nargs = 1

    @classmethod
    def eval(cls, arg):
        if isinstance(arg,sympy.Basic):
            if arg.is_Number:
                return arg

class maxval(sympy.Function):
    """Returns the maximum value over all components of the argument
    """
    nargs = 1

    @classmethod
    def eval(cls, arg):
        if isinstance(arg,sympy.Basic):
            if arg.is_Number:
                return arg

class maximum(sympy.Function):
    """Returns the maximum over the arguments
    """
    pass

class minimum(sympy.Function):
    """Returns the minimum over the arguments
    """
    pass

class integrate(sympy.Function):
    """Returns the integral of the argument
    """
    nargs = (1,2)

class interpolate(sympy.Function):
    """Returns the argument interpolated on the function space provided
    """
    nargs = 2

class L2(sympy.Function):
    """Returns the L2 norm of the argument
    """
    nargs = 1

class clip(sympy.Function):
    """Returns the argument clipped to a minimum and maximum value
    """
    nargs = (1,2,3)

class trace(sympy.Function):
    """Returns the trace of the argument with optional axis_offset
    """
    nargs = (1,2)

class transpose(sympy.Function):
    """Returns the transpose of the argument
    """
    nargs = (1,2)

class symmetric(sympy.Function):
    """Returns the symmetric part of the argument
    """
    nargs = 1

    @classmethod
    def eval(cls, arg):
        if isinstance(arg,sympy.Basic):
            if arg.is_Function:
                if arg.func is symmetric: return arg
                if arg.func is nonsymmetric: return S.Zero
            elif arg.is_Number:
                return arg

class nonsymmetric(sympy.Function):
    """Returns the non-symmetric part of the argument
    """
    nargs = 1

    @classmethod
    def eval(cls, arg):
        if isinstance(arg,sympy.Basic):
            if arg.is_Function:
                if arg.func is nonsymmetric: return arg
                if arg.func is symmetric: return S.Zero
            elif arg.is_Number:
                return arg

class swap_axes(sympy.Function):
    """Returns the 'swap' of the argument
    """
    nargs = (1,2,3)

class grad(sympy.Function):
    """Returns the spatial gradient of the argument
    """
    nargs = (1,2)

class inner(sympy.Function):
    """Returns the inner product of the arguments
    """
    nargs = 2

class outer(sympy.Function):
    """Returns the outer product of the arguments
    """
    nargs = 2

class eigenvalues(sympy.Function):
    """Returns the Eigenvalues of the argument
    """
    nargs = 1

class eigenvalues_and_eigenvectors(sympy.Function):
    """Returns the Eigenvalues and Eigenvectors of the argument
    """
    nargs = 1

#
# vim: expandtab shiftwidth=4:
