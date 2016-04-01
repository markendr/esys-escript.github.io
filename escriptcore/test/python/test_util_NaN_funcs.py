
##############################################################################
#
# Copyright (c) 2003-2016 by The University of Queensland
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

#here be nan tests
import esys.escript as es
import esys.escriptcore.utestselect as unittest

class Test_util_NaN_funcs(unittest.TestCase):
    RES_TOL=1.e-7 # RES_TOLerance to compare results
    DIFF_TOL=1.e-7 # RES_TOLerance to derivatives

    def test_replaceNaNExpanded(self):
        dom=self.domain
        scl=es.Scalar(0,es.ContinuousFunction(dom))
        scl.expand()
        sclNaN=scl/0
        self.assertTrue(sclNaN.hasNaN(),"sclNaN should contain NaN but its doesn't")
        sclNaN.replaceNaN(15.0)
        self.assertEqual(es.Lsup(sclNaN), 15.0)
    
    def test_replaceNaNConstant(self):
        dom=self.domain
        dat = es.Data(10,es.ContinuousFunction(dom))
        dat=(dat*0)/0
        self.assertTrue(dat.hasNaN(),"dat should contain NaN but its doesn't")
        dat.replaceNaN(10)
        self.assertEqual(es.Lsup(dat), 10)

    def test_replaceNaNTagged(self):
        dom=self.domain
        sigma = es.Scalar(0,es.FunctionOnBoundary(dom))
        dat=(sigma*0)/0
        sigma.setTaggedValue(1 , es.Lsup(dat))
        sigma.replaceNaN(10)
        self.assertEqual(es.Lsup(sigma), 10)
