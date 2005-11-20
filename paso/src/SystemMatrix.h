/* $Id$ */

/**************************************************************/

/*   Paso: SystemMatrix and SystemVector */

/**************************************************************/

/*   Copyrights by ACcESS Australia 2003,2004,2005 */
/*   Author: gross@access.edu.au */

/**************************************************************/

#ifndef INC_PASO_SYSTEM
#define INC_PASO_SYSTEM
#ifdef MSVC
#ifdef PASO_EXPORTS
#define PASO_DLL __declspec(dllexport)
#else
#define PASO_DLL __declspec(dllimport)
#endif
#else
#define PASO_DLL
#endif

#include "Common.h"
#include "SystemMatrixPattern.h"
#include "Options.h"

#ifdef __cplusplus
extern "C" {
#endif


/**************************************************************/

/*  this struct holds a stiffness matrix: */

/* matrix type */
#define  CSC 0
#define  CSR 1
/* these formats are used in the SCSL context */
#define  CSC_SYM 2
#define  CSR_SYM 3
#define  CSC_BLK1 4
#define  CSR_BLK1 5
#define  CSC_BLK1_SYM 6
#define  CSR_BLK1_SYM 7

typedef int Paso_SystemMatrixType;

typedef struct Paso_SystemMatrix {
  Paso_SystemMatrixType type;
  dim_t reference_counter;

  dim_t logical_row_block_size;
  dim_t logical_col_block_size;
  dim_t logical_block_size;

  dim_t row_block_size;
  dim_t col_block_size;
  dim_t block_size;

  dim_t num_rows;
  dim_t num_cols;

  Paso_SystemMatrixPattern* pattern;

  dim_t len;
  double *val;

  double *normalizer; /* vector with a inverse of the absolute row/col sum (set by Solver.c)*/
  bool_t normalizer_is_valid;
  void* direct;  /* pointer to data needed by the direct solver */
  void* iterative; /* pointer to data needed by the iterative solver */

} Paso_SystemMatrix;

/*  interfaces: */

PASO_DLL Paso_SystemMatrix* Paso_SystemMatrix_alloc(Paso_SystemMatrixType,Paso_SystemMatrixPattern*,dim_t,dim_t);
PASO_DLL Paso_SystemMatrix* Paso_SystemMatrix_reference(Paso_SystemMatrix*);
PASO_DLL void Paso_SystemMatrix_dealloc(Paso_SystemMatrix*);

PASO_DLL void Paso_SystemMatrix_setValues(Paso_SystemMatrix*,double);
PASO_DLL void Paso_SystemMatrix_copy(Paso_SystemMatrix*,double*);
PASO_DLL void Paso_SystemMatrix_add(Paso_SystemMatrix*,dim_t,index_t*, dim_t,dim_t,index_t*,dim_t, double*);
PASO_DLL void Paso_SystemMatrix_MatrixVector(double alpha, Paso_SystemMatrix* A, double* in, double beta, double* out);

PASO_DLL void Paso_SystemMatrix_saveMM(Paso_SystemMatrix *, char *);
PASO_DLL void Paso_SystemMatrix_saveHB(Paso_SystemMatrix *, char *);
PASO_DLL Paso_SystemMatrix* Paso_SystemMatrix_loadMM_toCSR(char *);
PASO_DLL void Paso_SystemMatrix_nullifyRowsAndCols(Paso_SystemMatrix* A, double* mask_row, double* mask_col, double main_diagonal_value);
PASO_DLL void Paso_SystemMatrix_setDefaults(Paso_Options*);
PASO_DLL int Paso_SystemMatrix_getSystemMatrixTypeId(index_t solver, index_t package, bool_t symmetry);
PASO_DLL Paso_SystemMatrix* Paso_SystemMatrix_getSubmatrix(Paso_SystemMatrix* A,dim_t,index_t*,index_t*);
PASO_DLL double* Paso_SystemMatrix_borrowNormalization(Paso_SystemMatrix* A);

#ifdef __cplusplus
}
#endif /* __cplusplus */



#endif /* #ifndef INC_PASO_SYSTEM */

/*
 * $Log$
 * Revision 1.2  2005/09/15 03:44:38  jgs
 * Merge of development branch dev-02 back to main trunk on 2005-09-15
 *
 * Revision 1.1.2.2  2005/09/07 00:59:08  gross
 * some inconsistent renaming fixed to make the linking work.
 *
 * Revision 1.1.2.1  2005/09/05 06:29:47  gross
 * These files have been extracted from finley to define a stand alone libray for iterative
 * linear solvers on the ALTIX. main entry through Paso_solve. this version compiles but
 * has not been tested yet.
 *
 *
 */
