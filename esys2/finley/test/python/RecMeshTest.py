# $Id$
"""checks the rectangular mesh generator for a single element by comparing the generated mesh file with a reference"""

import sys
import os

import esys.escript
import esys.finley

TMPFILE="tmp.msh"

ref_line1="""Rectangular mesh with 2 nodes
1D-Nodes 2
0 0 1 0.000000000000000e+00
1 1 2 1.000000000000000e+00
Line2 1
0 0 0 1
Point1 2
1 1 0
2 2 1
Point1_Contact 0
Point1 0
"""

ref_line2="""Rectangular mesh with 3 nodes
1D-Nodes 3
0 0 1 0.000000000000000e+00
1 1 0 5.000000000000000e-01
2 2 2 1.000000000000000e+00
Line3 1
0 0 0 2 1
Point1 2
1 1 0
2 2 2
Point1_Contact 0
Point1 0
"""

ref_rec1="""Rectangular 2 x 2 mesh
2D-Nodes 4
0 0 11 0.000000000000000e+00 0.000000000000000e+00
1 1 12 1.000000000000000e+00 0.000000000000000e+00
2 2 21 0.000000000000000e+00 1.000000000000000e+00
3 3 22 1.000000000000000e+00 1.000000000000000e+00
Rec4 1
0 0 0 1 3 2
Line2 4
1 10 0 1
3 1 2 0
4 2 1 3
2 20 3 2
Line2_Contact 0
Point1 0
"""

ref_rec2="""Rectangular 3 x 3 mesh
2D-Nodes 8
0 0 11 0.000000000000000e+00 0.000000000000000e+00
1 1 10 5.000000000000000e-01 0.000000000000000e+00
2 2 12 1.000000000000000e+00 0.000000000000000e+00
3 3 1 0.000000000000000e+00 5.000000000000000e-01
5 4 2 1.000000000000000e+00 5.000000000000000e-01
6 5 21 0.000000000000000e+00 1.000000000000000e+00
7 6 20 5.000000000000000e-01 1.000000000000000e+00
8 7 22 1.000000000000000e+00 1.000000000000000e+00
Rec8 1
0 0 0 2 8 6 1 5 7 3
Line3 4
1 10 0 2 1
3 1 6 0 3
4 2 2 8 5
2 20 8 6 7
Line3_Contact 0
Point1 0
"""

ref_brick1="""Rectangular 2 x 2 x 2 mesh
3D-Nodes 8
0 0 111 0.000000000000000e+00 0.000000000000000e+00 0.000000000000000e+00
1 1 112 1.000000000000000e+00 0.000000000000000e+00 0.000000000000000e+00
2 2 121 0.000000000000000e+00 1.000000000000000e+00 0.000000000000000e+00
3 3 122 1.000000000000000e+00 1.000000000000000e+00 0.000000000000000e+00
4 4 211 0.000000000000000e+00 0.000000000000000e+00 1.000000000000000e+00
5 5 212 1.000000000000000e+00 0.000000000000000e+00 1.000000000000000e+00
6 6 221 0.000000000000000e+00 1.000000000000000e+00 1.000000000000000e+00
7 7 222 1.000000000000000e+00 1.000000000000000e+00 1.000000000000000e+00
Hex8 1
0 0 0 1 3 2 4 5 7 6
Rec4 6
1 100 0 2 3 1
3 1 0 4 6 2
5 10 0 1 5 4
4 2 1 3 7 5
6 20 2 6 7 3
2 200 4 5 7 6
Rec4_Contact 0
Point1 0
"""

ref_brick2="""Rectangular 3 x 3 x 3 mesh
3D-Nodes 20
0 0 111 0.000000000000000e+00 0.000000000000000e+00 0.000000000000000e+00
1 1 110 5.000000000000000e-01 0.000000000000000e+00 0.000000000000000e+00
2 2 112 1.000000000000000e+00 0.000000000000000e+00 0.000000000000000e+00
3 3 101 0.000000000000000e+00 5.000000000000000e-01 0.000000000000000e+00
5 4 102 1.000000000000000e+00 5.000000000000000e-01 0.000000000000000e+00
6 5 121 0.000000000000000e+00 1.000000000000000e+00 0.000000000000000e+00
7 6 120 5.000000000000000e-01 1.000000000000000e+00 0.000000000000000e+00
8 7 122 1.000000000000000e+00 1.000000000000000e+00 0.000000000000000e+00
9 8 11 0.000000000000000e+00 0.000000000000000e+00 5.000000000000000e-01
11 9 12 1.000000000000000e+00 0.000000000000000e+00 5.000000000000000e-01
15 10 21 0.000000000000000e+00 1.000000000000000e+00 5.000000000000000e-01
17 11 22 1.000000000000000e+00 1.000000000000000e+00 5.000000000000000e-01
18 12 211 0.000000000000000e+00 0.000000000000000e+00 1.000000000000000e+00
19 13 210 5.000000000000000e-01 0.000000000000000e+00 1.000000000000000e+00
20 14 212 1.000000000000000e+00 0.000000000000000e+00 1.000000000000000e+00
21 15 201 0.000000000000000e+00 5.000000000000000e-01 1.000000000000000e+00
23 16 202 1.000000000000000e+00 5.000000000000000e-01 1.000000000000000e+00
24 17 221 0.000000000000000e+00 1.000000000000000e+00 1.000000000000000e+00
25 18 220 5.000000000000000e-01 1.000000000000000e+00 1.000000000000000e+00
26 19 222 1.000000000000000e+00 1.000000000000000e+00 1.000000000000000e+00
Hex20 1
0 0 0 2 8 6 18 20 26 24 1 5 7 3 9 11 17 15 19 23 25 21
Rec8 6
1 100 0 6 8 2 3 7 5 1
3 1 0 18 24 6 9 21 15 3
5 10 0 2 20 18 1 11 19 9
4 2 2 8 26 20 5 17 23 11
6 20 6 24 26 8 15 25 17 7
2 200 18 20 26 24 19 23 25 21
Rec8_Contact 0
Point1 0
"""
ref_line1_onElement="""Rectangular mesh with 2 nodes
1D-Nodes 2
0 0 1 0.000000000000000e+00
1 1 2 1.000000000000000e+00
Line2 1
0 0 0 1
Line2Face 2
1 1 0 1
2 2 1 0
Line2Face_Contact 0
Point1 0
"""

ref_line2_onElement="""Rectangular mesh with 3 nodes
1D-Nodes 3
0 0 1 0.000000000000000e+00
1 1 0 5.000000000000000e-01
2 2 2 1.000000000000000e+00
Line3 1
0 0 0 2 1
Line3Face 2
1 1 0 2 1
2 2 2 0 1
Line3Face_Contact 0
Point1 0
"""

ref_rec1_onElement="""Rectangular 2 x 2 mesh
2D-Nodes 4
0 0 11 0.000000000000000e+00 0.000000000000000e+00
1 1 12 1.000000000000000e+00 0.000000000000000e+00
2 2 21 0.000000000000000e+00 1.000000000000000e+00
3 3 22 1.000000000000000e+00 1.000000000000000e+00
Rec4 1
0 0 0 1 3 2
Rec4Face 4
1 10 0 1 3 2
2 20 3 2 0 1
3 1 2 0 1 3
4 2 1 3 2 0
Rec4Face_Contact 0
Point1 0
"""

ref_rec2_onElement="""Rectangular 3 x 3 mesh
2D-Nodes 8
0 0 11 0.000000000000000e+00 0.000000000000000e+00
1 1 10 5.000000000000000e-01 0.000000000000000e+00
2 2 12 1.000000000000000e+00 0.000000000000000e+00
3 3 1 0.000000000000000e+00 5.000000000000000e-01
5 4 2 1.000000000000000e+00 5.000000000000000e-01
6 5 21 0.000000000000000e+00 1.000000000000000e+00
7 6 20 5.000000000000000e-01 1.000000000000000e+00
8 7 22 1.000000000000000e+00 1.000000000000000e+00
Rec8 1
0 0 0 2 8 6 1 5 7 3
Rec8Face 4
1 10 0 2 8 6 1 5 7 3
2 20 8 6 0 2 7 3 1 5
3 1 6 0 2 8 3 1 5 7
4 2 2 8 6 0 5 7 3 1
Rec8Face_Contact 0
Point1 0
"""

ref_brick1_onElement="""Rectangular 2 x 2 x 2 mesh
3D-Nodes 8
0 0 111 0.000000000000000e+00 0.000000000000000e+00 0.000000000000000e+00
1 1 112 1.000000000000000e+00 0.000000000000000e+00 0.000000000000000e+00
2 2 121 0.000000000000000e+00 1.000000000000000e+00 0.000000000000000e+00
3 3 122 1.000000000000000e+00 1.000000000000000e+00 0.000000000000000e+00
4 4 211 0.000000000000000e+00 0.000000000000000e+00 1.000000000000000e+00
5 5 212 1.000000000000000e+00 0.000000000000000e+00 1.000000000000000e+00
6 6 221 0.000000000000000e+00 1.000000000000000e+00 1.000000000000000e+00
7 7 222 1.000000000000000e+00 1.000000000000000e+00 1.000000000000000e+00
Hex8 1
0 0 0 1 3 2 4 5 7 6
Hex8Face 6
1 100 0 2 3 1 4 6 7 5
2 200 4 5 7 6 0 1 3 2
3 1 0 4 6 2 1 5 7 3
4 2 1 3 7 5 0 2 6 4
5 10 0 1 5 4 2 3 7 6
6 20 2 6 7 3 0 4 5 1
Hex8Face_Contact 0
Point1 0
"""

ref_brick2_onElement="""Rectangular 3 x 3 x 3 mesh
3D-Nodes 20
0 0 111 0.000000000000000e+00 0.000000000000000e+00 0.000000000000000e+00
1 1 110 5.000000000000000e-01 0.000000000000000e+00 0.000000000000000e+00
2 2 112 1.000000000000000e+00 0.000000000000000e+00 0.000000000000000e+00
3 3 101 0.000000000000000e+00 5.000000000000000e-01 0.000000000000000e+00
5 4 102 1.000000000000000e+00 5.000000000000000e-01 0.000000000000000e+00
6 5 121 0.000000000000000e+00 1.000000000000000e+00 0.000000000000000e+00
7 6 120 5.000000000000000e-01 1.000000000000000e+00 0.000000000000000e+00
8 7 122 1.000000000000000e+00 1.000000000000000e+00 0.000000000000000e+00
9 8 11 0.000000000000000e+00 0.000000000000000e+00 5.000000000000000e-01
11 9 12 1.000000000000000e+00 0.000000000000000e+00 5.000000000000000e-01
15 10 21 0.000000000000000e+00 1.000000000000000e+00 5.000000000000000e-01
17 11 22 1.000000000000000e+00 1.000000000000000e+00 5.000000000000000e-01
18 12 211 0.000000000000000e+00 0.000000000000000e+00 1.000000000000000e+00
19 13 210 5.000000000000000e-01 0.000000000000000e+00 1.000000000000000e+00
20 14 212 1.000000000000000e+00 0.000000000000000e+00 1.000000000000000e+00
21 15 201 0.000000000000000e+00 5.000000000000000e-01 1.000000000000000e+00
23 16 202 1.000000000000000e+00 5.000000000000000e-01 1.000000000000000e+00
24 17 221 0.000000000000000e+00 1.000000000000000e+00 1.000000000000000e+00
25 18 220 5.000000000000000e-01 1.000000000000000e+00 1.000000000000000e+00
26 19 222 1.000000000000000e+00 1.000000000000000e+00 1.000000000000000e+00
Hex20 1
0 0 0 2 8 6 18 20 26 24 1 5 7 3 9 11 17 15 19 23 25 21
Hex20Face 6
1 100 0 6 8 2 18 24 26 20 3 7 5 1 9 15 17 11 21 25 23 19
2 200 18 20 26 24 0 2 8 6 19 23 25 21 9 11 17 15 1 5 7 3
3 1 0 18 24 6 2 20 26 8 9 21 15 3 1 19 25 7 11 23 17 5
4 2 2 8 26 20 0 6 24 18 5 17 23 11 1 7 25 19 3 15 21 9
5 10 0 2 20 18 6 8 26 24 1 11 19 9 3 5 23 21 7 17 25 15
6 20 6 24 26 8 0 18 20 2 15 25 17 7 3 21 23 5 9 19 11 1
Hex20Face_Contact 0
Point1 0
"""

def checker(dom,reference):
   dom.write(TMPFILE)
   mshfile=open(TMPFILE).read()
   if reference != mshfile:
      print reference
      print mshfile
      return None
   else:
      return not None

failed=[]

my_dom=Interval(1,1)
if checker(my_dom,ref_line1):
  print "@@@@ line, order 1 passed"
else:
  failed.append("line, order 1")

my_dom=Interval(1,2)
if checker(my_dom,ref_line2):
  print "@@@@ line, order 2 passed"
else:
  failed.append("line, order 2")

my_dom=Rectangle(1,1,1)
if checker(my_dom,ref_rec1):
  print "@@@@ rec, order 1 passed"
else:
  failed.append("rec, order 1")

my_dom=Rectangle(1,1,2)
if checker(my_dom,ref_rec2):
  print "@@@@ rec, order 2 passed"
else:
  failed.append("rec, order 2")

my_dom=Brick(1,1,1,1)
if checker(my_dom,ref_brick1):
  print "@@@@ brick, order 1 passed"
else:
  failed.append("brick, order 1")

my_dom=Brick(1,1,1,2)
if checker(my_dom,ref_brick2):
  print "@@@@ brick, order 2 passed"
else:
  failed.append("brick, order 2")

my_dom=Interval(1,1,useElementsOnFace=1)
if checker(my_dom,ref_line1_onElement):
  print "@@@@ line, order 1, onElement passed"
else:
  failed.append("line, order 1, onElement")

#my_dom=Interval(1,2,useElementsOnFace=1)
#if checker(my_dom,ref_line2_onElement):
#  print "@@@@ line, order 2, onElement passed"
#else:
#  failed.append("line, order 2, onElement")

my_dom=Rectangle(1,1,1,useElementsOnFace=1)
if checker(my_dom,ref_rec1_onElement):
  print "@@@@ rec, order 1, onElement passed"
else:
  failed.append("rec, order 1, onElement")

my_dom=Rectangle(1,1,2,useElementsOnFace=1)
if checker(my_dom,ref_rec2_onElement):
  print "@@@@ rec, order 2, onElement passed"
else:
  failed.append("rec, order 2, onElement")

my_dom=Brick(1,1,1,1,useElementsOnFace=1)
if checker(my_dom,ref_brick1_onElement):
  print "@@@@ brick, order 1, onElement passed"
else:
  failed.append("brick, order 1, onElement")

my_dom=Brick(1,1,1,2,useElementsOnFace=1)
if checker(my_dom,ref_brick2_onElement):
  print "@@@@ brick, order 2, onElement passed"
else:
  failed.append("brick, order 2, onElement")

if len(failed) == 0:
   print "@@ mesh generation test passed"
else:
   print "@@ mesh generation failed for %s"%failed
  
