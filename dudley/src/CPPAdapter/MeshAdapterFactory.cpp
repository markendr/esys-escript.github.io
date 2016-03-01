
/*****************************************************************************
*
* Copyright (c) 2003-2016 by The University of Queensland
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

#include "MeshAdapterFactory.h"
#include <dudley/Dudley.h>
#include <dudley/Mesh.h>
#include <dudley/TriangularMesh.h>

#include <escript/SubWorld.h>

#ifdef USE_NETCDF
#include <netcdfcpp.h>
#endif

#include <boost/python/extract.hpp>
#include <boost/scoped_array.hpp>

#include <sstream>

using namespace std;
using namespace escript;

namespace dudley {

#ifdef USE_NETCDF
// A convenience method to retrieve an integer attribute from a NetCDF file
template<typename T>
T ncReadAtt(NcFile* dataFile, const string& fName, const string& attrName)
{
    NcAtt* attr = dataFile->get_att(attrName.c_str());
    if (!attr) {
        stringstream msg;
        msg << "loadMesh: Error retrieving integer attribute '" << attrName
            << "' from NetCDF file '" << fName << "'";
        throw escript::IOError(msg.str());
    }
    T value = (sizeof(T) > 4 ? attr->as_long(0) : attr->as_int(0));
    delete attr;
    return value;
}
#endif

inline void cleanupAndThrow(Dudley_Mesh* mesh, string msg)
{
    Dudley_Mesh_free(mesh);
    string msgPrefix("loadMesh: NetCDF operation failed - ");
    throw escript::IOError(msgPrefix+msg);
}

Domain_ptr loadMesh(const std::string& fileName)
{
#ifdef USE_NETCDF
    escript::JMPI mpi_info = escript::makeInfo( MPI_COMM_WORLD );
    Dudley_Mesh *mesh_p=NULL;
    const string fName(mpi_info->appendRankToFileName(fileName));

    int *first_DofComponent, *first_NodeComponent;

    // Open NetCDF file for reading
    NcAtt *attr;
    NcVar *nc_var_temp;
    // netCDF error handler
    NcError err(NcError::silent_nonfatal);
    // Create the NetCDF file.
    NcFile dataFile(fName.c_str(), NcFile::ReadOnly);
    if (!dataFile.is_valid()) {
        stringstream msg;
        msg << "loadMesh: Opening NetCDF file '" << fName << "' for reading failed.";
        throw escript::IOError(msg.str());
    }

    // Read NetCDF integer attributes

    // index_size was only introduced with 64-bit index support so fall back
    // to 32 bits if not found.
    int index_size;
    try {
        index_size = ncReadAtt<int>(&dataFile, fName, "index_size");
    } catch (escript::IOError& e) {
        index_size = 4;
    }
    // technically we could cast if reading 32-bit data on 64-bit escript
    // but cost-benefit analysis clearly favours this implementation for now
    if (sizeof(index_t) != index_size) {
        throw escript::IOError("loadMesh: size of index types at runtime differ from dump file");
    }

    int mpi_size = ncReadAtt<int>(&dataFile, fName, "mpi_size");
    int mpi_rank = ncReadAtt<int>(&dataFile, fName, "mpi_rank");
    int numDim = ncReadAtt<int>(&dataFile, fName, "numDim");
    dim_t numNodes = ncReadAtt<dim_t>(&dataFile, fName, "numNodes");
    dim_t num_Elements = ncReadAtt<dim_t>(&dataFile, fName, "num_Elements");
    dim_t num_FaceElements = ncReadAtt<dim_t>(&dataFile, fName, "num_FaceElements");
    dim_t num_Points = ncReadAtt<dim_t>(&dataFile, fName, "num_Points");
    int num_Elements_numNodes = ncReadAtt<int>(&dataFile, fName, "num_Elements_numNodes");
    int Elements_TypeId = ncReadAtt<int>(&dataFile, fName, "Elements_TypeId");
    int num_FaceElements_numNodes = ncReadAtt<int>(&dataFile, fName, "num_FaceElements_numNodes");
    int FaceElements_TypeId = ncReadAtt<int>(&dataFile, fName, "FaceElements_TypeId");
    int Points_TypeId = ncReadAtt<int>(&dataFile, fName, "Points_TypeId");
    int num_Tags = ncReadAtt<int>(&dataFile, fName, "num_Tags");

    // Verify size and rank
    if (mpi_info->size != mpi_size) {
        stringstream msg;
        msg << "loadMesh: The NetCDF file '" << fName
            << "' can only be read on " << mpi_size
            << " CPUs. Currently running: " << mpi_info->size;
        throw DudleyException(msg.str());
    }
    if (mpi_info->rank != mpi_rank) {
        stringstream msg;
        msg << "loadMesh: The NetCDF file '" << fName
            << "' should be read on CPU #" << mpi_rank
            << " and NOT on #" << mpi_info->rank;
        throw DudleyException(msg.str());
    }

    // Read mesh name
    if (! (attr=dataFile.get_att("Name")) ) {
        stringstream msg;
        msg << "loadMesh: Error retrieving mesh name from NetCDF file '"
            << fName << "'";
        throw escript::IOError(msg.str());
    }
    boost::scoped_array<char> name(attr->as_string(0));
    delete attr;

    // allocate mesh
    mesh_p = Dudley_Mesh_alloc(name.get(), numDim, mpi_info);
    // read nodes
    Dudley_NodeFile_allocTable(mesh_p->Nodes, numNodes);
    // Nodes_Id
    if (! ( nc_var_temp = dataFile.get_var("Nodes_Id")) )
        cleanupAndThrow(mesh_p, "get_var(Nodes_Id)");
    if (! nc_var_temp->get(&mesh_p->Nodes->Id[0], numNodes) )
        cleanupAndThrow(mesh_p, "get(Nodes_Id)");
    // Nodes_Tag
    if (! ( nc_var_temp = dataFile.get_var("Nodes_Tag")) )
        cleanupAndThrow(mesh_p, "get_var(Nodes_Tag)");
    if (! nc_var_temp->get(&mesh_p->Nodes->Tag[0], numNodes) )
        cleanupAndThrow(mesh_p, "get(Nodes_Tag)");
    // Nodes_gDOF
    if (! ( nc_var_temp = dataFile.get_var("Nodes_gDOF")) )
        cleanupAndThrow(mesh_p, "get_var(Nodes_gDOF)");
    if (! nc_var_temp->get(&mesh_p->Nodes->globalDegreesOfFreedom[0], numNodes) )
        cleanupAndThrow(mesh_p, "get(Nodes_gDOF)");
    // Nodes_gNI
    if (! ( nc_var_temp = dataFile.get_var("Nodes_gNI")) )
        cleanupAndThrow(mesh_p, "get_var(Nodes_gNI)");
    if (! nc_var_temp->get(&mesh_p->Nodes->globalNodesIndex[0], numNodes) )
        cleanupAndThrow(mesh_p, "get(Nodes_gNI)");
    // Nodes_grDfI
    if (! ( nc_var_temp = dataFile.get_var("Nodes_grDfI")) )
        cleanupAndThrow(mesh_p, "get_var(Nodes_grDfI)");
    if (! nc_var_temp->get(&mesh_p->Nodes->globalReducedDOFIndex[0], numNodes) )
        cleanupAndThrow(mesh_p, "get(Nodes_grDfI)");
    // Nodes_grNI
    if (! ( nc_var_temp = dataFile.get_var("Nodes_grNI")) )
        cleanupAndThrow(mesh_p, "get_var(Nodes_grNI)");
    if (! nc_var_temp->get(&mesh_p->Nodes->globalReducedNodesIndex[0], numNodes) )
        cleanupAndThrow(mesh_p, "get(Nodes_grNI)");
    // Nodes_Coordinates
    if (!(nc_var_temp = dataFile.get_var("Nodes_Coordinates")))
        cleanupAndThrow(mesh_p, "get_var(Nodes_Coordinates)");
    if (! nc_var_temp->get(&(mesh_p->Nodes->Coordinates[0]), numNodes, numDim) )
        cleanupAndThrow(mesh_p, "get(Nodes_Coordinates)");

    Dudley_NodeFile_setTagsInUse(mesh_p->Nodes);

    /* read elements */
    mesh_p->Elements=Dudley_ElementFile_alloc((Dudley_ElementTypeId)Elements_TypeId, mpi_info);
    Dudley_ElementFile_allocTable(mesh_p->Elements, num_Elements);
    mesh_p->Elements->minColor=0;
    mesh_p->Elements->maxColor=num_Elements-1;
    if (num_Elements>0) {
       // Elements_Id
       if (! ( nc_var_temp = dataFile.get_var("Elements_Id")) )
           cleanupAndThrow(mesh_p, "get_var(Elements_Id)");
       if (! nc_var_temp->get(&mesh_p->Elements->Id[0], num_Elements) )
           cleanupAndThrow(mesh_p, "get(Elements_Id)");
       // Elements_Tag
       if (! ( nc_var_temp = dataFile.get_var("Elements_Tag")) )
           cleanupAndThrow(mesh_p, "get_var(Elements_Tag)");
       if (! nc_var_temp->get(&mesh_p->Elements->Tag[0], num_Elements) )
           cleanupAndThrow(mesh_p, "get(Elements_Tag)");
       // Elements_Owner
       if (! ( nc_var_temp = dataFile.get_var("Elements_Owner")) )
           cleanupAndThrow(mesh_p, "get_var(Elements_Owner)");
       if (! nc_var_temp->get(&mesh_p->Elements->Owner[0], num_Elements) )
           cleanupAndThrow(mesh_p, "get(Elements_Owner)");
       // Elements_Color
       if (! ( nc_var_temp = dataFile.get_var("Elements_Color")) )
           cleanupAndThrow(mesh_p, "get_var(Elements_Color)");
       if (! nc_var_temp->get(&mesh_p->Elements->Color[0], num_Elements) )
           cleanupAndThrow(mesh_p, "get(Elements_Color)");
       // Elements_Nodes
       int *Elements_Nodes = new int[num_Elements*num_Elements_numNodes];
       if (!(nc_var_temp = dataFile.get_var("Elements_Nodes"))) {
           delete[] Elements_Nodes;
           cleanupAndThrow(mesh_p, "get_var(Elements_Nodes)");
       }
       if (! nc_var_temp->get(&(Elements_Nodes[0]), num_Elements, num_Elements_numNodes) ) {
           delete[] Elements_Nodes;
           cleanupAndThrow(mesh_p, "get(Elements_Nodes)");
       }

       // Copy temp array into mesh_p->Elements->Nodes
       for (int i=0; i<num_Elements; i++) {
           for (int j=0; j<num_Elements_numNodes; j++) {
               mesh_p->Elements->Nodes[INDEX2(j,i,num_Elements_numNodes)]
                    = Elements_Nodes[INDEX2(j,i,num_Elements_numNodes)];
           }
       }
       delete[] Elements_Nodes;
       Dudley_ElementFile_setTagsInUse(mesh_p->Elements);
    } /* num_Elements>0 */

    /* get the face elements */
    mesh_p->FaceElements=Dudley_ElementFile_alloc((Dudley_ElementTypeId)FaceElements_TypeId, mpi_info);
    Dudley_ElementFile_allocTable(mesh_p->FaceElements, num_FaceElements);
    mesh_p->FaceElements->minColor=0;
    mesh_p->FaceElements->maxColor=num_FaceElements-1;
    if (num_FaceElements>0) {
       // FaceElements_Id
       if (! ( nc_var_temp = dataFile.get_var("FaceElements_Id")) )
           cleanupAndThrow(mesh_p, "get_var(FaceElements_Id)");
       if (! nc_var_temp->get(&mesh_p->FaceElements->Id[0], num_FaceElements) )
           cleanupAndThrow(mesh_p, "get(FaceElements_Id)");
       // FaceElements_Tag
       if (! ( nc_var_temp = dataFile.get_var("FaceElements_Tag")) )
           cleanupAndThrow(mesh_p, "get_var(FaceElements_Tag)");
       if (! nc_var_temp->get(&mesh_p->FaceElements->Tag[0], num_FaceElements) )
           cleanupAndThrow(mesh_p, "get(FaceElements_Tag)");
       // FaceElements_Owner
       if (! ( nc_var_temp = dataFile.get_var("FaceElements_Owner")) )
           cleanupAndThrow(mesh_p, "get_var(FaceElements_Owner)");
       if (! nc_var_temp->get(&mesh_p->FaceElements->Owner[0], num_FaceElements) )
           cleanupAndThrow(mesh_p, "get(FaceElements_Owner)");
       // FaceElements_Color
       if (! ( nc_var_temp = dataFile.get_var("FaceElements_Color")) )
           cleanupAndThrow(mesh_p, "get_var(FaceElements_Color)");
       if (! nc_var_temp->get(&mesh_p->FaceElements->Color[0], num_FaceElements) )
           cleanupAndThrow(mesh_p, "get(FaceElements_Color)");
       // FaceElements_Nodes
       int *FaceElements_Nodes = new int[num_FaceElements*num_FaceElements_numNodes];
       if (!(nc_var_temp = dataFile.get_var("FaceElements_Nodes"))) {
           delete[] FaceElements_Nodes;
           cleanupAndThrow(mesh_p, "get_var(FaceElements_Nodes)");
       }
       if (! nc_var_temp->get(&(FaceElements_Nodes[0]), num_FaceElements, num_FaceElements_numNodes) ) {
           delete[] FaceElements_Nodes;
           cleanupAndThrow(mesh_p, "get(FaceElements_Nodes)");
       }
       // Copy temp array into mesh_p->FaceElements->Nodes
       for (int i=0; i<num_FaceElements; i++) {
           for (int j=0; j<num_FaceElements_numNodes; j++) {
               mesh_p->FaceElements->Nodes[INDEX2(j,i,num_FaceElements_numNodes)] = FaceElements_Nodes[INDEX2(j,i,num_FaceElements_numNodes)];
           }
       }
       delete[] FaceElements_Nodes;
       Dudley_ElementFile_setTagsInUse(mesh_p->FaceElements);
    } /* num_FaceElements>0 */

    /* get the Points (nodal elements) */
    mesh_p->Points=Dudley_ElementFile_alloc((Dudley_ElementTypeId)Points_TypeId, mpi_info);
    Dudley_ElementFile_allocTable(mesh_p->Points, num_Points);
    mesh_p->Points->minColor=0;
    mesh_p->Points->maxColor=num_Points-1;
    if (num_Points>0) {
       // Points_Id
       if (! ( nc_var_temp = dataFile.get_var("Points_Id")))
           cleanupAndThrow(mesh_p, "get_var(Points_Id)");
       if (! nc_var_temp->get(&mesh_p->Points->Id[0], num_Points))
           cleanupAndThrow(mesh_p, "get(Points_Id)");
       // Points_Tag
       if (! ( nc_var_temp = dataFile.get_var("Points_Tag")))
           cleanupAndThrow(mesh_p, "get_var(Points_Tag)");
       if (! nc_var_temp->get(&mesh_p->Points->Tag[0], num_Points))
           cleanupAndThrow(mesh_p, "get(Points_Tag)");
       // Points_Owner
       if (! ( nc_var_temp = dataFile.get_var("Points_Owner")))
           cleanupAndThrow(mesh_p, "get_var(Points_Owner)");
       if (!nc_var_temp->get(&mesh_p->Points->Owner[0], num_Points))
           cleanupAndThrow(mesh_p, "get(Points_Owner)");
       // Points_Color
       if (! ( nc_var_temp = dataFile.get_var("Points_Color")))
           cleanupAndThrow(mesh_p, "get_var(Points_Color)");
       if (!nc_var_temp->get(&mesh_p->Points->Color[0], num_Points))
           cleanupAndThrow(mesh_p, "get(Points_Color)");
       // Points_Nodes
       int *Points_Nodes = new int[num_Points];
       if (!(nc_var_temp = dataFile.get_var("Points_Nodes"))) {
           delete[] Points_Nodes;
           cleanupAndThrow(mesh_p, "get_var(Points_Nodes)");
       }
       if (! nc_var_temp->get(&(Points_Nodes[0]), num_Points) ) {
           delete[] Points_Nodes;
           cleanupAndThrow(mesh_p, "get(Points_Nodes)");
       }
       // Copy temp array into mesh_p->Points->Nodes
       for (int i=0; i<num_Points; i++) {
           mesh_p->Points->Id[mesh_p->Points->Nodes[INDEX2(0,i,1)]] = Points_Nodes[i];
       }
       delete[] Points_Nodes;
       Dudley_ElementFile_setTagsInUse(mesh_p->Points);
    } /* num_Points>0 */

    /* get the tags */
    if (num_Tags>0) {
        // Temp storage to gather node IDs
        int *Tags_keys = new int[num_Tags];
        char name_temp[4096];
        int i;

        // Tags_keys
        if (! ( nc_var_temp = dataFile.get_var("Tags_keys")) ) {
            delete[] Tags_keys;
            cleanupAndThrow(mesh_p, "get_var(Tags_keys)");
        }
        if (! nc_var_temp->get(&Tags_keys[0], num_Tags) ) {
            delete[] Tags_keys;
            cleanupAndThrow(mesh_p, "get(Tags_keys)");
        }
        for (i=0; i<num_Tags; i++) {
          // Retrieve tag name
          sprintf(name_temp, "Tags_name_%d", i);
          if (! (attr=dataFile.get_att(name_temp)) ) {
              delete[] Tags_keys;
              stringstream msg;
              msg << "get_att(" << name_temp << ")";
              cleanupAndThrow(mesh_p, msg.str());
          }
          boost::scoped_array<char> name(attr->as_string(0));
          delete attr;
          Dudley_Mesh_addTagMap(mesh_p, name.get(), Tags_keys[i]);
        }
        delete[] Tags_keys;
    }

    // Nodes_DofDistribution
    first_DofComponent = new index_t[mpi_size+1];
    if (! ( nc_var_temp = dataFile.get_var("Nodes_DofDistribution")) ) {
        delete[] first_DofComponent;
        cleanupAndThrow(mesh_p, "get_var(Nodes_DofDistribution)");
    }
    if (! nc_var_temp->get(&first_DofComponent[0], mpi_size+1) ) {
        delete[] first_DofComponent;
        cleanupAndThrow(mesh_p, "get(Nodes_DofDistribution)");
    }

    // Nodes_NodeDistribution
    first_NodeComponent = new index_t[mpi_size+1];
    if (! ( nc_var_temp = dataFile.get_var("Nodes_NodeDistribution")) ) {
        delete[] first_DofComponent;
        delete[] first_NodeComponent;
        cleanupAndThrow(mesh_p, "get_var(Nodes_NodeDistribution)");
    }
    if (! nc_var_temp->get(&first_NodeComponent[0], mpi_size+1) ) {
        delete[] first_DofComponent;
        delete[] first_NodeComponent;
        cleanupAndThrow(mesh_p, "get(Nodes_NodeDistribution)");
    }
    Dudley_Mesh_createMappings(mesh_p, first_DofComponent, first_NodeComponent);
    delete[] first_DofComponent;
    delete[] first_NodeComponent;

    AbstractContinuousDomain* dom=new MeshAdapter(mesh_p);
    return dom->getPtr();
#else
    throw DataException("loadMesh: not compiled with NetCDF. Please contact your installation manager.");
#endif /* USE_NETCDF */
  }

  Domain_ptr readMesh(const std::string& fileName,
                      int integrationOrder,
                      int reducedIntegrationOrder,
                      int optimize)
  {
    //
    // create a copy of the filename to overcome the non-constness of call
    // to Dudley_Mesh_read
    Dudley_Mesh* fMesh=0;
    // Win32 refactor
    if( fileName.size() == 0 )
    {
       throw DataException("Null file name!");
    }

    char *fName = new char[fileName.size()+1];
        
    strcpy(fName,fileName.c_str());

    fMesh=Dudley_Mesh_read(fName,integrationOrder, reducedIntegrationOrder, optimize!=0);
    AbstractContinuousDomain* temp=new MeshAdapter(fMesh);
    
    delete[] fName;
    
    return temp->getPtr();
  }

  Domain_ptr readGmsh(const std::string& fileName,
                      int numDim,
                      int integrationOrder,
                      int reducedIntegrationOrder,
                      int optimize)
  {
    //
    // create a copy of the filename to overcome the non-constness of call
    // to Dudley_Mesh_read
    Dudley_Mesh* fMesh=0;
    if (fileName.size() == 0)
       throw DudleyException("Null file name!");

    char *fName = new char[fileName.size()+1];
    strcpy(fName,fileName.c_str());
    fMesh=Dudley_Mesh_readGmsh(fName, numDim, integrationOrder, reducedIntegrationOrder, optimize!=0);
    AbstractContinuousDomain* temp=new MeshAdapter(fMesh);
    delete[] fName;
    return temp->getPtr();
  }

  Domain_ptr brick(escript::JMPI& mpi_info, double n0, double n1,double n2,int order,
                   double l0,double l1,double l2,
                   int periodic0,int periodic1,
                   int periodic2,
                   int integrationOrder,
                   int reducedIntegrationOrder,
                   int useElementsOnFace,
                   int useFullElementOrder,
                   int optimize)
  {
    int numElements[]={static_cast<int>(n0),static_cast<int>(n1),static_cast<int>(n2)};
    double length[]={l0,l1,l2};

    if (periodic0 || periodic1) // we don't support periodic boundary conditions
    {
        throw DudleyException("Dudley does not support periodic boundary conditions.");
    }
    else if (integrationOrder>3 || reducedIntegrationOrder>1)
    {
        throw DudleyException("Dudley does not support the requested integrationOrders.");
    }
    else if (useElementsOnFace || useFullElementOrder)
    {
        throw DudleyException("Dudley does not support useElementsOnFace or useFullElementOrder.");
    }
    if (order>1)
    {
        throw DudleyException("Dudley does not support element order greater than 1.");
    }

    //
    // linearInterpolation
    Dudley_Mesh* fMesh=NULL;

    fMesh=Dudley_TriangularMesh_Tet4(numElements, length, integrationOrder,
                        reducedIntegrationOrder, optimize!=0,
                        mpi_info);

    AbstractContinuousDomain* temp=new MeshAdapter(fMesh);
    return temp->getPtr();
  }

  Domain_ptr brick_driver(const boost::python::list& args)
  {
      using boost::python::extract;
      boost::python::object pworld=args[15];
      escript::JMPI info;
      if (!pworld.is_none()) {
          extract<SubWorld_ptr> ex(pworld);
          if (!ex.check()) {       
              throw DudleyException("Invalid escriptworld parameter.");
          }
          info=ex()->getMPI();
      } else {
          info=escript::makeInfo(MPI_COMM_WORLD);

      }
      return brick(info, static_cast<int>(extract<float>(args[0])),
                   static_cast<int>(extract<float>(args[1])),
                   static_cast<int>(extract<float>(args[2])),
                   extract<int>(args[3]), extract<double>(args[4]),
                   extract<double>(args[5]), extract<double>(args[6]),
                   extract<int>(args[7]), extract<int>(args[8]),
                   extract<int>(args[9]), extract<int>(args[10]),
                   extract<int>(args[11]), extract<int>(args[12]),
                   extract<int>(args[13]), extract<int>(args[14])
                   );
  }  
  
  
  Domain_ptr rectangle_driver(const boost::python::list& args)
  {
      using boost::python::extract;
      boost::python::object pworld=args[12];
      escript::JMPI info;
      if (!pworld.is_none()) {
          extract<SubWorld_ptr> ex(pworld);
          if (!ex.check()) {
              throw DudleyException("Invalid escriptworld parameter.");
          }
          info=ex()->getMPI();
      } else {
          info=escript::makeInfo(MPI_COMM_WORLD);
      }

      return rectangle(info, static_cast<int>(extract<float>(args[0])),
                       static_cast<int>(extract<float>(args[1])),
                       extract<int>(args[2]), extract<double>(args[3]),
                       extract<double>(args[4]), extract<int>(args[5]),
                       extract<int>(args[6]), extract<int>(args[7]),
                       extract<int>(args[8]), extract<int>(args[9]),
                       extract<int>(args[10]), extract<int>(args[11]) 
                       );
  }  
  
  
  
  Domain_ptr rectangle(escript::JMPI& mpi_info, double n0, double n1, int order,
                       double l0, double l1,
                       int periodic0,int periodic1,
                       int integrationOrder,
                       int reducedIntegrationOrder,
                       int useElementsOnFace,
                       int useFullElementOrder,
                       int optimize)
  {
    int numElements[]={static_cast<int>(n0), static_cast<int>(n1)};
    double length[]={l0,l1};

    if (periodic0 || periodic1) // we don't support periodic boundary conditions
    {
        throw DudleyException("Dudley does not support periodic boundary conditions.");
    }
    else if (integrationOrder>3 || reducedIntegrationOrder>1)
    {
        throw DudleyException("Dudley does not support the requested integrationOrders.");
    }
    else if (useElementsOnFace || useFullElementOrder)
    {
        throw DudleyException("Dudley does not support useElementsOnFace or useFullElementOrder.");
    }

    if (order>1)
    {
        throw DudleyException("Dudley does not support element order greater than 1.");
    }
    Dudley_Mesh* fMesh=Dudley_TriangularMesh_Tri3(numElements, length,
          integrationOrder, reducedIntegrationOrder, optimize!=0,
          mpi_info);
    //
    // Convert any dudley errors into a C++ exception
    MeshAdapter* ma=new MeshAdapter(fMesh);
    return Domain_ptr(ma);
  }


} // namespace dudley

