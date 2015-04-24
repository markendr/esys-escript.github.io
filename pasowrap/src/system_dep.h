
/*****************************************************************************
*
* Copyright (c) 2003-2015 by The University of Queensland
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


/**
\file pasowrap/src/system_dep.h
\ingroup Other
 */
/*
   @(#) system_dep.h
*/

#ifndef pasowrap_system_dep_h
#define pasowrap_system_dep_h

#include <cmath>

#define PASOWRAP_DLL_API

#ifdef _WIN32

#   ifndef PASOWRAP_STATIC_LIB
#      undef PASOWRAP_DLL_API
#      ifdef PASOWRAP_EXPORTS
#         define PASOWRAP_DLL_API __declspec(dllexport)
#      else
#         define PASOWRAP_DLL_API __declspec(dllimport)
#      endif
#   endif
#endif

#endif

