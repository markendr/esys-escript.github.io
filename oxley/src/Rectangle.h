/*****************************************************************************
*
* Copyright (c) 2003-2019 by The University of Queensland
* http://www.uq.edu.au
*
* Primary Business: Queensland, Australia
* Licensed under the Apache License, version 2.0f
* http://www.apache.org/licenses/LICENSE-2.0
*
* Development until 2012 by Earth Systems Science Computational Center (ESSCC)
* Development 2012-2013 by School of Earth Sciences
* Development from 2014 by Centre for Geoscience Computing (GeoComp)
*
*****************************************************************************/

#ifndef __OXLEY_RECTANGLE_H__
#define __OXLEY_RECTANGLE_H__

#include <escript/Data.h>
#include <escript/EsysMPI.h>
#include <escript/SubWorld.h>

#include <oxley/AbstractAssembler.h>
#include <oxley/OxleyData.h>
#include <oxley/OxleyDomain.h>

#include <p4est.h>
#include <p4est_connectivity.h>
#include <p4est_lnodes.h>

#include <boost/python.hpp>
#ifdef ESYS_HAVE_BOOST_NUMPY
#include <boost/python/numpy.hpp>
#endif

using namespace boost::python;

namespace oxley {

/**
   \brief
   Rectangle is the 2-dimensional implementation of a Oxleydomain.
*/
class Rectangle: public OxleyDomain
{

    template<class Scalar> friend class DefaultAssembler2D;

public:

    /**
       \brief creates a rectangular mesh with n0 x n1 elements over the
              rectangle [x0,x1] x [y0,y1].
       \param
    */
    Rectangle(int order, dim_t n0, dim_t n1,
        double x0, double y0, double x1, double y1,
        int d0, int d1,
        int periodic0, int periodic1);

    /**
       \brief creates a rectangular mesh from numpy arrays [x,y].
            Requires boost numpy
       \param
    */
#ifdef ESYS_HAVE_BOOST_NUMPY
    Rectangle(int order, dim_t n0, dim_t n1, boost::python::numpy::ndarray x, boost::python::numpy::ndarray y);
#endif

    /**
       \brief
       Destructor.
    */
    ~Rectangle();

    /**
       \brief
       returns a description for this domain
    */
    virtual std::string getDescription() const;

    /**
       \brief
       writes the current mesh to a file with the given name
       \param filename The name of the file to write to
    */
    virtual void write(const std::string& filename) const;

    /**
       \brief
       dumps the mesh to a file with the given name
       \param filename The name of the output file
    */
    virtual void dump(const std::string& filename) const;

    /**
       \brief equality operator
    */
    virtual bool operator==(const escript::AbstractDomain& other) const;

    /**
       \brief
       interpolates data given on source onto target where source and target
       are given on different domains
    */
    virtual void interpolateAcross(escript::Data& target,
                                   const escript::Data& source) const;

    /**
       \brief
       determines whether interpolation from source to target is possible
    */
    virtual bool probeInterpolationAcross(int, const escript::AbstractDomain&,
            int) const;

    /**
       \brief
       returns true if this rank owns the sample id.
    */
    virtual bool ownSample(int fs_code, index_t id) const;

    /**
       \brief
       copies the surface normals at data points into out. The actual function
       space to be considered is defined by out. out has to be defined on this
       domain.
    */
    virtual void setToNormal(escript::Data& out) const;

    /**
       \brief
       copies the size of samples into out. The actual function space to be
       considered is defined by out. out has to be defined on this domain.
    */
    virtual void setToSize(escript::Data& out) const;

    /**
     * \brief
       Returns a Data object filled with random data passed through filter.
    */
    virtual escript::Data randomFill(const escript::DataTypes::ShapeType& shape,
       const escript::FunctionSpace& what, long seed, const boost::python::tuple& filter) const;

    /**
       \brief
       returns the array of reference numbers for a function space type
       \param fsType The function space type
    */
    const dim_t* borrowSampleReferenceIDs(int fsType) const;

    /**
       \brief
       writes the mesh to a VTK file
       \param filename The file name
       \param writeMesh whether to write tag information
    */
    virtual void writeToVTK(std::string filename, bool writeMesh) const;

    /**
       \brief
       refines the mesh
       \param maxRecursion Max levels of recursion
       \param algorithmname The algorithm to use
    */
    virtual void refineMesh(int maxRecursion, std::string algorithmname);

    /**
       \brief
       sets the number of levels of refinement
    */
    virtual void setRefinementLevels(int refinementlevels)
    {
        forestData->max_levels_refinement = refinementlevels;
    };

    /**
       \brief
       returns a Data object containing the coordinate information
    */
    virtual escript::Data getX() const;

    /**
       \brief
       returns the number of vertices (int)
    */
    int getNumVertices() const { return connectivity->num_vertices;};

    /**
       \brief
       creates and returns an assembler of the requested type.
    */
    virtual Assembler_ptr createAssembler(std::string type, const DataMap& options) const;


    virtual dim_t findNode(const double *coords) const;

    /**
       \brief inequality operator
    */
    // virtual bool operator!=(const escript::AbstractDomain& other) const {
    //     return !(operator==(other));
    // }

    // These functions are used internally and are not exposed to python
    p4est_t * borrow_p4est() const { return p4est;};
    p4estData * borrow_forestData() { return forestData;};
    p4est_connectivity_t * borrow_connectivity() const { return connectivity; };
    void * borrow_temp_data() { return temp_data; };
    void set_temp_data(addSurfaceData * x) { temp_data = x; };
    void clear_temp_data() { free(temp_data); };
    void print_debug_report(std::string);

private:

    // A p4est
    p4est_t * p4est;

    // The data structure in p4est
    p4estData * forestData;

    // This structure records the connectivity of the p4est quadrants
    p4est_connectivity_t * connectivity;

    // Node numbering
    std::vector<long> nodeNumbering;

    // Pointer that records the location of a temporary data structure
    void * temp_data;

    // This is a modified version of the p4est library function new_connectivity
p4est_connectivity_t *
new_rectangle_connectivity(int mi, int ni, int periodic_a, int periodic_b, 
    double x0, double x1, double y0, double y1);

protected:
    virtual dim_t getNumNodes() const;
    virtual dim_t getNumElements() const;
    virtual dim_t getNumFaceElements() const;
    virtual dim_t getNumDOF() const;
    void updateNodeNumbering() const;
    // virtual dim_t getNumDOFInAxis(unsigned axis) const;
    // virtual index_t getFirstInDim(unsigned axis) const;
    // virtual IndexVector getDiagonalIndices(bool upperOnly) const;
    bool isBoundaryNode(p4est_quadrant_t * quad, int n, p4est_topidx_t treeid, p4est_qcoord_t length) const;
    bool isUpperBoundaryNode(p4est_quadrant_t * quad, int n, p4est_topidx_t treeid, p4est_qcoord_t length) const;
    bool isHangingNode(p4est_lnodes_code_t face_code, int n) const;
    virtual void assembleCoordinates(escript::Data& arg) const;
    virtual void assembleGradient(escript::Data& out, const escript::Data& in) const;
    // virtual void assembleIntegrate(std::vector<real_t>& integrals, const escript::Data& arg) const;
    // virtual void assembleIntegrate(std::vector<cplx_t>& integrals, const escript::Data& arg) const;
    virtual std::vector<IndexVector> getConnections(bool includeShared=false) const;
#ifdef ESYS_HAVE_TRILINOS
    virtual esys_trilinos::const_TrilinosGraph_ptr getTrilinosGraph() const;
#endif
#ifdef ESYS_HAVE_PASO
    virtual paso::SystemMatrixPattern_ptr getPasoMatrixPattern(bool reducedRowOrder, bool reducedColOrder) const;
#endif
    virtual void interpolateNodesOnElements(escript::Data& out, const escript::Data& in, bool reduced) const;   
    virtual void interpolateNodesOnFaces(escript::Data& out, const escript::Data& in, bool reduced) const;
    virtual void nodesToDOF(escript::Data& out, const escript::Data& in) const;
    virtual dim_t getDofOfNode(dim_t node) const;
    virtual void populateSampleIds();
    virtual void populateDofMap();

    template <typename S>
    void interpolateNodesOnElementsWorker(escript::Data& out,
                                  const escript::Data& in, bool reduced, S sentinel) const;   
    template <typename S>
    void interpolateNodesOnFacesWorker(escript::Data& out,
                                         const escript::Data& in,
                                         bool reduced, S sentinel) const;  

    template<typename Scalar>
    void assembleGradientImpl(escript::Data& out,
                              const escript::Data& in) const;

    template<typename Scalar> void addToMatrixAndRHS(escript::AbstractSystemMatrix* S, escript::Data& F,
           const std::vector<Scalar>& EM_S, const std::vector<Scalar>& EM_F,
           bool addS, bool addF, index_t firstNode, int nEq=1, int nComp=1) const;

    // Updates m_faceOffset for each quadrant
    void updateFaceOffset();

#ifdef ESYS_HAVE_PASO
    // the Paso System Matrix pattern
    mutable paso::SystemMatrixPattern_ptr m_pattern;
#endif

#ifdef ESYS_HAVE_TRILINOS
    /// Trilinos graph structure, cached for efficiency
    mutable esys_trilinos::const_TrilinosGraph_ptr m_graph;
#endif

    IndexVector getNodeDistribution() const;

};


typedef POINTER_WRAPPER_CLASS(Rectangle) OxleyDomainRect_ptr;

} //end namespace


#endif //__OXLEY_RECTANGLE_H__
