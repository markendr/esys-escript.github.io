/* $Id$ */

/**************************************************************/

/* Paso: SystemMatrix is saved to Harwell-Boeing format     */

/**************************************************************/

/* Copyright: ACcESS Australia 2005                           */
/* Author: imran@esscc.uq.edu.au                              */

/**************************************************************/

#include "Paso.h"
#include "SystemMatrix.h"

/* TODO: Refactor the stuff in here into hbio, just like mmio! */

static dim_t M, N, nz;

static int calc_digits( int );
static void fmt_str( int, int, int*, int*, int*, char*, char* );
static void print_data( FILE*, int, int, int, char*, void*, int, int );
static void generate_HB( FILE*, dim_t*, dim_t*, double* );

/* function to get number of digits in an integer */
int calc_digits( int var )
{
	int digits = 1;
	while( (var/=10) )
		digits++;

	return digits;
}

/* function to generate the format string.
 *
 * use maxlen to determine no. of entries per line
 * use nvalues to determine no. of lines
 */
void fmt_str( int nvalues, int integer, int *width, int *nlines, int *nperline, char *pfmt, char *fmt )
{
	int per_line;
	int maxlen = *width;

 	if( integer && maxlen < 10 )
 		maxlen = 10;
	else
		maxlen = 13;

	per_line = 80 / maxlen;
	*nlines = nvalues / per_line;
	if( nvalues % per_line )
		(*nlines)++;

	*nperline = per_line;
	if( integer )
	{
		sprintf( pfmt, "(%dI%d)", per_line, maxlen );
		sprintf( fmt, "%%%dd", maxlen );
	}
	else
	{
		sprintf( pfmt, "(1P%dE%d.6)", per_line, maxlen );
		sprintf( fmt, "%%%d.6E", maxlen );
	}
	*width = maxlen;
}

/* function to print the actual data in the right format */
void print_data( FILE *fp, int n_perline, int width, int nval, char *fmt, void *ptr, int integer, int adjust )
{
	int entries_done = 0;
	int padding;
	char pad_fmt[10];

	padding = 80 - n_perline*width;
	sprintf( pad_fmt, "%%%dc", padding );

	if( adjust != 1 )
		adjust = 0;

	if( integer )
	{
		dim_t *data = (dim_t *)ptr;
		for( int i=0; i<nval; i++ )
		{
			fprintf( fp, fmt, data[i]+adjust );
			entries_done++;
			if( entries_done == n_perline )
			{
				if( padding )
					fprintf( fp, pad_fmt, ' ' );
				fprintf( fp, "\n" );
				entries_done = 0;
			}
		}
	}
	else
	{
		double *data = (double*)ptr;
		for( int i=0; i<nval; i++ )
		{
			fprintf( fp, fmt, data[i] );
			entries_done++;
			if( entries_done == n_perline )
			{
				if( padding )
					fprintf( fp, pad_fmt, ' ' );
				fprintf( fp, "\n" );
				entries_done = 0;
			}
		}
	}
	if( entries_done )
	{
		sprintf( pad_fmt, "%%%dc\n", (80 - entries_done*width) );
		fprintf( fp, pad_fmt, ' ' );
	}
}

void generate_HB( FILE *fp, dim_t *col_ptr, dim_t *row_ind, double *val )
{
	char buffer[81];

	int val_lines, ind_lines, ptr_lines;
	int val_perline, ind_perline, ptr_perline;
	int val_width, ind_width, ptr_width;
	char ptr_pfmt[7], ind_pfmt[7], val_pfmt[11];
	char ptr_fmt[10], ind_fmt[10], val_fmt[10];

	/* line 1 */
	sprintf( buffer, "%-72s%-8s", "Matrix Title", "Key" );
	buffer[80] = '\0';
	fprintf( fp, "%s\n", buffer );

	/* line 2 */
	ptr_width = calc_digits( nz+1 );
	fmt_str( N+1, 1, &ptr_width, &ptr_lines, &ptr_perline, ptr_pfmt, ptr_fmt );
	ind_width = calc_digits( N );
	fmt_str( nz, 1, &ind_width, &ind_lines, &ind_perline, ind_pfmt, ind_fmt );
	val_width = 13;
	fmt_str( nz, 0, &val_width, &val_lines, &val_perline, val_pfmt, val_fmt );
	sprintf( buffer, "%14d%14d%14d%14d%14d%10c", (ptr_lines+ind_lines+val_lines), ptr_lines, ind_lines, val_lines, 0, ' ' );
	buffer[80] = '\0';
	fprintf( fp, "%s\n", buffer );

	/* line 3 */
	sprintf( buffer, "%c%c%c%11c%14d%14d%14d%14d%10c", 'R', 'U', 'A', ' ', M, N, nz, 0, ' ' );
	buffer[80] = '\0';
	fprintf( fp, "%s\n", buffer );

	/* line 4 */
	sprintf( buffer, "%16s%16s%20s%28c", ptr_pfmt, ind_pfmt, val_pfmt, ' ');
	buffer[80]='\0';
	fprintf( fp, "%s\n", buffer );

	/* line 5 */
	/* NOT PRESENT */

	/* write the actual data */
	print_data( fp, ptr_perline, ptr_width, (N+1), ptr_fmt, col_ptr, 1, 1 );
	print_data( fp, ind_perline, ind_width, nz, ind_fmt, row_ind, 1, 1 );
	print_data( fp, val_perline, val_width, nz, val_fmt, val, 0, 0 );
}

void Paso_SystemMatrix_saveHB( Paso_SystemMatrix *A_p, char *filename_p )
{
	/* open the file */
	FILE *fileHandle_p = fopen( filename_p, "w" );
	if( fileHandle_p == NULL )
	{
		Paso_setError(IO_ERROR,"File could not be opened for writing.");
		return;
	}

	/* check the internal storage type
	 * currently ONLY support for CSC
	 */
	switch( A_p->type )
	{
		case CSC:
				if( A_p->row_block_size == 1 && A_p->col_block_size == 1 )
				{
					M = A_p->num_rows;
					N = A_p->num_cols;
					nz = A_p->len;
					generate_HB( fileHandle_p, A_p->pattern->ptr, A_p->pattern->index, A_p->val );
				}
				else
				{
					int i, curr_col;
					int iPtr, iCol, ir, ic;

// 					fprintf( fileHandle_p, "NEED unrolling!\n" );
					M = A_p->num_rows*A_p->row_block_size;
					N = A_p->num_cols*A_p->col_block_size;
					nz = A_p->len;

					dim_t *row_ind = MEMALLOC( nz, dim_t );
					dim_t *col_ind = MEMALLOC( nz, dim_t );

					i = 0;
					for( iCol=0; iCol<A_p->pattern->n_ptr; iCol++ )
						for( ic=0; ic<A_p->col_block_size; ic++)
							for( iPtr=A_p->pattern->ptr[iCol]-PTR_OFFSET; iPtr<A_p->pattern->ptr[iCol+1]-PTR_OFFSET; iPtr++)
								for( ir=0; ir<A_p->row_block_size; ir++ )
								{
									row_ind[i] = (A_p->pattern->index[iPtr]-INDEX_OFFSET)*A_p->row_block_size+ir+1;
									col_ind[i] = iCol*A_p->col_block_size+ic+1;
									i++;
								}

					/* get the col_ptr */
					dim_t *col_ptr = MEMALLOC( (N+1), dim_t );

					curr_col = 0;
					for( int j=0; (j<nz && curr_col<N); curr_col++ )
					{
						while( col_ind[j] != curr_col )
							j++;
						col_ptr[curr_col] = j;
					}
					col_ptr[N] = nz;

					/* generate the HB file */
					generate_HB( fileHandle_p, col_ptr, row_ind, A_p->val );

					/* free the allocated memory */
					MEMFREE( col_ptr );
					MEMFREE( col_ind );
					MEMFREE( row_ind );
				}
				break;
		case CSR:
// 				fprintf( fileHandle_p, "bleh CSR found,,\n" );
		default:
				Paso_setError(TYPE_ERROR,"__FILE__: only CSC is currently supported.\n");
	}

	/* close the file */
	fclose( fileHandle_p );

	return;
}

/*
 * $Log$
 * Revision 1.2  2005/09/15 03:44:39  jgs
 * Merge of development branch dev-02 back to main trunk on 2005-09-15
 *
 * Revision 1.1.2.1  2005/09/05 06:29:48  gross
 * These files have been extracted from finley to define a stand alone libray for iterative
 * linear solvers on the ALTIX. main entry through Paso_solve. this version compiles but
 * has not been tested yet.
 *
 *
 */
