
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

/// Some utility routines

#ifndef __DUDLEY_UTIL_H__
#define __DUDLEY_UTIL_H__

#include "Dudley.h"

#include <escript/Data.h>

namespace dudley {
namespace util {

typedef std::pair<index_t,index_t> IndexPair;
typedef std::vector<IndexPair> ValueAndIndexList;

/// orders a ValueAndIndexList by value.
void sortValueAndIndex(ValueAndIndexList& array);

/// gathers values into array `out` from array `in` using `index`:
///   out(1:numData, 1:len) := in(1:numData, index(1:len))
void gather(int len, const index_t* index, int numData, const double* in,
            double* out);

/// adds array `in` into `out` using an `index`:
///   out(1:numData,index[p])+=in(1:numData,p) where
///   p={k=1...len, index[k]<upperBound}
void addScatter(int len, const index_t* index, int numData,
                const double* in, double *out, index_t upperBound);

/// multiplies two matrices: A(1:A1,1:A2) := B(1:A1,1:B2)*C(1:B2,1:A2)
void smallMatMult(int A1, int A2, double* A, int B2, const double* B,
                  const double* C);

/// multiplies a set of matrices with a single matrix:
///   A(1:A1,1:A2,i)=B(1:A1,1:B2,i)*C(1:B2,1:A2) for i=1,len
void smallMatSetMult1(int len, int A1, int A2, double* A, int B2,
                      const double* B, const double* C);

/// returns the normalized vector normal[dim,len] orthogonal to A(:,0,q) and
/// A(:,1,q) in the case of dim=3, or the vector A(:,0,q) in the case of dim=2
void normalVector(dim_t len, int dim, int dim1, const double* A, double* normal);

/// calculates the minimum and maximum value from an integer array of length
/// N x dim
IndexPair getMinMaxInt(int dim, dim_t N, const index_t* values);

/// calculates the minimum and maximum value from an integer array of length N
/// disregarding the value `ignore`
IndexPair getFlaggedMinMaxInt(dim_t N, const index_t* values, index_t ignore);

/// extracts the positive entries in `mask` returning a contiguous vector of
/// those entries
std::vector<index_t> packMask(const std::vector<short>& mask);

void setValuesInUse(const index_t* values, dim_t numValues,
                    std::vector<int>& valuesInUse, escript::JMPI mpiInfo);

} // namespace util
} // namespace dudley

#endif // __DUDLEY_UTIL_H__

