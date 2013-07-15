
/*****************************************************************************
*
* Copyright (c) 2003-2013 by University of Queensland
* http://www.uq.edu.au
*
* Primary Business: Queensland, Australia
* Licensed under the Open Software License version 3.0
* http://www.opensource.org/licenses/osl-3.0.php
*
* Development until 2012 by Earth Systems Science Computational Center (ESSCC)
* Development since 2012 by School of Earth Sciences
*
*****************************************************************************/


/****************************************************************************

  Finley: declaration of rectangular mesh generators in 1D, 2D, 3D.

*****************************************************************************/

#ifndef __FINLEY_RECTANGULARMESH_H__
#define __FINLEY_RECTANGULARMESH_H__

#include "Mesh.h"

namespace finley {

Mesh* RectangularMesh_Hex20(const int*, const double*, const bool*, int, int, bool, bool, bool, bool);
Mesh* RectangularMesh_Hex8(const int*, const double*, const bool*, int, int, bool, bool, bool);
Mesh* RectangularMesh_Rec8(const int*, const double*, const bool*, int, int, bool, bool, bool, bool);
Mesh* RectangularMesh_Rec4(const int*, const double*, const bool*, int, int, bool, bool, bool);

}

#endif // __FINLEY_RECTANGULARMESH_H__

