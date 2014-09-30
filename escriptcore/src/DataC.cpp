
/*****************************************************************************
*
* Copyright (c) 2003-2014 by University of Queensland
* http://www.uq.edu.au
*
* Primary Business: Queensland, Australia
* Licensed under the Open Software License version 3.0
* http://www.opensource.org/licenses/osl-3.0.php
*
* Development until 2012 by Earth Systems Science Computational Center (ESSCC)
* Development 2012-2013 by School of Earth Sciences
* Development from 2014 by Centre for Geoscience Computing (GeoComp)
*
*****************************************************************************/


#include "DataC.h"

#include "Data.h"
#include "DataTypes.h"

int getFunctionSpaceType(struct escriptDataC* data) 
{
  escript::Data* temp=(escript::Data*)(data->m_dataPtr);
  return temp->getFunctionSpace().getTypeCode();
}


int isDataPointShapeEqual(struct escriptDataC* data, int rank, const int* dimensions)
{
  if (data == (struct escriptDataC*)0) {
       return 1;
  } else {
     escript::Data* temp=(escript::Data*)(data->m_dataPtr);
     return temp->isDataPointShapeEqual(rank, dimensions);
  }
}

int getNumDataPointsPerSample(struct escriptDataC* data) 
{
  if (data == (struct escriptDataC*)0) {
       return 0;
  } else {
     escript::Data* temp=(escript::Data*)(data->m_dataPtr);
     if (temp->isEmpty()) {
        return 0;
     } else {
          return (temp->getNumDataPointsPerSample());
     }
  }
}

int numSamplesEqual(struct escriptDataC* data, int numDataPointsPerSample,
                    dim_t numSamples)
{
  if (data == (struct escriptDataC*)0) {
     return 1;
  } else {
     escript::Data* temp=(escript::Data*)(data->m_dataPtr);
     return temp->numSamplesEqual(numDataPointsPerSample, numSamples);
  }
}

int getDataPointRank(struct escriptDataC* data)
{
  if (data == (struct escriptDataC*)0) {
       return 0;
  } else {
       escript::Data* temp=(escript::Data*)(data->m_dataPtr);
       return temp->getDataPointRank();
  }
}

int getDataPointShape(struct escriptDataC* data,int i)
{
  if (data == (struct escriptDataC*)0) {
       return 0;
  } else {
     escript::Data* temp=(escript::Data*)(data->m_dataPtr);
     int rank = temp->getDataPointRank();
     if (i<0 || i>=rank) {
        return 1;
     } else {
        const escript::DataTypes::ShapeType view=temp->getDataPointShape();
        return view[i];
     }
  }
}

int getDataPointSize(struct escriptDataC* data)
{
  escript::Data* temp=(escript::Data*)(data->m_dataPtr);
  return temp->getDataPointSize();
}

int getLength(struct escriptDataC* data)
{
  escript::Data* temp=(escript::Data*)(data->m_dataPtr);
  return temp->getLength();
}

int isExpanded(struct escriptDataC* data)
{
  if (data == (struct escriptDataC*)0) {
       return false;
  } else {
     escript::Data* temp=(escript::Data*)(data->m_dataPtr);
     if (temp->isEmpty()) {
        return false;
     } else {
        return temp->actsExpanded();
     }
  }
}

int isEmpty(escriptDataC* data) 
{
  if (data == (struct escriptDataC*)0) {
       return true;
  } else {
      escript::Data* temp=(escript::Data*)(data->m_dataPtr);
      return temp->isEmpty();
  }
}

// The unusual (for me) ordering of __const here is because I'm not sure
// whether gcc would try to interpret __const as a function attribute rather than
// a modifier on the return value. Putting it here should remove any ambiguity
// I have used const rather than __const in the cpp because only c++ will be reading the cpp.
double const* getSampleDataRO(struct escriptDataC* data, int sampleNo)
{
  if (data == (struct escriptDataC*)0) {
       return NULL;
  } else {
      escript::Data* temp=(escript::Data*)(data->m_dataPtr);
     if (temp->isEmpty()) {
        return NULL;
     } else {
        return temp->getSampleDataRO(sampleNo);
     }
  }
}

double* getSampleDataRW(struct escriptDataC* data, int sampleNo)
{
  if (data == (struct escriptDataC*)0) {
       return NULL;
  } else {
      escript::Data* temp=(escript::Data*)(data->m_dataPtr);
     if (temp->isEmpty()) {
        return NULL;
     } else {
        return temp->getSampleDataRW(sampleNo);
     }
  }
}

const double* getSampleDataROFast(struct escriptDataC* data, int sampleNo)
{
  escript::Data* temp=(escript::Data*)(data->m_dataPtr);
  return temp->getSampleDataRO(sampleNo);
}

double* getSampleDataRWFast(struct escriptDataC* data, int sampleNo)
{
  escript::Data* temp=(escript::Data*)(data->m_dataPtr);
  return temp->getSampleDataRW(sampleNo);
}

double* getDataRW(escriptDataC* data)
{
  escript::Data* temp=(escript::Data*)(data->m_dataPtr);
  if (temp->getNumSamples()>0)
  {
     requireWrite(data);
     return getSampleDataRWFast(data,0);
  }
  return 0;
}


void requireWrite(escriptDataC* data)
{
  if (data == (struct escriptDataC*)0) {
       return;
  } else {
      ((escript::Data*)(data->m_dataPtr))->requireWrite();
  }
}
