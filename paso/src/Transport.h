
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


#ifndef INC_PASOTRANSPORT
#define INC_PASOTRANSPORT

#define DT_FACTOR_MAX 100000.

#include "SystemMatrix.h"
#include "Options.h"
#include "performance.h"
#include "Paso.h"

typedef struct Paso_TransportProblem {

    bool valid_matrices;
    double dt_max_R;       /* safe time step size for reactive  part */
    double dt_max_T;       /* safe time step size for transport  part */
    double* constraint_mask;

    Paso_SystemMatrix * transport_matrix;
    Paso_SystemMatrix * mass_matrix;
 
    Paso_SystemMatrix * iteration_matrix;
    double* main_diagonal_low_order_transport_matrix;
    double* lumped_mass_matrix;     /* 'relevant' lumped mass matrix is assumed to be positive. 
                                       values with corresponding constraint_mask>0 value are set to -1
                                       to indicate the value infinity */
    double* reactive_matrix;
    double* main_diagonal_mass_matrix;

    Esys_MPIInfo *mpi_info;
    dim_t reference_counter;

} Paso_TransportProblem;



PASO_DLL_API
Paso_TransportProblem* Paso_TransportProblem_getReference(Paso_TransportProblem* in);

PASO_DLL_API
Paso_TransportProblem* Paso_TransportProblem_alloc(paso::SystemMatrixPattern_ptr pattern, int block_size);

PASO_DLL_API
dim_t Paso_TransportProblem_getBlockSize(const Paso_TransportProblem* in);

PASO_DLL_API
double Paso_TransportProblem_getSafeTimeStepSize(Paso_TransportProblem* in);

PASO_DLL_API
Paso_SystemMatrix* Paso_TransportProblem_borrowTransportMatrix(Paso_TransportProblem* in);

PASO_DLL_API
Paso_SystemMatrix* Paso_TransportProblem_borrowMassMatrix(Paso_TransportProblem* in);

PASO_DLL_API
void Paso_TransportProblem_solve(Paso_TransportProblem* fctp, double* u, double dt, double* u0, double* q, Paso_Options* options);

PASO_DLL_API
double* Paso_TransportProblem_borrowLumpedMassMatrix(Paso_TransportProblem* in);

PASO_DLL_API
dim_t Paso_TransportProblem_getTotalNumRows(Paso_TransportProblem* in);

PASO_DLL_API
void Paso_TransportProblem_free(Paso_TransportProblem* in);

PASO_DLL_API
void Paso_TransportProblem_reset(Paso_TransportProblem* in);

PASO_DLL_API
paso::Connector* Paso_TransportProblem_borrowConnector(const Paso_TransportProblem* in);

PASO_DLL_API
index_t Paso_TransportProblem_getTypeId(const index_t solver,const index_t preconditioner, const index_t package,const  bool symmetry, Esys_MPIInfo *mpi_info);

PASO_DLL_API
void Paso_TransportProblem_insertConstraint(Paso_TransportProblem* fctp,  const double* r,  double* source);


PASO_DLL_API
void Paso_TransportProblem_setUpConstraint(Paso_TransportProblem* fctp,  const double* q);

#define Paso_TransportProblem_borrowMainDiagonalPointer(_fct_) paso::SparseMatrix_borrowMainDiagonalPointer((_fct_)->mass_matrix->mainBlock)
#define Paso_TransportProblem_getBlockSize(__in__) (__in__)->transport_matrix->row_block_size
#define Paso_TransportProblem_borrowConnector(__in__) (__in__)->transport_matrix->pattern->col_connector
#define Paso_TransportProblem_borrowTransportMatrix(__in__) (__in__)->transport_matrix
#define Paso_TransportProblem_borrowMassMatrix(__in__) (__in__)->mass_matrix
#define Paso_TransportProblem_borrowLumpedMassMatrix(__in__) (__in__)->lumped_mass_matrix
#define Paso_TransportProblem_getTotalNumRows(__in__) Paso_SystemMatrix_getTotalNumRows((__in__)->transport_matrix)




#endif /* #ifndef INC_PASOTRANSPORT */
