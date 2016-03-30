
/*****************************************************************************
*
* Copyright (c) 2016 by The University of Queensland
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

#include <trilinoswrap/PreconditionerFactory.h>
#include <trilinoswrap/TrilinosAdapterException.h>

#include <escript/SolverOptions.h>

#include <Ifpack2_Factory.hpp>
#include <MueLu_CreateTpetraPreconditioner.hpp>

using Teuchos::RCP;

namespace esys_trilinos {

template<typename ST>
RCP<OpType<ST> > createPreconditioner(RCP<MatrixType<ST> > mat,
                                      const escript::SolverBuddy& sb)
{
    RCP<Teuchos::ParameterList> params = Teuchos::parameterList();
    Ifpack2::Factory factory;
    RCP<OpType<ST> > prec;
    RCP<Ifpack2::Preconditioner<ST,LO,GO,NT> > ifprec;

    // TODO: options!
    switch (sb.getPreconditioner()) {
        case escript::SO_PRECONDITIONER_NONE:
            break;
        case escript::SO_PRECONDITIONER_AMG:
            {
                params->set("max levels", sb.getLevelMax());
                params->set("number of equations", 1);
                params->set("cycle type", sb.getCycleType()==1 ? "V" : "W");
                params->set("problem: symmetric", sb.isSymmetric());
                params->set("verbosity", sb.isVerbose()? "high":"low");
                RCP<OpType<ST> > A(mat);
                prec = MueLu::CreateTpetraPreconditioner(A, *params);
            }
            break;
        case escript::SO_PRECONDITIONER_ILUT:
            ifprec = factory.create<MatrixType<ST> >("ILUT", mat);
            params->set("fact: drop tolerance", sb.getDropTolerance());
            break;
        case escript::SO_PRECONDITIONER_GAUSS_SEIDEL:
        case escript::SO_PRECONDITIONER_JACOBI:
            ifprec = factory.create<MatrixType<ST> >("RELAXATION", mat);
            if (sb.getPreconditioner() == escript::SO_PRECONDITIONER_JACOBI) {
                params->set("relaxation: type", "Jacobi");
            } else {
                params->set("relaxation: type", (sb.isSymmetric() ?
                            "Symmetric Gauss-Seidel" : "Gauss-Seidel"));
            }
            params->set("relaxation: sweeps", sb.getNumSweeps());
            params->set("relaxation: damping factor", sb.getRelaxationFactor());
            break;
        case escript::SO_PRECONDITIONER_RILU:
            ifprec = factory.create<MatrixType<ST> >("RILUK", mat);
            params->set("fact: relax value", sb.getRelaxationFactor());
            break;
        default:
            throw escript::ValueError("Unsupported preconditioner requested.");
    }
    if (!ifprec.is_null()) {
        ifprec->setParameters(*params);
        ifprec->initialize();
        ifprec->compute();
        prec = ifprec;
    }
    return prec;
}

// instantiate our two supported versions
template
RCP<RealOperator> createPreconditioner<real_t>(RCP<RealMatrix> mat,
                                               const escript::SolverBuddy& sb);
template
RCP<ComplexOperator> createPreconditioner<cplx_t>(RCP<ComplexMatrix> mat,
                                               const escript::SolverBuddy& sb);

}  // end of namespace

