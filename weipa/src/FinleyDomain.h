
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

#ifndef __WEIPA_FINLEYDOMAIN_H__
#define __WEIPA_FINLEYDOMAIN_H__

#include <weipa/DomainChunk.h>
#include <weipa/FinleyElements.h>
#include <boost/enable_shared_from_this.hpp>

namespace finley {
    class Mesh;
}

namespace weipa {

/// \brief Represents a full Finley or Dudley domain including nodes and
///        elements.
///
/// This class represents a Finley or Dudley domain including nodes, cells,
/// and face elements (plus contact elements for Finley). It provides
/// functionality to read a domain from a netCDF file (generated by the
/// domain's dump() method) or directly through an instance of finley::Mesh or
/// Dudley_Mesh.
///
/// Once initialised, the domain can be saved to a Silo file or its nodes
/// and elements accessed through the respective methods.
class FinleyDomain : public DomainChunk, public boost::enable_shared_from_this<FinleyDomain>
{
public:
    FinleyDomain();
    FinleyDomain(const FinleyDomain& m);
    virtual ~FinleyDomain();
    virtual bool initFromEscript(const escript::AbstractDomain* domain);
    virtual bool initFromFile(const std::string& filename);
    virtual bool writeToSilo(DBfile* dbfile, const std::string& pathInSilo,
                             const StringVec& labels, const StringVec& units,
                             bool writeMeshData);
    virtual void reorderGhostZones(int ownIndex);
    virtual void removeGhostZones(int ownIndex);
    virtual StringVec getMeshNames() const;
    virtual StringVec getVarNames() const;
    virtual ElementData_ptr getElementsByName(const std::string& name) const;
    virtual NodeData_ptr getMeshByName(const std::string& name) const;
    virtual DataVar_ptr getDataVarByName(const std::string& name) const;
    virtual Centering getCenteringForFunctionSpace(int fsCode) const;
    virtual NodeData_ptr getMeshForFunctionSpace(int fsCode) const;
    virtual ElementData_ptr getElementsForFunctionSpace(int fsCode) const;
    virtual NodeData_ptr getNodes() const { return nodes; }
    virtual std::string getSiloPath() const { return siloPath; }
    virtual void setSiloPath(const std::string& path)  { siloPath = path; }

private:
    void cleanup();

    bool initialized;
    FinleyNodes_ptr    nodes;
    FinleyElements_ptr cells;
    FinleyElements_ptr faces;
    FinleyElements_ptr contacts;
    std::string        siloPath;
};

} // namespace weipa

#endif // __WEIPA_FINLEYDOMAIN_H__

