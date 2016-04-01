
/*****************************************************************************
*
* Copyright (c) 2003-2016 by The University of Queensland
* http://www.uq.edu.au
*
* Primary Business: Queensland, Australia
* Licensed under the Apache License, version 2.0
* http://www.apache.org/licenses/LICENSE-2.0
*
* Development until 2012 by Earth Systems Science Computational Center (ESSCC)
* Development 2012-2013 by School of Earth Sciences
* Development from 2014 by Centre for Geoscience Computing (GeoComp)
*
*****************************************************************************/

#include <escript/AbstractContinuousDomain.h>

#include "MeshAdapterTestCase.h"

#include "dudley/CppAdapter/MeshAdapter.h"
#include "dudley/CppAdapter/MeshAdapterFactory.h"

#include <cppunit/TestCaller.h>
#include <boost/scoped_ptr.hpp>

using namespace escript;
using namespace dudley;
using namespace CppUnit;

void MeshAdapterTestCase::testAll()
{
    JMPI info=makeInfo(MPI_COMM_WORLD);
	brick(info);
}

TestSuite* MeshAdapterTestCase::suite()
{
    TestSuite *testSuite = new TestSuite("MeshAdapterTestCase");

    testSuite->addTest(new TestCaller<MeshAdapterTestCase>(
                "testAll",&MeshAdapterTestCase::testAll));
    return testSuite;
}

