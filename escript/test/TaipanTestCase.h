
/*******************************************************
*
* Copyright (c) 2003-2012 by University of Queensland
* Earth Systems Science Computational Center (ESSCC)
* http://www.uq.edu.au/esscc
*
* Primary Business: Queensland, Australia
* Licensed under the Open Software License version 3.0
* http://www.opensource.org/licenses/osl-3.0.php
*
*******************************************************/


#if !defined  TaipanTestCase_20050427_H
#define  TaipanTestCase_20050427_H

#include <cppunit/TestFixture.h>
#include <cppunit/TestSuite.h>

class TaipanTestCase : public CppUnit::TestFixture
{
public:
  void testAll();
  void testN1();
  void testN0();

  static CppUnit::TestSuite* suite();
};

#endif

