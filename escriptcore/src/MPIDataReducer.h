/*****************************************************************************
*
* Copyright (c) 2014-2015 by The University of Queensland
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

#ifndef __ESCRIPT_DATAREDUCER_H__
#define __ESCRIPT_DATAREDUCER_H__

#include "esysUtils/Esys_MPI.h"
#include "escript/Data.h"
#include <boost/shared_ptr.hpp>
#include "AbstractReducer.h"
namespace escript
{

// Reduces using pointwise MPI operations
class MPIDataReducer : public AbstractReducer
{
public:
    MPIDataReducer(MPI_Op op);
    ~MPIDataReducer(){};
    
        // This is not a constructor parameter because 
        // if these are created outside the subworld, they won't have
        // access to a domain yet.
        // I also want SplitWorld to be able to set this
    void setDomain(escript::Domain_ptr d);
    bool valueCompatible(boost::python::object v);
    bool reduceLocalValue(boost::python::object v, std::string& errstring);
    void reset();
    bool checkRemoteCompatibility(esysUtils::JMPI& mpi_info, std::string& errstring);
    
    void getCompatibilityInfo(std::vector<unsigned>& params);
    
      // talk to corresponding processes in other subworlds
    bool reduceRemoteValues(esysUtils::JMPI& mpi_info, bool active);
    
      // human readable description
    std::string description();
    
	// Get a value for this variable from another process
	// This is not a reduction and will replace any existing value
    bool recvFrom(Esys_MPI_rank localid, Esys_MPI_rank source, esysUtils::JMPI& mpiinfo);

	// Send a value to this variable to another process
	// This is not a reduction and will replace any existing value    
    bool sendTo(Esys_MPI_rank localid, Esys_MPI_rank target, esysUtils::JMPI& mpiinfo);    
    virtual boost::python::object getPyObj();

	// send from proc 0 in the communicator to all others
    bool groupSend(MPI_Comm& com);
    
	// reduction with some procs submitting identity values
    bool groupReduce(MPI_Comm& com, char mystate);    
   

    void newRunJobs();
private:    
    escript::Data value;
    escript::const_Domain_ptr dom;
    MPI_Op reduceop;
    bool had_an_export_this_round;
};

Reducer_ptr makeDataReducer(std::string type);

}

#endif // __ESCRIPT_DATAREDUCER_H__

