
/*****************************************************************************
*
* Copyright (c) 2003-2020 by The University of Queensland
* http://www.uq.edu.au
*
* Primary Business: Queensland, Australia
* Licensed under the Apache License, version 2.0
* http://www.apache.org/licenses/LICENSE-2.0
*
* Development until 2012 by Earth Systems Science Computational Center (ESSCC)
* Development 2012-2013 by School of Earth Sciences
* Development from 2014-2017 by Centre for Geoscience Computing (GeoComp)
* Development from 2019 by School of Earth and Environmental Sciences
**
*****************************************************************************/


/*
*   Matrix Market I/O library for ANSI C
*
*   See http://math.nist.gov/MatrixMarket for details.
*
*/

#ifndef MM_IO_H
#define MM_IO_H

#include <fstream>

#define MM_MAX_LINE_LENGTH 1025
#define MatrixMarketBanner "%%MatrixMarket"
#define MM_MAX_TOKEN_LENGTH 64

typedef char MM_typecode[4];

char *mm_typecode_to_str(MM_typecode matcode);

int mm_read_banner(std::istream& f, MM_typecode *matcode);
int mm_read_mtx_crd_size(std::istream& f, int *M, int *N, int *nz);
int mm_read_mtx_array_size(std::istream& f, int *M, int *N);

int mm_write_banner(std::ostream& f, MM_typecode matcode);
int mm_write_mtx_crd_size(std::ostream& f, int M, int N, int nz);
int mm_write_mtx_array_size(std::ostream& f, int M, int N);


/********************* MM_typecode query functions ***************************/

#define mm_is_matrix(typecode)  ((typecode)[0]=='M')

#define mm_is_sparse(typecode)  ((typecode)[1]=='C')
#define mm_is_coordinate(typecode)((typecode)[1]=='C')
#define mm_is_dense(typecode)   ((typecode)[1]=='A')
#define mm_is_array(typecode)   ((typecode)[1]=='A')

#define mm_is_complex(typecode) ((typecode)[2]=='C')
#define mm_is_real(typecode)    ((typecode)[2]=='R')
#define mm_is_pattern(typecode) ((typecode)[2]=='P')
#define mm_is_integer(typecode) ((typecode)[2]=='I')

#define mm_is_symmetric(typecode)((typecode)[3]=='S')
#define mm_is_general(typecode) ((typecode)[3]=='G')
#define mm_is_skew(typecode)    ((typecode)[3]=='K')
#define mm_is_hermitian(typecode)((typecode)[3]=='H')

int mm_is_valid(MM_typecode matcode);       /* too complex for a macro */


/********************* MM_typecode modify functions ***************************/

#define mm_set_matrix(typecode) ((*typecode)[0]='M')
#define mm_set_coordinate(typecode) ((*typecode)[1]='C')
#define mm_set_array(typecode)  ((*typecode)[1]='A')
#define mm_set_dense(typecode)  mm_set_array(typecode)
#define mm_set_sparse(typecode) mm_set_coordinate(typecode)

#define mm_set_complex(typecode)((*typecode)[2]='C')
#define mm_set_real(typecode)   ((*typecode)[2]='R')
#define mm_set_pattern(typecode)((*typecode)[2]='P')
#define mm_set_integer(typecode)((*typecode)[2]='I')


#define mm_set_symmetric(typecode)((*typecode)[3]='S')
#define mm_set_general(typecode)((*typecode)[3]='G')
#define mm_set_skew(typecode)   ((*typecode)[3]='K')
#define mm_set_hermitian(typecode)((*typecode)[3]='H')

#define mm_clear_typecode(typecode) ((*typecode)[0]=(*typecode)[1]= \
                                    (*typecode)[2]=' ',(*typecode)[3]='G')

#define mm_initialize_typecode(typecode) mm_clear_typecode(typecode)


/********************* Matrix Market error codes ***************************/


#define MM_COULD_NOT_READ_FILE  11
#define MM_PREMATURE_EOF        12
#define MM_NOT_MTX              13
#define MM_NO_HEADER            14
#define MM_UNSUPPORTED_TYPE     15
#define MM_LINE_TOO_LONG        16
#define MM_COULD_NOT_WRITE_FILE 17


/******************** Matrix Market internal definitions ********************

   MM_matrix_typecode: 4-character sequence

                    object      sparse/     data        storage
                                dense       type        scheme

   string position:  [0]        [1]         [2]         [3]

   Matrix typecode:  M(atrix)  C(oord)      R(eal)      G(eneral)
                                A(array)    C(omplex)   H(ermitian)
                                            P(attern)   S(ymmetric)
                                            I(nteger)   sKew

 ****************************************************************************/

#define MM_MTX_STR      "matrix"
#define MM_ARRAY_STR    "array"
#define MM_DENSE_STR    "array"
#define MM_COORDINATE_STR "coordinate"
#define MM_SPARSE_STR   "coordinate"
#define MM_COMPLEX_STR  "complex"
#define MM_REAL_STR     "real"
#define MM_INT_STR      "integer"
#define MM_GENERAL_STR  "general"
#define MM_SYMM_STR     "symmetric"
#define MM_HERM_STR     "hermitian"
#define MM_SKEW_STR     "skew-symmetric"
#define MM_PATTERN_STR  "pattern"


/*  high level routines */

int mm_write_mtx_crd(char* fname, int M, int N, int nz, int* i, int* j,
                     double* val, MM_typecode matcode);

int mm_read_mtx_crd_data(std::istream& f, int M, int N, int nz, int* i, int* j,
                         double* val, MM_typecode matcode);

int mm_read_mtx_crd_entry(std::istream& f, int* i, int* j, double* real,
                          double* img, MM_typecode matcode);

int mm_read_unsymmetric_sparse(const char* fname, int* M, int* N, int* nz,
                double** val, int** I, int** J);

#endif

/*
 * $Log$
 * Revision 1.1  2004/10/26 06:53:59  jgs
 * Initial revision
 *
 * Revision 1.1  2004/07/02 00:48:35  gross
 * matrix market io function added
 *
 *
 */
