#/usr/bin/python
# $Id:$

#
#      COPYRIGHT ACcESS 2004 -  All Rights Reserved
#
#   This software is the property of ACcESS.  No part of this code
#   may be copied in any form or by any means without the expressed written
#   consent of ACcESS.  Copying, use or modification of this software
#   by any unauthorised person is illegal unless that
#   person has a software license agreement with ACcESS.
#

"""
some benchmarks for tetsing the finley solver.

@var __author__: name of author
@var __licence__: licence agreement
var __url__: url entry point on documentation
@var __version__: version
@var __date__: date of the version
"""

__author__="Lutz Gross, l.gross@uq.edu.au"
__licence__="contact: esys@access.uq.edu.au"
__url__="http://www.iservo.edu.au/esys/escript"
__version__="$Revision:$"
__date__="$Date:$"

from esys.finley.finleybench import *
from esys.escript.benchmark import BenchmarkSuite,Benchmark

thlist=[1,2,4,8,16]
# thlist=[1,2,4,8,16,32]
# thlist=[1,2,4,8,16,32,64,128]
# thlist=[1,2,4,8,16,32,64,128]
show=False
ff=FinleyFilter()

opt1=FinleyOptions(solver_method=LinearPDE.PCG,preconditioner=LinearPDE.JACOBI,verbose=show)
opt2=FinleyOptions(solver_method=LinearPDE.PCG,preconditioner=LinearPDE.ILU0,verbose=show)
opt3=FinleyOptions(solver_method=LinearPDE.DIRECT,verbose=show)

bm_L2Do1=Benchmark(name="Laplace 2D (order 1)")
bm_L2Do1.addProblem(Laplace2DOrder1_30k())
bm_L2Do1.addProblem(Laplace2DOrder1_60k())
bm_L2Do1.addProblem(Laplace2DOrder1_120k())
bm_L2Do1.addProblem(Laplace2DOrder1_240k())
bm_L2Do1.addProblem(Laplace2DOrder1_480k())
bm_L2Do1.addProblem(Laplace2DOrder1_960k())
bm_L2Do1.addProblem(Laplace2DOrder1_1920k())
bm_L2Do1.addProblem(Laplace2DOrder1_3840k())
bm_L2Do1.addProblem(Laplace2DOrder1_7680k())
bm_L2Do1.addProblem(Laplace2DOrder1_15360k())
bm_L2Do1.addOptions(opt1)
bm_L2Do1.addOptions(opt2)
bm_L2Do1.addOptions(opt3)

bm_L2Do2=Benchmark("Laplace 2D (order 2)")
bm_L2Do2.addProblem(Laplace2DOrder2_30k())
bm_L2Do2.addProblem(Laplace2DOrder2_60k())
bm_L2Do2.addProblem(Laplace2DOrder2_120k())
bm_L2Do2.addProblem(Laplace2DOrder2_240k())
bm_L2Do2.addProblem(Laplace2DOrder2_480k())
bm_L2Do2.addProblem(Laplace2DOrder2_960k())
bm_L2Do2.addProblem(Laplace2DOrder2_1920k())
bm_L2Do2.addProblem(Laplace2DOrder2_3840k())
bm_L2Do2.addProblem(Laplace2DOrder2_7680k())
bm_L2Do2.addProblem(Laplace2DOrder2_15360k())
bm_L2Do2.addOptions(opt1)
bm_L2Do2.addOptions(opt2)
bm_L2Do2.addOptions(opt3)

bm_L3Do1=Benchmark("Laplace 3D (order 1)")
bm_L3Do1.addProblem(Laplace3DOrder1_30k())
bm_L3Do1.addProblem(Laplace3DOrder1_60k())
bm_L3Do1.addProblem(Laplace3DOrder1_120k())
bm_L3Do1.addProblem(Laplace3DOrder1_240k())
bm_L3Do1.addProblem(Laplace3DOrder1_480k())
bm_L3Do1.addProblem(Laplace3DOrder1_960k())
bm_L3Do1.addProblem(Laplace3DOrder1_1920k())
bm_L3Do1.addProblem(Laplace3DOrder1_3840k())
bm_L3Do1.addProblem(Laplace3DOrder1_7680k())
bm_L3Do1.addProblem(Laplace3DOrder1_15360k())
bm_L3Do1.addOptions(opt1)
bm_L3Do1.addOptions(opt2)
bm_L3Do1.addOptions(opt3)

bm_L3Do2=Benchmark("Laplace 3D (order 2)")
bm_L3Do2.addProblem(Laplace3DOrder2_30k())
bm_L3Do2.addProblem(Laplace3DOrder2_60k())
bm_L3Do2.addProblem(Laplace3DOrder2_120k())
bm_L3Do2.addProblem(Laplace3DOrder2_240k())
bm_L3Do2.addProblem(Laplace3DOrder2_480k())
bm_L3Do2.addProblem(Laplace3DOrder2_960k())
bm_L3Do2.addProblem(Laplace3DOrder2_1920k())
bm_L3Do2.addProblem(Laplace3DOrder2_3840k())
bm_L3Do2.addProblem(Laplace3DOrder2_7680k())
bm_L3Do2.addProblem(Laplace3DOrder2_15360k())
bm_L3Do2.addOptions(opt1)
bm_L3Do2.addOptions(opt2)
bm_L3Do2.addOptions(opt3)

bm_A2Do1g30=Benchmark("Anisotropic 2D (gamma=30, order=1)")
bm_A2Do1g30.addProblem(Anisotropic2DOrder1Gamma30_30k())
bm_A2Do1g30.addProblem(Anisotropic2DOrder1Gamma30_60k())
bm_A2Do1g30.addProblem(Anisotropic2DOrder1Gamma30_120k())
bm_A2Do1g30.addProblem(Anisotropic2DOrder1Gamma30_240k())
bm_A2Do1g30.addProblem(Anisotropic2DOrder1Gamma30_480k())
bm_A2Do1g30.addProblem(Anisotropic2DOrder1Gamma30_960k())
bm_A2Do1g30.addProblem(Anisotropic2DOrder1Gamma30_1920k())
bm_A2Do1g30.addProblem(Anisotropic2DOrder1Gamma30_3840k())
bm_A2Do1g30.addProblem(Anisotropic2DOrder1Gamma30_7680k())
bm_A2Do1g30.addProblem(Anisotropic2DOrder1Gamma30_15360k())

bm_A2Do1g45=Benchmark("Anisotropic 2D (gamma=45, order=1)")
bm_A2Do1g45.addProblem(Anisotropic2DOrder1Gamma45_30k())
bm_A2Do1g45.addProblem(Anisotropic2DOrder1Gamma45_60k())
bm_A2Do1g45.addProblem(Anisotropic2DOrder1Gamma45_120k())
bm_A2Do1g45.addProblem(Anisotropic2DOrder1Gamma45_240k())
bm_A2Do1g45.addProblem(Anisotropic2DOrder1Gamma45_480k())
bm_A2Do1g45.addProblem(Anisotropic2DOrder1Gamma45_960k())
bm_A2Do1g45.addProblem(Anisotropic2DOrder1Gamma45_1920k())
bm_A2Do1g45.addProblem(Anisotropic2DOrder1Gamma45_3840k())
bm_A2Do1g45.addProblem(Anisotropic2DOrder1Gamma45_7680k())
bm_A2Do1g45.addProblem(Anisotropic2DOrder1Gamma45_15360k())

bm_A2Do2g30=Benchmark("Anisotropic 2D (gamma=30, order=2)")
bm_A2Do2g30.addProblem(Anisotropic2DOrder2Gamma30_30k())
bm_A2Do2g30.addProblem(Anisotropic2DOrder2Gamma30_60k())
bm_A2Do2g30.addProblem(Anisotropic2DOrder2Gamma30_120k())
bm_A2Do2g30.addProblem(Anisotropic2DOrder2Gamma30_240k())
bm_A2Do2g30.addProblem(Anisotropic2DOrder2Gamma30_480k())
bm_A2Do2g30.addProblem(Anisotropic2DOrder2Gamma30_960k())
bm_A2Do2g30.addProblem(Anisotropic2DOrder2Gamma30_1920k())
bm_A2Do2g30.addProblem(Anisotropic2DOrder2Gamma30_3840k())
bm_A2Do2g30.addProblem(Anisotropic2DOrder2Gamma30_7680k())
bm_A2Do2g30.addProblem(Anisotropic2DOrder2Gamma30_15360k())


bm_A2Do2g45=Benchmark("Anisotropic 2D (gamma=45, order=2)")
bm_A2Do2g45.addProblem(Anisotropic2DOrder2Gamma45_30k())
bm_A2Do2g45.addProblem(Anisotropic2DOrder2Gamma45_60k())
bm_A2Do2g45.addProblem(Anisotropic2DOrder2Gamma45_120k())
bm_A2Do2g45.addProblem(Anisotropic2DOrder2Gamma45_240k())
bm_A2Do2g45.addProblem(Anisotropic2DOrder2Gamma45_480k())
bm_A2Do2g45.addProblem(Anisotropic2DOrder2Gamma45_960k())
bm_A2Do2g45.addProblem(Anisotropic2DOrder2Gamma45_1920k())
bm_A2Do2g45.addProblem(Anisotropic2DOrder2Gamma45_3840k())
bm_A2Do2g45.addProblem(Anisotropic2DOrder2Gamma45_7680k())
bm_A2Do2g45.addProblem(Anisotropic2DOrder2Gamma45_15360k())


bm_A3Do1g30=Benchmark("Anisotropic 3D (gamma=30, order=1)")
bm_A3Do1g30.addProblem(Anisotropic3DOrder1Gamma30_30k())
bm_A3Do1g30.addProblem(Anisotropic3DOrder1Gamma30_60k())
bm_A3Do1g30.addProblem(Anisotropic3DOrder1Gamma30_120k())
bm_A3Do1g30.addProblem(Anisotropic3DOrder1Gamma30_240k())
bm_A3Do1g30.addProblem(Anisotropic3DOrder1Gamma30_480k())
bm_A3Do1g30.addProblem(Anisotropic3DOrder1Gamma30_960k())
bm_A3Do1g30.addProblem(Anisotropic3DOrder1Gamma30_1920k())
bm_A3Do1g30.addProblem(Anisotropic3DOrder1Gamma30_3840k())
bm_A3Do1g30.addProblem(Anisotropic3DOrder1Gamma30_7680k())
bm_A3Do1g30.addProblem(Anisotropic3DOrder1Gamma30_15360k())

bm_A3Do1g45=Benchmark("Anisotropic 3D (gamma=45, order=1)")
bm_A3Do1g45.addProblem(Anisotropic3DOrder1Gamma45_30k())
bm_A3Do1g45.addProblem(Anisotropic3DOrder1Gamma45_60k())
bm_A3Do1g45.addProblem(Anisotropic3DOrder1Gamma45_120k())
bm_A3Do1g45.addProblem(Anisotropic3DOrder1Gamma45_240k())
bm_A3Do1g45.addProblem(Anisotropic3DOrder1Gamma45_480k())
bm_A3Do1g45.addProblem(Anisotropic3DOrder1Gamma45_960k())
bm_A3Do1g45.addProblem(Anisotropic3DOrder1Gamma45_1920k())
bm_A3Do1g45.addProblem(Anisotropic3DOrder1Gamma45_3840k())
bm_A3Do1g45.addProblem(Anisotropic3DOrder1Gamma45_7680k())
bm_A3Do1g45.addProblem(Anisotropic3DOrder1Gamma45_15360k())

bm_A3Do2g30=Benchmark("Anisotropic 3D (gamma=30, order=2)")
bm_A3Do2g30.addProblem(Anisotropic3DOrder2Gamma30_30k())
bm_A3Do2g30.addProblem(Anisotropic3DOrder2Gamma30_60k())
bm_A3Do2g30.addProblem(Anisotropic3DOrder2Gamma30_120k())
bm_A3Do2g30.addProblem(Anisotropic3DOrder2Gamma30_240k())
bm_A3Do2g30.addProblem(Anisotropic3DOrder2Gamma30_480k())
bm_A3Do2g30.addProblem(Anisotropic3DOrder2Gamma30_960k())
bm_A3Do2g30.addProblem(Anisotropic3DOrder2Gamma30_1920k())
bm_A3Do2g30.addProblem(Anisotropic3DOrder2Gamma30_3840k())
bm_A3Do2g30.addProblem(Anisotropic3DOrder2Gamma30_7680k())
bm_A3Do2g30.addProblem(Anisotropic3DOrder2Gamma30_15360k())

bm_A3Do2g45=Benchmark("Anisotropic 3D (gamma=45, order=2)")
bm_A3Do2g45.addProblem(Anisotropic3DOrder2Gamma45_30k())
bm_A3Do2g45.addProblem(Anisotropic3DOrder2Gamma45_60k())
bm_A3Do2g45.addProblem(Anisotropic3DOrder2Gamma45_120k())
bm_A3Do2g45.addProblem(Anisotropic3DOrder2Gamma45_240k())
bm_A3Do2g45.addProblem(Anisotropic3DOrder2Gamma45_480k())
bm_A3Do2g45.addProblem(Anisotropic3DOrder2Gamma45_960k())
bm_A3Do2g45.addProblem(Anisotropic3DOrder2Gamma45_1920k())
bm_A3Do2g45.addProblem(Anisotropic3DOrder2Gamma45_3840k())
bm_A3Do2g45.addProblem(Anisotropic3DOrder2Gamma45_7680k())
bm_A3Do2g45.addProblem(Anisotropic3DOrder2Gamma45_15360k())


bms=BenchmarkSuite("Paso/Finley")
bms.addBenchmark(bm_L2Do1)
bms.addBenchmark(bm_L2Do2)
bms.addBenchmark(bm_L3Do1)
bms.addBenchmark(bm_L3Do2)
# bms.addBenchmark(bm_A2Do1g30)
# bms.addBenchmark(bm_A2Do1g45)
# bms.addBenchmark(bm_A2Do2g30)
# bms.addBenchmark(bm_A2Do2g45)
# bms.addBenchmark(bm_A3Do1g30)
# bms.addBenchmark(bm_A3Do1g45)
# bms.addBenchmark(bm_A3Do2g30)
# bms.addBenchmark(bm_A3Do2g45)
bms.run(scale=thlist)
out=bms.getHTML(filter=ff)
print out
