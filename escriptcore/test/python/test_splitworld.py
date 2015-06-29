##############################################################################
#
# Copyright (c) 2015 by The University of Queensland
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

__copyright__="""Copyright (c) 2015 by The University of Queensland
http://www.uq.edu.au
Primary Business: Queensland, Australia"""
__license__="""Licensed under the Open Software License version 3.0
http://www.opensource.org/licenses/osl-3.0.php"""
__url__="https://launchpad.net/escript-finley"

"""
Tests to ensure that splitworld features operate correctly
"""

import esys.escriptcore.utestselect as unittest
from esys.escript import *

from esys.escriptcore.splitworld import *
from esys.escript.linearPDEs import Poisson, Helmholtz
from esys.escriptcore.testing import *
import sys

mpisize=getMPISizeWorld()

def f1(self, **args):
    x=Data(1, Function(self.domain))
    self.exportValue('v_data',x)
    self.exportValue('v_scalar', 1)
    
def f2(self, **kwargs):
    x=self.importValue('v_data')
    z=self.importValue('v_scalar')
    b=kwargs['expected']
    if abs(z-b)>0.001:
        raise RuntimeError("Scalar value did not match expected value")
    if abs(Lsup(x)-b)>0.001:
        print("x=",str(x)," b=",str(b), file=sys.stderr)
        raise RuntimeError("Data value did not match expected value")

def f3(self, **kwargs):
    print(";;;;;;", file=sys.stderr)
    x=self.importValue('v_data')
    z=self.importValue('v_scalar')
    print("Data=", str(x), file=sys.stderr)
    print("Scal=", str(z), file=sys.stderr)
    

def poisson_work(self, **args):
    x = self.domain.getX()
    gammaD = whereZero(x[0])+whereZero(x[1])
    mypde = Poisson(domain=self.domain)
    mypde.setValue(f=1+self.swid,q=gammaD)
    u = mypde.getSolution()
    return True

def set_var(self, **kwargs):
    self.exportValue("v_scalar", 7)

def inp_var(self, **kwargs):
    self.importValue("v_scalar")    
    
def sum_work(self, **args):
    x=self.domain.getX()
    id=self.jobid
    x=x*self.jobid
    self.exportValue("v_scalar", id)
    self.exportValue("v_data", x)
    
def sum_check(self, **args):
    high=args["high"]
    low=args["low"]
    x=self.domain.getX()
    dtot=0
    stot=0
    for i in range(low, high+1):
        stot+=i
        dtot+=x*i
    sactual=self.importValue("v_scalar")
    dactual=self.importValue("v_data")
    if abs(sactual-stot)>0.001:
        raise RuntimeError("Scalar total is not as expected %e vs %e"%(sactual, stot))
    if Lsup(dactual-dtot)>0.001:
        print("Actual:"+str(dactual))
        print("calced:"+str(dtot))
        raise RuntimeError("Data total is not as expected")

        
def var_setup(self, **kwargs):
    z=1
    x=Data(1, Function(self.domain))
    self.exportValue("v_scalar", z)
    self.exportValue("v_data", x)
    self.exportValue("v_list", [1])

def var_increment(self, **kwargs):
    z=self.importValue("v_scalar")
    x=self.importValue("v_data")
    l=self.importValue("v_list")
    z+=1
    x+=1
    l.append([2])
    self.exportValue("v_scalar", z)
    self.exportValue("v_data", x)
    self.exportValue("v_list", l)
    
def var_check(self, **kwargs):
    zc=self.importValue("v_scalar_copy")
    xc=self.importValue("v_data_copy")
    lc=self.importValue("v_list_copy")
    z=self.importValue("v_scalar")
    x=self.importValue("v_data")
    l=self.importValue("v_list")
    if abs(z-zc)<0.001:
        raise RuntimeError("Scalar variables appear to be incorrectly linked.")
    if Lsup(x-xc)<0.001:
        raise RuntimeError("Data variables appear to be incorrectly linked.")
    if l!=lc:
        raise RuntimeError("Python list appears not to linked.")

class sw_testing(unittest.TestCase):
    
    def create_singleworld(self):
        sw=SplitWorld(1)    
        buildDomains(sw,self.domain_ctr, *self.domain_vec, **self.domain_dict)
        return sw
    
    # This is to test multiple subworlds
    def create_twoworlds(self):
        sw=SplitWorld(2)
        buildDomains(sw,self.domain_ctr, *self.domain_vec, **self.domain_dict)
        return sw

      
    def create_many_subworlds(self):
        sw=SplitWorld(getMPISizeWorld())
        buildDomains(sw,self.domain_ctr, *self.domain_vec, **self.domain_dict)
        return sw
        

    def set_tester(self, sw):
        import time
        #time.sleep(20)
        addVariable(sw, "v_scalar", makeScalarReducer, "SET")
        addVariable(sw, "v_data", makeDataReducer, "SET")
        addVariable(sw, "v_list", makeLocalOnly)    # so we can use var_setup
        addVariable(sw, "ex", makeScalarReducer, "SUM")         # So we have something to read when the others are wiped out

        def ex_set(self, **kwargs):
            self.exportValue("ex",7)

        addJob(sw, FunctionJob, ex_set)
        addJob(sw, FunctionJob, var_setup)
        sw.runJobs()

        if sw.getSubWorldCount()>1:
            addJobPerWorld(sw, FunctionJob, var_setup)
            sw.runJobs()
            self.assertRaises(RuntimeError, sw.getDoubleVariable, "v_scalar")
            self.assertRaises(RuntimeError, sw.getDoubleVariable, "v_scalar")

        addJob(sw, FunctionJob, var_setup)
        addJob(sw, FunctionJob, var_setup)
        if sw.getSubWorldCount()==1:
            self.assertRaises(RuntimeError, sw.runJobs)
        else:
            sw.runJobs()
            self.assertRaises(RuntimeError, sw.runJobs) # This gives up after the first dud resolve
            self.assertRaises(RuntimeError, sw.runJobs) # since we have multiple vars we need to flush
        print(sw.getVarList())
        sw.getDoubleVariable("ex")

        addJob(sw, FunctionJob, var_setup)
        sw.runJobs()
        
    def sum_vars_tester(self, sw):
        addVariable(sw, "v_scalar", makeScalarReducer, "SUM")
        addVariable(sw, "v_data", makeDataReducer, "SUM")
        addVariable(sw, "notused", makeLocalOnly)
        flags1=[['notused', False], ['v_data', False], ['v_scalar', False]]
        self.assertEqual(flags1, sw.getVarList())
        lim=2*getMPISizeWorld()
        for i in range(1,lim+1):
          addJob(sw, FunctionJob, sum_work)
        sw.runJobs()
        flags2=[['notused', False], ['v_data', True], ['v_scalar', True]]

        self.assertEqual(flags2, sw.getVarList())
        addJob(sw, FunctionJob, sum_check, imports=['v_scalar', 'v_data'], low=1, high=lim)
        sw.runJobs()
        total=0
        for i in range(1, lim+1):
            total+=i
        act=sw.getDoubleVariable("v_scalar")
        self.assertEqual(total, act, "Extract of double variable failed")
        sw.removeVariable("v_scalar")
        self.assertEqual([['notused', False], ['v_data', True]], sw.getVarList())
        self.assertRaises(RuntimeError, sw.getDoubleVariable, "v_scalar")
        
        addJobPerWorld(sw, FunctionJob, set_var)
        self.assertRaises(RuntimeError, sw. runJobs)
        
        addJobPerWorld(sw, FunctionJob, inp_var)
        self.assertRaises(RuntimeError, sw. runJobs)
        
        addVariable(sw, "v_scalar", makeScalarReducer, "SUM")
        flags3=[['notused', False], ['v_data', True], ['v_scalar', False]]
        self.assertEqual(flags3, sw.getVarList())
        
        addJob(sw, FunctionJob, set_var)        # note that this will only set the value in one world
        sw.runJobs()                            # want to test if getDouble is transporting values        
        self.assertEqual(7, sw.getDoubleVariable("v_scalar"))    
        
        
    def copy_vars_tester(self, sw):
        addVariable(sw, "v_scalar", makeScalarReducer, "SUM")
        addVariable(sw, "v_data", makeDataReducer, "SUM")
        addVariable(sw, "v_list", makeLocalOnly)
        addVariable(sw, "v_scalar_copy", makeScalarReducer, "SUM")
        addVariable(sw, "v_data_copy", makeDataReducer, "SUM")
        addVariable(sw, "v_list_copy", makeLocalOnly)
        addJobPerWorld(sw, FunctionJob, var_setup)
        sw.runJobs()
        sw.copyVariable("v_scalar", "v_scalar_copy")
        sw.copyVariable("v_data", "v_data_copy")
        sw.copyVariable("v_list", "v_list_copy")
        self.assertRaises(RuntimeError, sw.copyVariable, "v_scalar", "v_data_copy")
        self.assertRaises(RuntimeError, sw.copyVariable, "v_scalar", "v_list_copy")
        self.assertRaises(RuntimeError, sw.copyVariable, "v_data", "v_scalar_copy")
        self.assertRaises(RuntimeError, sw.copyVariable, "v_data", "v_list_copy")
        self.assertRaises(RuntimeError, sw.copyVariable, "v_list", "v_data_copy")
        self.assertRaises(RuntimeError, sw.copyVariable, "v_list", "v_scalar_copy")
        self.assertRaises(RuntimeError, sw.copyVariable, "v_data", "v_data")
       
        addJobPerWorld(sw, FunctionJob, var_increment)
        sw.runJobs()
        addJobPerWorld(sw, FunctionJob, var_check)
        sw.runJobs()
        sw.runJobs()    # Just to make sure empty list doesn't break it

#-------------------------------------------  

    def testbigworld_singleround(self):
        sw=self.create_singleworld()
        addJob(sw, FunctionJob, poisson_work) 
        sw.runJobs()
        
        sw=self.create_singleworld()
        addJobPerWorld(sw, FunctionJob, poisson_work)
        sw.runJobs()
        
        sw=self.create_singleworld()
        for i in range(4):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()
        
    def testbigworld_multiround(self):        
        sw=self.create_singleworld()
        for i in range(4*getMPISizeWorld()):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()
        for i in range(2):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()
        for i in range(3*getMPISizeWorld()+1):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()
        
    def testbigworld_sum_vars(self):
        sw=self.create_singleworld()
        self.sum_vars_tester(sw) 
        
    def testbigworld_copy_vars(self):
        sw=self.create_singleworld()
        self.copy_vars_tester(sw)

        
    def testbigworld_set_vars(self):
        sw=self.create_singleworld()
        self.set_tester(sw)

#--------------------------------------------------
    @unittest.skipIf(mpisize%2!=0, "test only fires for even numbers of processes")
    def test2world_singleround(self):
        sw=self.create_twoworlds()
        addJob(sw, FunctionJob, poisson_work) 
        sw.runJobs()
        
        sw=self.create_twoworlds()
        addJobPerWorld(sw, FunctionJob, poisson_work)
        sw.runJobs()
        
        sw=self.create_twoworlds()
        for i in range(4):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()

       
    @unittest.skipIf(mpisize%2!=0, "test only fires for even numbers of processes")   
    def test2world_multiround(self):        
        sw=self.create_twoworlds()
        for i in range(4*getMPISizeWorld()):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()
        for i in range(2):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()
        for i in range(3*getMPISizeWorld()+1):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()

    @unittest.skipIf(mpisize%2!=0, "test only fires for even numbers of processes")
    def test2world_sum_vars(self):
        sw=self.create_twoworlds()
        self.sum_vars_tester(sw) 

    @unittest.skipIf(mpisize%2!=0, "test only fires for even numbers of processes")    
    def test2world_copy_vars(self):
        sw=self.create_twoworlds()
        self.copy_vars_tester(sw)        

    @unittest.skipIf(mpisize%2!=0, "test only fires for even numbers of processes")
    def test2world_set_vars(self):
        sw=self.create_twoworlds()
        self.set_tester(sw)
#------------------------------------------------         

    @unittest.skipIf(mpisize<3, "test is redundant on fewer than three processes")
    def testmanyworld_singleround(self):
        sw=self.create_many_subworlds()
        addJob(sw, FunctionJob, poisson_work) 
        sw.runJobs()
        
        sw=self.create_many_subworlds()
        addJobPerWorld(sw, FunctionJob, poisson_work)
        sw.runJobs()
        
        sw=self.create_many_subworlds()
        for i in range(4):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()        
        
    @unittest.skipIf(mpisize<3, "test is redundant on fewer than three processes")
    def testmanyworld_multiround(self):        
        sw=self.create_many_subworlds()
        for i in range(4*getMPISizeWorld()):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()
        for i in range(2):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()
        for i in range(3*getMPISizeWorld()+1):
            addJob(sw, FunctionJob, poisson_work)
        sw.runJobs()

    @unittest.skipIf(mpisize<3, "test is redundant on fewer than three processes")        
    def testmanyworld_sum_vars(self):
        sw=self.create_many_subworlds()
        self.sum_vars_tester(sw) 
        
        
    @unittest.skipIf(mpisize<3, "test is redundant on fewer than three processes")        
    def testmanyworld_copy_vars(self):
        sw=self.create_many_subworlds()
        self.copy_vars_tester(sw)         
        
    @unittest.skipIf(mpisize<3, "test is redundant on fewer than three processes")        
    def testmanyworld_partial_reduce(self):
        sw=self.create_many_subworlds()
        addVariable(sw, 'v_scalar', makeScalarReducer, "SUM")
        addVariable(sw, 'v_data', makeDataReducer, "SUM")
        addJob(sw, FunctionJob, f1)
        sw.runJobs()    # only one world has the value
                # value=1
        addJobPerWorld(sw, FunctionJob, f2, expected=1, imports=['v_data']) # can everyone get the correct value
        sw.runJobs()
            # now we change some of the values (we know we have at least 3 worlds)
        addJob(sw, FunctionJob, f1)
        addJob(sw, FunctionJob, f1)
        sw.runJobs()
        addJobPerWorld(sw, FunctionJob, f2, expected=2) # can everyone get the correct value
        sw.runJobs()
            # Now we try the same with a clean start
        sw.clearVariable('v_data')
        sw.clearVariable('v_scalar')
        addJob(sw, FunctionJob, f1)
        addJob(sw, FunctionJob, f1)
        sw.runJobs()
        addJobPerWorld(sw, FunctionJob, f2, expected=2) # can everyone get the correct value
        sw.runJobs()
        
        
    @unittest.skipIf(mpisize<3, "test is redundant on fewer than three processes")        
    def testmanyworld_set_vars(self):
        sw=self.create_many_subworlds()
        self.set_tester(sw)
#------------------------------------------------         

    def test_illegal_ws(self):
        self.assertRaises(RuntimeError, SplitWorld, getMPISizeWorld()+1)




class Test_SplitWorld(unittest.TestCase):
  """
  Class to test splitworld functions.
  Requires subclasses to supply self.domainpars which is a list of constructor function followed
  by arguments.
  eg:  if your domain is created with Rectangle(3,4), then your domainpars would be [Rectangle,3,4]
  """
  
  
  class PoissonJob1(Job):
    def __init__(self, **kwargs):
      super(PoissonJob1, self).__init__(**kwargs)
    
    def work(self):
      x = self.domain.getX()
      gammaD = whereZero(x[0])+whereZero(x[1])
      # define PDE and get its solution u
      mypde = Poisson(domain=self.domain)
      mypde.setValue(f=1, q=gammaD)
      u = mypde.getSolution()
      self.exportValue("answer", Lsup(u))
      return True

  class PoissonJob(Job):
    def __init__(self, **kwargs):
      super(Test_SplitWorld.PoissonJob, self).__init__(**kwargs)
    
    def work(self):
      x = self.domain.getX()
      gammaD = whereZero(x[0])+whereZero(x[1])
      # define PDE and get its solution u
      mypde = Poisson(domain=self.domain)
      mypde.setValue(f=self.jobid, q=gammaD)
      u = Lsup(mypde.getSolution())   # we won't actually export the value to make
      self.exportValue("answer", self.jobid) # testing easier
      return True
      
  class HelmholtzJob(Job):
    def __init__(self, **kwargs):
      super(Test_SplitWorld.HelmholtzJob, self).__init__(**kwargs)
    
    def work(self):
      # define PDE and get its solution u
      mypde = Helmholtz(domain=self.domain)
      mypde.setValue(omega=self.jobid)
      u = mypde.getSolution()
      self.exportValue("hanswer", 2*self.jobid)
      self.exportValue("v", self.jobid)
      return True
      
  class InjectJob(Job):
    """
    Tests jobs taking parameters
    """
    def __init__(self, **kwargs):
      super(Test_SplitWorld.InjectJob, self).__init__(**kwargs)
      self.value=kwargs['val']
      self.name=kwargs['name']
    
    def work(self):
      """
      Make use of values passed to constructor
      """
      self.exportValue(self.name, self.value)
      return True      

  class FactorJob(Job):
    """
    Tests jobs taking parameters
    """
    def __init__(self, **kwargs):
      super(Test_SplitWorld.FactorJob, self).__init__(**kwargs)
      self.divisor=kwargs['fact']
    
    def work(self):
      """
      Make use of values passed to constructor
      """
      z=self.importValue("value")
      if (z%self.divisor==0):
          self.exportValue("boolean", self.divisor)
      return True 
      
      
  class ThrowJob(Job):
    """
    Trigger various faults
    """
    def __init__(self, **kwargs):
      super(Test_SplitWorld.ThrowJob, self).__init__(**kwargs)
      self.faultnum=kwargs['fault']             #leaving this out will test error in constructor
      
    def work(self):
      if self.faultnum==1:
        return "zero"           # non-boolean return value
      if self.faultnum==2:
        z=self.importValue("missing")   # unannounced import
        return True
      if self.faultnum==3:
        self.exportValue("missing",0)   # undeclared
        return True
      if self.faultnum==4:
        self.exportValue("answer","answer")  # type-mismatch in export
      return True

  class DummyJob(Job):
    """
    Trigger various faults
    """
    def __init__(self, **kwargs):
      super(Test_SplitWorld.DummyJob, self).__init__(**kwargs)
      
    def work(self):
      return True      
      
      
  def test_faults(self):
      for x in range(1,5):
        sw=SplitWorld(getMPISizeWorld())
        buildDomains(sw,*self.domainpars)
        addVariable(sw, "answer", makeScalarReducer, "MAX") 
        addJob(sw, Test_SplitWorld.ThrowJob, fault=x)
        self.assertRaises(RuntimeError, sw.runJobs)

  @unittest.skipIf(getMPISizeWorld()>97, "Too many ranks for this test")
  def test_factorjobs(self):
      """
      test importing, multiple phases, max as a flag
      """
      sw=SplitWorld(getMPISizeWorld())
      buildDomains(sw,*self.domainpars)
      addVariable(sw, "value", makeScalarReducer, "MAX")
      addVariable(sw, "boolean", makeScalarReducer, "MAX")
         # first we will load in a value to factorise
         # Don't run this test with 99 or more processes
      addJob(sw, Test_SplitWorld.InjectJob, name='value', val=101)      # Feed it a prime  
      addJob(sw, Test_SplitWorld.InjectJob, name='boolean', val=0)              # so we have a value
      sw.runJobs()
      for x in range(2,getMPISizeWorld()+2):
        addJob(sw, Test_SplitWorld.FactorJob, fact=x)
      sw.runJobs()
      self.assertEquals(sw.getDoubleVariable('boolean'),0)
      sw.clearVariable('value')
      sw.clearVariable('boolean')
      addJob(sw, Test_SplitWorld.InjectJob, name='value', val=101)      # Feed it a prime  
      addJob(sw, Test_SplitWorld.InjectJob, name='boolean', val=0)              # so we have a value
      sw.runJobs()
      sw.clearVariable("value")
      
        # Now test with a value which has a factor
      addJob(sw, Test_SplitWorld.InjectJob, name='value', val=100)       # Feed it a prime  
      addJob(sw, Test_SplitWorld.InjectJob, name='boolean', val=0)               # so we have a value
      sw.runJobs()
      m=0
      for x in range(2,getMPISizeWorld()+2):
        addJob(sw, Test_SplitWorld.FactorJob, fact=x)
        if 100%x==0:
          m=x
      sw.runJobs()
      self.assertEquals(sw.getDoubleVariable('boolean'),m)      
      
  def test_split_simple_solve(self):
    """
    Solve a single equation
    """
    sw=SplitWorld(getMPISizeWorld())
    buildDomains(sw,*self.domainpars)
    addVariable(sw, "answer", makeScalarReducer, "SUM")
    addJob(sw, Test_SplitWorld.PoissonJob)
    sw.runJobs()
    self.assertEquals(sw.getDoubleVariable("answer"),1)
    
  def test_split_simple_solve_multiple(self):
    """
    Solve a number of the same equation in one batch
    """
    sw=SplitWorld(getMPISizeWorld())
    buildDomains(sw,*self.domainpars)
    addVariable(sw, "answer", makeScalarReducer, "SUM")
        # this gives us 1 job per world
    total=0
    jobid=1
    for x in range(0,getMPISizeWorld()):
        addJob(sw, Test_SplitWorld.PoissonJob)
        total+=jobid
        jobid+=1
    sw.runJobs()
    self.assertEquals(sw.getDoubleVariable("answer"), total)
    
  def test_split_simple_and_dummy(self):
    """
    Solve a number of the same equation with some worlds doing dummy Jobs
    """
    sw=SplitWorld(getMPISizeWorld())
    buildDomains(sw,*self.domainpars)
    addVariable(sw, "answer", makeScalarReducer, "SUM")
        # this gives us 1 job per world
    total=0
    mid=getMPISizeWorld()//2
    if getMPISizeWorld()%2==1:
      mid=mid+1
    for x in range(0,mid):
        addJob(sw, Test_SplitWorld.PoissonJob)
        total=total+(x+1)
    for x in range(0,mid):
        addJob(sw, Test_SplitWorld.DummyJob)
    sw.runJobs()
      # expecting this to fail until I work out the answer
    self.assertEqual(sw.getDoubleVariable("answer"), total)
    
  def test_split_simple_and_empty(self):
    """
    Solve a number of the same equation with some worlds doing nothing
    """
    sw=SplitWorld(getMPISizeWorld())
    buildDomains(sw, *self.domainpars)
    addVariable(sw, "answer", makeScalarReducer, "SUM")
        # this gives us at most 1 job per world
    total=0    
    mid=getMPISizeWorld()//2
    if getMPISizeWorld()%2==1:
      mid=mid+1    
    for x in range(0,mid):
        addJob(sw, Test_SplitWorld.PoissonJob)
        total=total+(x+1)
    sw.runJobs()
      # expecting this to fail until I work out the answer
    self.assertEquals(sw.getDoubleVariable("answer"),total)    
    
    
  def test_split_multiple_batches(self):
    """
    Solve a number of the same equation in multiple batches
    """
    sw=SplitWorld(getMPISizeWorld())
    buildDomains(sw,*self.domainpars)
    addVariable(sw, "answer", makeScalarReducer, "SUM")
        # this gives us 1 job per world
    total=0
    sw.runJobs()
    for x in range(0,getMPISizeWorld()):
        addJob(sw, Test_SplitWorld.PoissonJob)
        total=total+x
    sw.runJobs()
    sw.runJobs()
    sw.clearVariable("answer")
    total=0
    for x in range(0,getMPISizeWorld()):
        addJob(sw, Test_SplitWorld.PoissonJob)
        total=total+(x+1+getMPISizeWorld())
    sw.runJobs()
      # expecting this to fail until I work out the answer
    self.assertEquals(sw.getDoubleVariable("answer"),total)    
  
  @unittest.skipIf(getMPISizeWorld()%2!=0, "Test requires even number of processes")
  def test_multiple_equations_size2world(self):
    """
    Test two different types of equations to solve mixed in batches
    We will try various combinations to spread them out over the 
    worlds in different patterns.
    This version attempts this with worlds of size 2
    """
    wc=getMPISizeWorld()//2
    sw=SplitWorld(wc)
    buildDomains(sw, *self.domainpars)
    addVariable(sw, "answer", makeScalarReducer, "SUM")   
    addVariable(sw, "hanswer", makeScalarReducer, "SUM")  
    addVariable(sw, "v", makeScalarReducer, "MAX")
    
    tot=0
    jobid=1
       #first put jobs of the same type close.
    for x in range(0, max(wc//3,1)):
      addJob(sw, Test_SplitWorld.PoissonJob)
      jobid+=1
    for x in range(0, max(wc//3,1)):
      addJob(sw, Test_SplitWorld.HelmholtzJob)
      tot+=2*(jobid)
      jobid+=1
    for x in range(0, max(wc//3,1)):
      addJob(sw, Test_SplitWorld.DummyJob)
      jobid+=1
    sw.runJobs()
    ha=sw.getDoubleVariable("hanswer")
    self.assertEquals(ha, tot)
    sw.clearVariable("answer")
    sw.clearVariable("hanswer")
    sw.clearVariable("v")
    tot=0
      # similar but separated by dummy Jobs
    for x in range(0, max(wc//3,1)):
      addJob(sw, Test_SplitWorld.PoissonJob)
      jobid+=1
    for x in range(0, max(wc//3,1)):
      addJob(sw, Test_SplitWorld.DummyJob)      
      jobid+=1
    for x in range(0, max(wc//3,1)):
      addJob(sw, Test_SplitWorld.HelmholtzJob)
      tot+=2*jobid
      jobid+=1
    sw.runJobs()
    ha=sw.getDoubleVariable("hanswer")
    self.assertEquals(ha, tot)
    sw.clearVariable("answer")
    sw.clearVariable("hanswer")
    sw.clearVariable("v")   
      # mixed
    tot=0
    for x in range(0, max(wc//2,1)):
      addJob(sw, Test_SplitWorld.HelmholtzJob)
      tot+=2*jobid
      addJob(sw, Test_SplitWorld.DummyJob)
      jobid+=2
      addJob(sw, Test_SplitWorld.PoissonJob)
      jobid+=1
    sw.runJobs()
    ha=sw.getDoubleVariable("hanswer")
    self.assertEquals(ha, tot)    

  @unittest.skipIf(getMPISizeWorld()%4!=0, "Test requires number of processes divisible by 4")
  def test_multiple_equations_size4world(self):
    """
    Test two different types of equations to solve mixed in batches
    We will try various combinations to spread them out over the 
    worlds in different patterns.
    This version attempts this with worlds of size 2
    """
    wc=getMPISizeWorld()//4
    sw=SplitWorld(wc)
    buildDomains(sw,*self.domainpars)
    addVariable(sw, "answer", makeScalarReducer, "SUM")   
    addVariable(sw, "hanswer", makeScalarReducer, "SUM")  
    addVariable(sw, "v", makeScalarReducer, "MAX")
    
    jobid=1
    tot=0
       #first put jobs of the same type close.
    for x in range(0, max(wc//2,1)):
      addJob(sw, Test_SplitWorld.PoissonJob)
      jobid+=1
    for x in range(0, max(wc//2,1)):
      addJob(sw, Test_SplitWorld.HelmholtzJob)
      tot+=2*jobid
      jobid+=1      
    for x in range(0, max(wc//2,1)):
      addJob(sw, Test_SplitWorld.DummyJob)
      jobid+=1
    sw.runJobs()
    ha=sw.getDoubleVariable("hanswer")
    self.assertEquals(ha, tot)
    sw.clearVariable("answer")
    sw.clearVariable("hanswer")
    sw.clearVariable("v")
    tot=0
      # similar but separated by dummy Jobs
    for x in range(0, max(wc//2,1)):
      addJob(sw, Test_SplitWorld.PoissonJob)
      jobid+=1      
    for x in range(0, max(wc//2,1)):
      addJob(sw, Test_SplitWorld.DummyJob) 
      jobid+=1     
    for x in range(0, max(wc//2,1)):
      addJob(sw, Test_SplitWorld.HelmholtzJob)
      tot+=2*jobid
      jobid+=1
    sw.runJobs()
    ha=sw.getDoubleVariable("hanswer")
    self.assertEquals(ha, tot)
    sw.clearVariable("answer")
    sw.clearVariable("hanswer")
    sw.clearVariable("v")   
    tot=0
      # mixed
    for x in range(0, max(wc//2,1)):
      addJob(sw, Test_SplitWorld.HelmholtzJob)
      tot+=2*jobid
      jobid+=1
      addJob(sw, Test_SplitWorld.DummyJob)
      addJob(sw, Test_SplitWorld.PoissonJob)
      jobid+=2
    sw.runJobs()
    ha=sw.getDoubleVariable("hanswer")
    self.assertEquals(ha, tot)        
    
    
  def test_multiple_equations_smallworld(self):
    """
    Test two different types of equations to solve mixed in batches
    We will try various combinations to spread them out over the 
    worlds in different patterns
    """
    sw=SplitWorld(getMPISizeWorld())
    buildDomains(sw,*self.domainpars)
    addVariable(sw, "answer", makeScalarReducer, "SUM")   
    addVariable(sw, "hanswer", makeScalarReducer, "SUM")  
    addVariable(sw, "v", makeScalarReducer, "MAX")
    
    tot=0
    jobid=1
       #first put jobs of the same type close together.
    for x in range(0,max(getMPISizeWorld()//3,1)):
      addJob(sw, Test_SplitWorld.PoissonJob)
      jobid+=1
    for x in range(0,max(getMPISizeWorld()//3,1)):
      addJob(sw, Test_SplitWorld.HelmholtzJob)
      tot+=2*jobid
      jobid+=1
    for x in range(0,getMPISizeWorld()//3):
      addJob(sw, Test_SplitWorld.DummyJob)
      jobid+=1
    sw.runJobs()
    ha=sw.getDoubleVariable("hanswer")
    self.assertEquals(ha, tot)
    sw.clearVariable("answer")
    sw.clearVariable("hanswer")
    sw.clearVariable("v")
    tot=0
      # similar but separated by dummy Jobs
    for x in range(0,max(getMPISizeWorld()//3,1)):
      addJob(sw, Test_SplitWorld.PoissonJob)
      jobid+=1
    for x in range(0,getMPISizeWorld()//3):
      addJob(sw, Test_SplitWorld.DummyJob)      
      jobid+=1      
    for x in range(0,max(getMPISizeWorld()//3,1)):
      addJob(sw, Test_SplitWorld.HelmholtzJob)
      tot+=2*jobid
      jobid+=1      
    sw.runJobs()
    ha=sw.getDoubleVariable("hanswer")
    self.assertEquals(ha, tot)
    sw.clearVariable("answer")
    sw.clearVariable("hanswer")
    sw.clearVariable("v")   
    tot=0
      # mixed
    for x in range(0, max(getMPISizeWorld()//2,1)):
      addJob(sw, Test_SplitWorld.HelmholtzJob)
      tot+=jobid*2
      addJob(sw, Test_SplitWorld.DummyJob)
      addJob(sw, Test_SplitWorld.PoissonJob)
      jobid+=3
    sw.runJobs()
    ha=sw.getDoubleVariable("hanswer")
    self.assertEquals(ha, tot)     
