/**************************************************************/

/*   Finley: write Mesh */

/**************************************************************/

/*   Copyrights by ACcESS Australia 2003 */
/*   Author: gross@access.edu.au */
/*   Version: $Id$ */

/**************************************************************/

#include "Common.h"
#include "Finley.h"
#include "Mesh.h"

/**************************************************************/

/*  writes the mesh to the external file fname unsing the Finley file format: */

void Finley_Mesh_write(Finley_Mesh *in,char* fname) {
  FILE *f;
  int NN,i,j,numDim;

  /* open file */
  f=fopen(fname,"w");
  if (f==NULL) {
    Finley_ErrorCode=IO_ERROR;
    sprintf(Finley_ErrorMsg,"Opening file %s for writing failed.",fname);
    return;
  }

  /* write header */

  fprintf(f,"%s\n",in->Name);
  
  /*  write nodes: */
  
  if (in->Nodes!=NULL) {
    numDim=Finley_Mesh_getDim(in);
    fprintf(f,"%1dD-Nodes %d\n", numDim, in->Nodes->numNodes);
    for (i=0;i<in->Nodes->numNodes;i++) {
      fprintf(f,"%d %d %d",in->Nodes->Id[i],in->Nodes->degreeOfFreedom[i],in->Nodes->Tag[i]);
      for (j=0;j<numDim;j++) fprintf(f," %20.15e",in->Nodes->Coordinates[INDEX2(j,i,numDim)]);
      fprintf(f,"\n");
    }
  } else {
    fprintf(f,"0D-Nodes 0\n");
  }
  
  /*  write elements: */

  if (in->Elements!=NULL) {
    fprintf(f, "%s %d\n",in->Elements->ReferenceElement->Type->Name,in->Elements->numElements);
    NN=in->Elements->ReferenceElement->Type->numNodes;
    for (i=0;i<in->Elements->numElements;i++) {
      fprintf(f,"%d %d",in->Elements->Id[i],in->Elements->Tag[i]);
      for (j=0;j<NN;j++) fprintf(f," %d",in->Nodes->Id[in->Elements->Nodes[INDEX2(j,i,NN)]]);
      fprintf(f,"\n");
    }
  } else {
    fprintf(f,"Tet4 0\n");
  }

  /*  write face elements: */
  if (in->FaceElements!=NULL) {
    fprintf(f, "%s %d\n", in->FaceElements->ReferenceElement->Type->Name,in->FaceElements->numElements);
    NN=in->FaceElements->ReferenceElement->Type->numNodes;
    for (i=0;i<in->FaceElements->numElements;i++) {
      fprintf(f,"%d %d",in->FaceElements->Id[i],in->FaceElements->Tag[i]);
      for (j=0;j<NN;j++) fprintf(f," %d",in->Nodes->Id[in->FaceElements->Nodes[INDEX2(j,i,NN)]]);
      fprintf(f,"\n");
    }
  } else {
    fprintf(f,"Tri3 0\n");
  }

  /*  write Contact elements : */
  if (in->ContactElements!=NULL) {
    fprintf(f, "%s %d\n",in->ContactElements->ReferenceElement->Type->Name,in->ContactElements->numElements);
    NN=in->ContactElements->ReferenceElement->Type->numNodes;
    for (i=0;i<in->ContactElements->numElements;i++) {
      fprintf(f,"%d %d",in->ContactElements->Id[i],in->ContactElements->Tag[i]);
      for (j=0;j<NN;j++) fprintf(f," %d",in->Nodes->Id[in->ContactElements->Nodes[INDEX2(j,i,NN)]]);
      fprintf(f,"\n");
    }
  } else {
    fprintf(f,"Tri3_Contact 0\n");
  }
  
  /*  write points: */
  if (in->Points!=NULL) {
    fprintf(f, "%s %d\n",in->Points->ReferenceElement->Type->Name,in->Points->numElements);
    for (i=0;i<in->Points->numElements;i++) {
      fprintf(f,"%d %d %d\n",in->Points->Id[i],in->Points->Tag[i],in->Nodes->Id[in->Points->Nodes[INDEX2(0,i,1)]]);
    }
  } else {
    fprintf(f,"Point1 0\n");
  }
  
  fclose(f);
  #ifdef Finley_TRACE
  printf("mesh %s has been written to file %s\n",in->Name,fname);
  #endif
}

/*
* $Log$
* Revision 1.1  2004/10/26 06:53:57  jgs
* Initial revision
*
* Revision 1.1.1.1  2004/06/24 04:00:40  johng
* Initial version of eys using boost-python.
*
*
*/

