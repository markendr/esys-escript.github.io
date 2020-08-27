
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

#ifndef __WEIPA_SPECKLEYDOMAIN_H__
#define __WEIPA_SPECKLEYDOMAIN_H__

#include <weipa/DomainChunk.h>
#include <weipa/SpeckleyElements.h>
#include <boost/enable_shared_from_this.hpp>

namespace weipa {

/// \brief Represents a full Speckley domain including nodes and elements.
///
/// This class represents a Speckley domain including nodes, cells, and face
/// elements. It provides functionality to read a domain from a file
/// (generated by the domain's dump() method) or directly through an instance
/// of SpeckleyDomain.
///
/// Once initialised, the domain can be saved to a Silo file or its nodes
/// and elements accessed through the respective methods.
class SpeckleyDomain : public DomainChunk, public boost::enable_shared_from_this<SpeckleyDomain>
{
public:
    SpeckleyDomain();
    SpeckleyDomain(const SpeckleyDomain& m);
    virtual ~SpeckleyDomain() {}
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
    bool initialized;
    SpeckleyNodes_ptr    nodes;
    SpeckleyElements_ptr cells;
    SpeckleyElements_ptr faces;
    std::string        siloPath;
};

} // namespace weipa

#endif // __WEIPA_SPECKLEYDOMAIN_H__

