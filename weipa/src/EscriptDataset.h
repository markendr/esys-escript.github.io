
/*****************************************************************************
*
* Copyright (c) 2003-2018 by The University of Queensland
* http://www.uq.edu.au
*
* Primary Business: Queensland, Australia
* Licensed under the Apache License, version 2.0
* http://www.apache.org/licenses/LICENSE-2.0
*
* Development until 2012 by Earth Systems Science Computational Center (ESSCC)
* Development 2012-2013 by School of Earth Sciences
* Development from 2014 by Centre for Geoscience Computing (GeoComp)
*
*****************************************************************************/

#ifndef __WEIPA_ESCRIPTDATASET_H__
#define __WEIPA_ESCRIPTDATASET_H__

#include <weipa/weipa.h>

#include <ostream>

class DBfile;

namespace escript {
    class AbstractDomain;
    class Data;
}


namespace weipa {

typedef std::vector<DataVar_ptr>     DataChunks;
typedef std::vector<DomainChunk_ptr> DomainChunks;

struct VarInfo {
    std::string varName;
    std::string units;
    DataChunks dataChunks;
    IntVec sampleDistribution;
    bool valid;
};

typedef std::vector<VarInfo> VarVector;


/// \brief Represents an escript dataset including a domain and data variables
///        for one timestep.
//
/// This class represents an escript dataset complete with domain and
/// variable data. It can read the dataset from files generated by the
/// dump() methods within escript or through an escript domain instance plus
/// a number of escript::Data instances. Subsequently, the dataset can be
/// saved in the Silo or VTK file format or accessed through a number of
/// accessor methods.
///
/// If the data is distributed via MPI then all ranks should create an instance
/// of this class and call the respective methods. Dump files that stem from
/// a parallel run can be read on one processor or on the same number of MPI
/// processes as they were created with.
class WEIPA_DLL_API EscriptDataset
{
public:
    /// \brief Default constructor.
    EscriptDataset();

#if WEIPA_HAVE_MPI
    /// \brief Constructor with communicator.
    EscriptDataset(MPI_Comm comm);
#endif

    /// \brief Destructor.
    ~EscriptDataset();

    /// \brief Sets the escript domain for this dataset. This method can only
    ///        be called once and should be the first call unless loading from
    ///        dump files.
    ///
    /// \note If MPI is enabled this method also initialises the communicator
    ///       that will be used subsequently.
    bool setDomain(const escript::AbstractDomain* domain);

    /// \brief Adds an escript data instance to this dataset. You must ensure
    ///        that the data is defined on the domain that was used in
    //         setDomain(), otherwise you will get undefined behaviour later!
    bool addData(escript::Data& data, const std::string name,
                 const std::string units = "");

    /// \brief Loads domain and variables from escript NetCDF files.
    ///
    /// \param domainFilePattern a printf-style pattern for the domain file
    ///                          names (e.g. "dom.%02d.nc")
    /// \param varFiles a vector of file name patterns for variables
    /// \param varNames a vector of variable names
    /// \param nChunks number of chunks to load
    ///
    /// \note If MPI is enabled nChunks must be equal to the size of the
    ///       communicator or this method fails.
    bool loadNetCDF(const std::string domainFilePattern,
                    const StringVec& varFiles, const StringVec& varNames,
                    int nChunks);

    /// \brief Loads only variables from escript NetCDF files using the domain
    ///        provided.
    bool loadNetCDF(const DomainChunks& domain, const StringVec& varFiles,
                    const StringVec& varNames);

    /// \brief Sets the cycle number and time value for this dataset.
    void setCycleAndTime(int c, double t) { cycle=c; time=t; }

    /// \brief Returns the cycle number.
    int getCycle() const { return cycle; }

    /// \brief Returns the time value.
    double getTime() const { return time; }

    /// \brief Sets labels for the mesh axes.
    /// \note This information is only used by the Silo writer.
    void setMeshLabels(const std::string x, const std::string y, const std::string z="");

    /// \brief Sets units for the mesh axes.
    /// \note This information is only used by the Silo writer.
    void setMeshUnits(const std::string x, const std::string y, const std::string z="");

    /// \brief Sets a metadata schema and content
    /// \note Only used by the VTK writer.
    void setMetadataSchemaString(const std::string schema,
                                 const std::string metadata)
        { mdSchema=schema; mdString=metadata; }

    /// \brief Enables/Disables saving of mesh-related data
    void setSaveMeshData(bool flag) { wantsMeshVars=flag; }

    /// \brief Saves the dataset in the Silo file format.
    bool saveSilo(const std::string fileName, bool useMultiMesh=true);

    /// \brief Saves the dataset in the VTK XML file format.
    void saveVTK(const std::string fileName);

    /// \brief Returns the dataset's converted domain so it can be reused.
    DomainChunks getConvertedDomain() { return domainChunks; }

    /// \brief Returns a vector with the dataset's variables.
    const VarVector& getVariables() const { return variables; }

    /// \brief Returns a vector with the mesh variables.
    const VarVector& getMeshVariables() const { return meshVariables; }

#if WEIPA_HAVE_MPI
    MPI_Comm
#else
    void*
#endif
        getMPIComm() { return mpiComm; }

private:
    bool loadDomain(const std::string filePattern, int nChunks);
    bool setExternalDomain(const DomainChunks& domain);
    bool loadData(const std::string filePattern, const std::string name,
                  const std::string units);

    void convertMeshVariables();
    void updateSampleDistribution(VarInfo& vi);
    void putSiloMultiMesh(DBfile* dbfile, const std::string& meshName);
    void putSiloMultiTensor(DBfile* dbfile, const VarInfo& vi);
    void putSiloMultiVar(DBfile* dbfile, const VarInfo& vi,
                         bool useMeshFile = false);
    void saveVTKsingle(const std::string& fileName,
                       const std::string& meshName, const VarVector& vars);
    void writeVarToVTK(const VarInfo& varInfo, std::ostream& os);

    int cycle;
    double time;
    std::string mdSchema, mdString;
    StringVec meshLabels, meshUnits;
    bool externalDomain, wantsMeshVars;
    DomainChunks domainChunks;
    VarVector variables, meshVariables;
    int mpiRank, mpiSize;
#if WEIPA_HAVE_MPI
    MPI_Comm mpiComm;
#else
    void* mpiComm;
#endif
};

} // namespace weipa

#endif // __WEIPA_ESCRIPTDATASET_H__

