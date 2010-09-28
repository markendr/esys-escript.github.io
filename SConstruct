########################################################
#
# Copyright (c) 2003-2010 by University of Queensland
# Earth Systems Science Computational Center (ESSCC)
# http://www.uq.edu.au/esscc
#
# Primary Business: Queensland, Australia
# Licensed under the Open Software License version 3.0
# http://www.opensource.org/licenses/osl-3.0.php
#
########################################################

EnsureSConsVersion(0,96,91)
EnsurePythonVersion(2,5)

import sys, os, platform, re
from distutils import sysconfig
from site_init import *

# Version number to check for in options file. Increment when new features are
# added or existing options changed.
REQUIRED_OPTS_VERSION=200

# MS Windows support, many thanks to PH
IS_WINDOWS = (os.name == 'nt')

########################## Determine options file ############################
# 1. command line
# 2. scons/<hostname>_options.py
# 3. name as part of a cluster
options_file=ARGUMENTS.get('options_file', None)
if not options_file:
    ext_dir = os.path.join(os.getcwd(), 'scons')
    hostname = platform.node().split('.')[0]
    for name in hostname, effectiveName(hostname):
        mangledhostname = re.sub('[^0-9a-zA-Z]', '_', hostname)
        options_file = os.path.join(ext_dir, mangledhostname+'_options.py')
        if os.path.isfile(options_file): break

if not os.path.isfile(options_file):
    print("\nWARNING:\nOptions file %s" % options_file)
    print("not found! Default options will be used which is most likely suboptimal.")
    print("It is recommended that you copy one of the TEMPLATE files in the scons/")
    print("subdirectory and customize it to your needs.\n")
    options_file = None

######################## SCons compatibility stuff ###########################

# Call additional SConscript
# scons <  0.98: build_dir, BuildDir()
# scons >= 0.98: variant_dir, VariantDir()
import SCons
scons_ver=SCons.__version__.split('.')
cantusevariantdir=float(scons_ver[0]+'.'+scons_ver[1])<0.98

def CallSConscript(obj, **kw):
    if cantusevariantdir:
        if 'variant_dir' in kw:
            kw['build_dir']=kw['variant_dir']
            del kw['variant_dir']
    obj.SConscript(**kw)

# Prepare user-settable variables
# scons <= 0.98.0: Options
# scons >= 0.98.1: Variables
unknown_vars=None
try:
    vars = Variables(options_file, ARGUMENTS)
    adder = vars.AddVariables
    unknown_vars = vars.UnknownVariables
except:
    vars = Options(options_file, ARGUMENTS)
    adder = vars.AddOptions
    if 'UnknownOptions' in dir(vars):
        unknown_vars = vars.UnknownOptions
    BoolVariable = BoolOption
    EnumVariable = EnumOption
    PackageVariable = PackageOption
    PathVariable = PathOption

############################### build options ################################

default_prefix='/usr'
mpi_flavours=('none', 'MPT', 'MPICH', 'MPICH2', 'OPENMPI', 'INTELMPI')
lapack_flavours=('none', 'clapack', 'mkl')

adder(
  PathVariable('options_file', 'Path to options file', options_file, PathVariable.PathIsFile),
  PathVariable('prefix', 'Installation prefix', Dir('#.').abspath, PathVariable.PathIsDirCreate),
  BoolVariable('verbose', 'Output full compile/link lines', False),
# Compiler/Linker options
  ('cc', 'Path to C compiler', 'default'),
  ('cxx', 'Path to C++ compiler', 'default'),
  ('cc_flags', 'Base C/C++ compiler flags', 'default'),
  ('cc_optim', 'Additional C/C++ flags for a non-debug build', 'default'),
  ('cc_debug', 'Additional C/C++ flags for a debug build', 'default'),
  ('cc_extra', 'Extra C compiler flags', ''),
  ('cxx_extra', 'Extra C++ compiler flags', ''),
  ('ld_extra', 'Extra linker flags', ''),
  BoolVariable('werror','Treat compiler warnings as errors', True),
  BoolVariable('debug', 'Compile with debug flags', False),
  BoolVariable('openmp', 'Compile parallel version using OpenMP', False),
  ('omp_flags', 'OpenMP compiler flags', 'default'),
  ('omp_ldflags', 'OpenMP linker flags', 'default'),
# Mandatory libraries
  EnumVariable('mpi', 'Compile parallel version using MPI flavour', 'none', allowed_values=mpi_flavours),
  ('mpi_prefix', 'Prefix/Paths of MPI installation', default_prefix),
  ('mpi_libs', 'MPI shared libraries to link with', ['mpi']),
  ('boost_prefix', 'Prefix/Paths of boost installation', default_prefix),
  ('boost_libs', 'Boost libraries to link with', ['boost_python']),
# Optional libraries
  BoolVariable('netcdf', 'Enable netCDF file support', False),
  ('netcdf_prefix', 'Prefix/Paths of netCDF installation', default_prefix),
  ('netcdf_libs', 'netCDF libraries to link with', ['netcdf_c++', 'netcdf']),
  BoolVariable('parmetis', 'Enable ParMETIS (requires MPI)', False),
  ('parmetis_prefix', 'Prefix/Paths of ParMETIS installation', default_prefix),
  ('parmetis_libs', 'ParMETIS libraries to link with', ['parmetis', 'metis']),
  BoolVariable('papi', 'Enable PAPI', False),
  ('papi_prefix', 'Prefix/Paths to PAPI installation', default_prefix),
  ('papi_libs', 'PAPI libraries to link with', ['papi']),
  BoolVariable('papi_instrument_solver', 'Use PAPI to instrument each iteration of the solver', False),
  BoolVariable('mkl', 'Enable the Math Kernel Library', False),
  ('mkl_prefix', 'Prefix/Paths to MKL installation', default_prefix),
  ('mkl_libs', 'MKL libraries to link with', ['mkl_solver','mkl_em64t','guide','pthread']),
  BoolVariable('umfpack', 'Enable UMFPACK', False),
  ('umfpack_prefix', 'Prefix/Paths to UMFPACK installation', default_prefix),
  ('umfpack_libs', 'UMFPACK libraries to link with', ['umfpack']),
  EnumVariable('lapack', 'Set LAPACK flavour', 'none', allowed_values=lapack_flavours),
  ('lapack_prefix', 'Prefix/Paths to LAPACK installation', default_prefix),
  ('lapack_libs', 'LAPACK libraries to link with', []),
  BoolVariable('silo', 'Enable the Silo file format in weipa', False),
  ('silo_prefix', 'Prefix/Paths to Silo installation', default_prefix),
  ('silo_libs', 'Silo libraries to link with', ['siloh5', 'hdf5']),
  BoolVariable('visit', 'Enable the VisIt simulation interface', False),
  ('visit_prefix', 'Prefix/Paths to VisIt installation', default_prefix),
  ('visit_libs', 'VisIt libraries to link with', ['simV2']),
  BoolVariable('pyvisi', 'Enable pyvisi (deprecated, requires VTK module)', False),
# Advanced settings
  # To enable passing function pointers through python
  BoolVariable('iknowwhatimdoing', 'Allow non-standard C', False),
  # An option for specifying the compiler tools (see windows branch)
  ('tools_names', 'Compiler tools to use', ['default']),
  ('env_export', 'Environment variables to be passed to tools',[]),
  EnumVariable('forcelazy', 'For testing use only - set the default value for autolazy', 'leave_alone', allowed_values=('leave_alone', 'on', 'off')),
  EnumVariable('forcecollres', 'For testing use only - set the default value for force resolving collective ops', 'leave_alone', allowed_values=('leave_alone', 'on', 'off')),
  # finer control over library building, intel aggressive global optimisation
  # works with dynamic libraries on windows.
  ('share_esysutils', 'Build a dynamic esysUtils library', False),
  ('share_paso', 'Build a dynamic paso library', False),
  ('sys_libs', 'Extra libraries to link with', []),
  ('escript_opts_version', 'Version of options file (do not specify on command line)'),
)

##################### Create environment and help text #######################

# Intel's compiler uses regular expressions improperly and emits a warning
# about failing to find the compilers. This warning can be safely ignored.

env = Environment(tools = ['default'], options = vars)
if env['tools_names'] != 'default':
    env = Environment(tools = ['default'] + env['tools_names'], options = vars)

if options_file:
    opts_valid=False
    if 'escript_opts_version' in env.Dictionary() and \
        int(env['escript_opts_version']) >= REQUIRED_OPTS_VERSION:
            opts_valid=True
    if opts_valid:
        print("Using options in %s." % options_file)
    else:
        print("\nOptions file %s" % options_file)
        print("is outdated! Please update the file by examining one of the TEMPLATE")
        print("files in the scons/ subdirectory and setting escript_opts_version to %d.\n"%REQUIRED_OPTS_VERSION)
        Exit(1)

# Generate help text (scons -h)
Help(vars.GenerateHelpText(env))

# Check for superfluous options if scons supports it
if unknown_vars:
    for k in unknown_vars():
        print("WARNING: Ignoring unknown option '%s'" % k)

#################### Make sure install directories exist #####################

prefix=Dir(env['prefix']).abspath
env['incinstall'] = os.path.join(prefix, 'include')
env['bininstall'] = os.path.join(prefix, 'bin')
env['libinstall'] = os.path.join(prefix, 'lib')
env['pyinstall']  = os.path.join(prefix, 'esys')
if not os.path.isdir(env['bininstall']):
    os.makedirs(env['bininstall'])
if not os.path.isdir(env['libinstall']):
    os.makedirs(env['libinstall'])
if not os.path.isdir(env['pyinstall']):
    os.makedirs(env['pyinstall'])

env.Append(CPPPATH = [env['incinstall']])
env.Append(LIBPATH = [env['libinstall']])

################# Fill in compiler options if not set above ##################

if env['cc'] != 'default': env['CC']=env['cc']
if env['cxx'] != 'default': env['CXX']=env['cxx']

# version >=9 of intel C++ compiler requires use of icpc to link in C++
# runtimes (icc does not)
if not IS_WINDOWS and os.uname()[4]=='ia64' and env['CXX']=='icpc':
    env['LINK'] = env['CXX']

# default compiler/linker options
cc_flags = ''
cc_optim = ''
cc_debug = ''
omp_flags = ''
omp_ldflags = ''
fatalwarning = '' # switch to turn warnings into errors
sysheaderopt = '' # how to indicate that a header is a system header

# env['CC'] might be a full path
cc_name=os.path.basename(env['CC'])

if cc_name == 'icc':
    # Intel compiler
    cc_flags    = "-std=c99 -fPIC -wd161 -w1 -vec-report0 -DBLOCKTIMER -DCORE_ID1"
    cc_optim    = "-O3 -ftz -IPF_ftlacc- -IPF_fma -fno-alias -ip"
    cc_debug    = "-g -O0 -DDOASSERT -DDOPROF -DBOUNDS_CHECK"
    omp_flags   = "-openmp -openmp_report0"
    omp_ldflags = "-openmp -openmp_report0 -lguide -lpthread"
    fatalwarning = "-Werror"
elif cc_name[:3] == 'gcc':
    # GNU C on any system
    cc_flags     = "-pedantic -Wall -fPIC -ffast-math -Wno-unknown-pragmas -DBLOCKTIMER  -Wno-sign-compare -Wno-system-headers -Wno-long-long -Wno-strict-aliasing -finline-functions"
    cc_optim     = "-O3"
    cc_debug     = "-g -O0 -DDOASSERT -DDOPROF -DBOUNDS_CHECK"
    omp_flags    = "-fopenmp"
    omp_ldflags  = "-fopenmp"
    fatalwarning = "-Werror"
    sysheaderopt = "-isystem"
elif cc_name == 'cl':
    # Microsoft Visual C on Windows
    cc_flags     = "/EHsc /GR /MD /wd4068 -D_USE_MATH_DEFINES -DDLL_NETCDF"
    cc_optim     = "/O2 /Op /MT /W3"
    cc_debug     = "/Od /RTCcsu /MTd /ZI -DBOUNDS_CHECK"
    fatalwarning = "/WX"
elif cc_name == 'icl':
    # Intel C on Windows
    cc_flags     = '/EHsc /GR /MD'
    cc_optim     = '/fast /Oi /W3 /Qssp /Qinline-factor- /Qinline-min-size=0 /Qunroll'
    cc_debug     = '/Od /RTCcsu /Zi /Y- /debug:all /Qtrapuv'
    omp_flags    = '/Qvec-report0 /Qopenmp /Qopenmp-report0 /Qparallel'
    omp_ldflags  = '/Qvec-report0 /Qopenmp /Qopenmp-report0 /Qparallel'

# set defaults if not otherwise specified
if env['cc_flags']    == 'default': env['cc_flags'] = cc_flags
if env['cc_optim']    == 'default': env['cc_optim'] = cc_optim
if env['cc_debug']    == 'default': env['cc_debug'] = cc_debug
if env['omp_flags']   == 'default': env['omp_flags'] = omp_flags
if env['omp_ldflags'] == 'default': env['omp_ldflags'] = omp_ldflags
if env['cc_extra']  != '': env.Append(CFLAGS = env['cc_extra'])
if env['cxx_extra'] != '': env.Append(CXXFLAGS = env['cxx_extra'])
if env['ld_extra']  != '': env.Append(LINKFLAGS = env['ld_extra'])

# set up the autolazy values
if env['forcelazy'] == 'on':
    env.Append(CPPDEFINES=['FAUTOLAZYON'])
elif env['forcelazy'] == 'off':
    env.Append(CPPDEFINES=['FAUTOLAZYOFF'])

# set up the collective resolve values
if env['forcecollres'] == 'on':
    env.Append(CPPDEFINES=['FRESCOLLECTON'])
elif env['forcecollres'] == 'off':
    env.Append(CPPDEFINES=['FRESCOLLECTOFF'])

# allow non-standard C if requested
if env['iknowwhatimdoing']:
    env.Append(CPPDEFINES=['IKNOWWHATIMDOING'])

# Disable OpenMP if no flags provided
if env['openmp'] and env['omp_flags'] == '':
   print("OpenMP requested but no flags provided - disabling OpenMP!")
   env['openmp'] = False

if env['openmp']:
    env.Append(CCFLAGS = env['omp_flags'])
    if env['omp_ldflags'] != '': env.Append(LINKFLAGS = env['omp_ldflags'])
else:
    env['omp_flags']=''
    env['omp_ldflags']=''

# add debug/non-debug compiler flags
if env['debug']:
    env.Append(CCFLAGS = env['cc_debug'])
else:
    env.Append(CCFLAGS = env['cc_optim'])

# always add cc_flags
env.Append(CCFLAGS = env['cc_flags'])

# Get the global Subversion revision number for the getVersion() method
try:
    global_revision = os.popen('svnversion -n .').read()
    global_revision = re.sub(':.*', '', global_revision)
    global_revision = re.sub('[^0-9]', '', global_revision)
    if global_revision == '': global_revision='-2'
except:
    global_revision = '-1'
env.Append(CPPDEFINES=['SVN_VERSION='+global_revision])

if IS_WINDOWS:
    if not env['share_esysutils']:
        env.Append(CPPDEFINES = ['ESYSUTILS_STATIC_LIB'])
    if not env['share_paso']:
        env.Append(CPPDEFINES = ['PASO_STATIC_LIB'])

###################### Copy required environment vars ########################

# Windows doesn't use LD_LIBRARY_PATH but PATH instead
if IS_WINDOWS:
    LD_LIBRARY_PATH_KEY='PATH'
    env['ENV']['LD_LIBRARY_PATH']=''
else:
    LD_LIBRARY_PATH_KEY='LD_LIBRARY_PATH'

# the following env variables are exported for the unit tests, PATH is needed
# so the compiler/linker is found if they are not in default locations.

for key in 'OMP_NUM_THREADS', 'ESCRIPT_NUM_PROCS', 'ESCRIPT_NUM_NODES':
    try:
        env['ENV'][key] = os.environ[key]
    except KeyError:
        env['ENV'][key] = 1

env_export=env['env_export']
env_export.extend(['ESCRIPT_NUM_THREADS','ESCRIPT_HOSTFILE','DISPLAY','XAUTHORITY','PATH'])

for key in set(env_export):
    try:
        env['ENV'][key] = os.environ[key]
    except KeyError:
        pass

try:
    env.PrependENVPath(LD_LIBRARY_PATH_KEY, os.environ[LD_LIBRARY_PATH_KEY])
except KeyError:
    pass

#for key in 'PATH','C_INCLUDE_PATH','CPLUS_INCLUDE_PATH','LIBRARY_PATH':
#    try:
#        env['ENV'][key] = os.environ[key]
#    except KeyError:
#        pass
#
try:
    env['ENV']['PYTHONPATH'] = os.environ['PYTHONPATH']
except KeyError:
    pass

######################## Add some custom builders ############################

py_builder = Builder(action = build_py, suffix = '.pyc', src_suffix = '.py', single_source=True)
env.Append(BUILDERS = {'PyCompile' : py_builder});

runUnitTest_builder = Builder(action = runUnitTest, suffix = '.passed', src_suffix=env['PROGSUFFIX'], single_source=True)
env.Append(BUILDERS = {'RunUnitTest' : runUnitTest_builder});

runPyUnitTest_builder = Builder(action = runPyUnitTest, suffix = '.passed', src_suffic='.py', single_source=True)
env.Append(BUILDERS = {'RunPyUnitTest' : runPyUnitTest_builder});

epstopdfbuilder = Builder(action = eps2pdf, suffix='.pdf', src_suffix='.eps', single_source=True)
env.Append(BUILDERS = {'EpsToPDF' : epstopdfbuilder});

############################ Dependency checks ###############################

# Create a Configure() environment to check for compilers and python
conf = Configure(clone_env(env))

######## Test that the compilers work

if 'CheckCC' in dir(conf): # exists since scons 1.1.0
    if not conf.CheckCC():
        print("Cannot run C compiler '%s' (check config.log)" % (env['CC']))
        Exit(1)
    if not conf.CheckCXX():
        print("Cannot run C++ compiler '%s' (check config.log)" % (env['CXX']))
        Exit(1)
else:
    if not conf.CheckFunc('printf', language='c'):
        print("Cannot run C compiler '%s' (check config.log)" % (env['CC']))
        Exit(1)
    if not conf.CheckFunc('printf', language='c++'):
        print("Cannot run C++ compiler '%s' (check config.log)" % (env['CXX']))
        Exit(1)

if conf.CheckFunc('gethostname'):
  conf.env.Append(CPPDEFINES = ['HAVE_GETHOSTNAME'])

######## Python headers & library (required)

python_inc_path=sysconfig.get_python_inc()
python_lib_path=sysconfig.get_config_var('LIBDIR')
#python_libs=[sysconfig.get_config_var('LDLIBRARY')] #not on darwin
python_libs=['python'+sysconfig.get_python_version()]

if sysheaderopt == '':
    conf.env.AppendUnique(CPPPATH = [python_inc_path])
else:
    conf.env.Append(CCFLAGS = [sysheaderopt, python_inc_path])

conf.env.AppendUnique(LIBPATH = [python_lib_path])
conf.env.AppendUnique(LIBS = python_libs)
# The wrapper script needs to find the libs
conf.env.PrependENVPath(LD_LIBRARY_PATH_KEY, python_lib_path)

if not conf.CheckCHeader('Python.h'):
    print("Cannot find python include files (tried 'Python.h' in directory %s)" % (python_inc_path))
    Exit(1)
if not conf.CheckFunc('Py_Exit'):
    print("Cannot find python library method Py_Main (tried %s in directory %s)" % (python_libs, python_lib_path))
    Exit(1)

# Commit changes to environment
env = conf.Finish()

######## boost (required)

boost_inc_path,boost_lib_path=findLibWithHeader(env, env['boost_libs'], 'boost/python.hpp', env['boost_prefix'], lang='c++')
if sysheaderopt == '':
    env.AppendUnique(CPPPATH = [boost_inc_path])
else:
    # This is required because we can't -isystem /usr/include since it breaks
    # std includes
    if os.path.normpath(boost_inc_path) == '/usr/include':
        conf.env.Append(CCFLAGS=[sysheaderopt, os.path.join(boost_inc_path,'boost')])
    else:
        env.Append(CCFLAGS=[sysheaderopt, boost_inc_path])

env.AppendUnique(LIBPATH = [boost_lib_path])
env.AppendUnique(LIBS = env['boost_libs'])
env.PrependENVPath(LD_LIBRARY_PATH_KEY, boost_lib_path)

######## numpy (required)

try:
    from numpy import identity
except ImportError:
    print("Cannot import numpy, you need to set your PYTHONPATH and probably %s"%LD_LIBRARY_PATH_KEY)
    Exit(1)

######## VTK (optional)

if env['pyvisi']:
    try:
        import vtk
        env['pyvisi'] = True
    except ImportError:
        env['pyvisi'] = False

######## netCDF (optional)

netcdf_inc_path=''
netcdf_lib_path=''
if env['netcdf']:
    netcdf_inc_path,netcdf_lib_path=findLibWithHeader(env, env['netcdf_libs'], 'netcdf.h', env['netcdf_prefix'], lang='c++')
    env.AppendUnique(CPPPATH = [netcdf_inc_path])
    env.AppendUnique(LIBPATH = [netcdf_lib_path])
    env.AppendUnique(LIBS = env['netcdf_libs'])
    env.PrependENVPath(LD_LIBRARY_PATH_KEY, netcdf_lib_path)
    env.Append(CPPDEFINES = ['USE_NETCDF'])

######## PAPI (optional)

papi_inc_path=''
papi_lib_path=''
if env['papi']:
    papi_inc_path,papi_lib_path=findLibWithHeader(env, env['papi_libs'], 'papi.h', env['papi_prefix'], lang='c')
    env.AppendUnique(CPPPATH = [papi_inc_path])
    env.AppendUnique(LIBPATH = [papi_lib_path])
    env.AppendUnique(LIBS = env['papi_libs'])
    env.PrependENVPath(LD_LIBRARY_PATH_KEY, papi_lib_path)
    env.Append(CPPDEFINES = ['BLOCKPAPI'])

######## MKL (optional)

mkl_inc_path=''
mkl_lib_path=''
if env['mkl']:
    mkl_inc_path,mkl_lib_path=findLibWithHeader(env, env['mkl_libs'], 'mkl_solver.h', env['mkl_prefix'], lang='c')
    env.AppendUnique(CPPPATH = [mkl_inc_path])
    env.AppendUnique(LIBPATH = [mkl_lib_path])
    env.AppendUnique(LIBS = env['mkl_libs'])
    env.PrependENVPath(LD_LIBRARY_PATH_KEY, mkl_lib_path)
    env.Append(CPPDEFINES = ['MKL'])

######## UMFPACK (optional)

umfpack_inc_path=''
umfpack_lib_path=''
if env['umfpack']:
    umfpack_inc_path,umfpack_lib_path=findLibWithHeader(env, env['umfpack_libs'], 'umfpack.h', env['umfpack_prefix'], lang='c')
    env.AppendUnique(CPPPATH = [umfpack_inc_path])
    env.AppendUnique(LIBPATH = [umfpack_lib_path])
    env.AppendUnique(LIBS = env['umfpack_libs'])
    env.PrependENVPath(LD_LIBRARY_PATH_KEY, umfpack_lib_path)
    env.Append(CPPDEFINES = ['UMFPACK'])

######## LAPACK (optional)

if env['lapack']=='mkl' and not env['mkl']:
    print("mkl_lapack requires MKL!")
    Exit(1)

env['uselapack'] = env['lapack']!='none'
lapack_inc_path=''
lapack_lib_path=''
if env['uselapack']:
    header='clapack.h'
    if env['lapack']=='mkl':
        env.AppendUnique(CPPDEFINES = ['MKL_LAPACK'])
        header='mkl_lapack.h'
    lapack_inc_path,lapack_lib_path=findLibWithHeader(env, env['lapack_libs'], header, env['lapack_prefix'], lang='c')
    env.AppendUnique(CPPPATH = [lapack_inc_path])
    env.AppendUnique(LIBPATH = [lapack_lib_path])
    env.AppendUnique(LIBS = env['lapack_libs'])
    env.Append(CPPDEFINES = ['USE_LAPACK'])

######## Silo (optional)

silo_inc_path=''
silo_lib_path=''
if env['silo']:
    silo_inc_path,silo_lib_path=findLibWithHeader(env, env['silo_libs'], 'silo.h', env['silo_prefix'], lang='c')
    env.AppendUnique(CPPPATH = [silo_inc_path])
    env.AppendUnique(LIBPATH = [silo_lib_path])
    # Note that we do not add the libs since they are only needed for the
    # weipa library and tools.
    #env.AppendUnique(LIBS = [env['silo_libs']])

######## VisIt (optional)

visit_inc_path=''
visit_lib_path=''
if env['visit']:
    visit_inc_path,visit_lib_path=findLibWithHeader(env, env['visit_libs'], 'VisItControlInterface_V2.h', env['visit_prefix'], lang='c')
    env.AppendUnique(CPPPATH = [visit_inc_path])
    env.AppendUnique(LIBPATH = [visit_lib_path])

######## MPI (optional)

env['usempi'] = env['mpi']!='none'

# Create a modified environment for MPI programs (identical to env if mpi=none)
env_mpi = clone_env(env)

mpi_inc_path=''
mpi_lib_path=''
if env_mpi['usempi']:
    mpi_inc_path,mpi_lib_path=findLibWithHeader(env_mpi, env['mpi_libs'], 'mpi.h', env['mpi_prefix'], lang='c')
    env_mpi.AppendUnique(CPPPATH = [mpi_inc_path])
    env_mpi.AppendUnique(LIBPATH = [mpi_lib_path])
    env_mpi.AppendUnique(LIBS = env['mpi_libs'])
    env_mpi.PrependENVPath(LD_LIBRARY_PATH_KEY, mpi_lib_path)
    env_mpi.Append(CPPDEFINES = ['PASO_MPI', 'MPI_NO_CPPBIND', 'MPICH_IGNORE_CXX_SEEK'])
    # NetCDF 4.1 defines MPI_Comm et al. if MPI_INCLUDED is not defined!
    # On the other hand MPT and OpenMPI don't define the latter so we have to
    # do that here
    if env['netcdf'] and env_mpi['mpi'] in ['MPT','OPENMPI']:
        env_mpi.Append(CPPDEFINES = ['MPI_INCLUDED'])


######## ParMETIS (optional)

if not env_mpi['usempi']: env_mpi['parmetis'] = False

parmetis_inc_path=''
parmetis_lib_path=''
if env_mpi['parmetis']:
    parmetis_inc_path,parmetis_lib_path=findLibWithHeader(env_mpi, env['parmetis_libs'], 'parmetis.h', env['parmetis_prefix'], lang='c')
    env_mpi.AppendUnique(CPPPATH = [parmetis_inc_path])
    env_mpi.AppendUnique(LIBPATH = [parmetis_lib_path])
    env_mpi.AppendUnique(LIBS = env_mpi['parmetis_libs'])
    env_mpi.PrependENVPath(LD_LIBRARY_PATH_KEY, parmetis_lib_path)
    env_mpi.Append(CPPDEFINES = ['USE_PARMETIS'])

env['parmetis'] = env_mpi['parmetis']

######################## Summarize our environment ###########################

# keep some of our install paths first in the list for the unit tests
env.PrependENVPath(LD_LIBRARY_PATH_KEY, env['libinstall'])
env.PrependENVPath('PYTHONPATH', prefix)
env['ENV']['ESCRIPT_ROOT'] = prefix

if not env['verbose']:
    for e in env, env_mpi:
        e['CCCOMSTR'] = "Compiling $TARGET"
        e['CXXCOMSTR'] = "Compiling $TARGET"
        e['SHCCCOMSTR'] = "Compiling $TARGET"
        e['SHCXXCOMSTR'] = "Compiling $TARGET"
        e['ARCOMSTR'] = "Linking $TARGET"
        e['LINKCOMSTR'] = "Linking $TARGET"
        e['SHLINKCOMSTR'] = "Linking $TARGET"
        #Progress(['Checking -\r', 'Checking \\\r', 'Checking |\r', 'Checking /\r'], interval=17)

print("")
print("*** Config Summary (see config.log and lib/buildvars for details) ***")
print("Escript/Finley revision %s"%global_revision)
print("  Install prefix:  %s"%env['prefix'])
print("          Python:  %s"%sysconfig.PREFIX)
print("           boost:  %s"%env['boost_prefix'])
print("           numpy:  YES")
if env['usempi']:
    print("             MPI:  YES (flavour: %s)"%env['mpi'])
else:
    print("             MPI:  DISABLED")
if env['uselapack']:
    print("          LAPACK:  YES (flavour: %s)"%env['lapack'])
else:
    print("          LAPACK:  DISABLED")
d_list=[]
e_list=[]
for i in 'debug','openmp','netcdf','parmetis','papi','mkl','umfpack','silo','visit','pyvisi':
    if env[i]: e_list.append(i)
    else: d_list.append(i)
for i in e_list:
    print("%16s:  YES"%i)
for i in d_list:
    print("%16s:  DISABLED"%i)
if ((fatalwarning != '') and (env['werror'])):
    print("  Treating warnings as errors")
else:
    print("  NOT treating warnings as errors")
print("")

####################### Configure the subdirectories #########################

from grouptest import *

TestGroups=[]

# keep an environment without warnings-as-errors
dodgy_env=clone_env(env_mpi)

# now add warnings-as-errors flags. This needs to be done after configuration
# because the scons test files have warnings in them
if ((fatalwarning != '') and (env['werror'])):
    env.Append(CCFLAGS = fatalwarning)
    env_mpi.Append(CCFLAGS = fatalwarning)

Export(
  ['env',
   'env_mpi',
   'clone_env',
   'dodgy_env',
   'IS_WINDOWS',
   'TestGroups',
   'CallSConscript',
   'cantusevariantdir'
  ]
)

CallSConscript(env, dirs = ['tools/CppUnitTest/src'], variant_dir='build/$PLATFORM/tools/CppUnitTest', duplicate=0)
CallSConscript(env, dirs = ['tools/escriptconvert'], variant_dir='build/$PLATFORM/tools/escriptconvert', duplicate=0)
CallSConscript(env, dirs = ['paso/src'], variant_dir='build/$PLATFORM/paso', duplicate=0)
CallSConscript(env, dirs = ['weipa/src'], variant_dir='build/$PLATFORM/weipa', duplicate=0)
CallSConscript(env, dirs = ['escript/src'], variant_dir='build/$PLATFORM/escript', duplicate=0)
CallSConscript(env, dirs = ['esysUtils/src'], variant_dir='build/$PLATFORM/esysUtils', duplicate=0)
CallSConscript(env, dirs = ['finley/src'], variant_dir='build/$PLATFORM/finley', duplicate=0)
CallSConscript(env, dirs = ['modellib/py_src'], variant_dir='build/$PLATFORM/modellib', duplicate=0)
CallSConscript(env, dirs = ['doc'], variant_dir='build/$PLATFORM/doc', duplicate=0)
CallSConscript(env, dirs = ['pyvisi/py_src'], variant_dir='build/$PLATFORM/pyvisi', duplicate=0)
CallSConscript(env, dirs = ['pycad/py_src'], variant_dir='build/$PLATFORM/pycad', duplicate=0)
CallSConscript(env, dirs = ['pythonMPI/src'], variant_dir='build/$PLATFORM/pythonMPI', duplicate=0)
CallSConscript(env, dirs = ['scripts'], variant_dir='build/$PLATFORM/scripts', duplicate=0)
CallSConscript(env, dirs = ['paso/profiling'], variant_dir='build/$PLATFORM/paso/profiling', duplicate=0)

######################## Populate the buildvars file #########################

# remove obsolete file
if not env['usempi']:
    Execute(Delete(os.path.join(env['libinstall'], 'pythonMPI')))
    Execute(Delete(os.path.join(env['libinstall'], 'pythonMPIredirect')))

# Try to extract the boost version from version.hpp
boosthpp=open(os.path.join(boost_inc_path, 'boost', 'version.hpp'))
boostversion='unknown'
try:
    for line in boosthpp:
        ver=re.match(r'#define BOOST_VERSION (\d+)',line)
        if ver:
            boostversion=ver.group(1)
except StopIteration:
    pass
boosthpp.close()

buildvars=open(os.path.join(env['libinstall'], 'buildvars'), 'w')
buildvars.write("svn_revision="+str(global_revision)+"\n")
buildvars.write("prefix="+prefix+"\n")
buildvars.write("cc="+env['CC']+"\n")
buildvars.write("cxx="+env['CXX']+"\n")
buildvars.write("python="+sys.executable+"\n")
buildvars.write("python_version="+str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2])+"\n")
buildvars.write("boost_inc_path="+boost_inc_path+"\n")
buildvars.write("boost_lib_path="+boost_lib_path+"\n")
buildvars.write("boost_version="+boostversion+"\n")
buildvars.write("debug=%d\n"%int(env['debug']))
buildvars.write("openmp=%d\n"%int(env['openmp']))
buildvars.write("mpi=%s\n"%env['mpi'])
buildvars.write("mpi_inc_path=%s\n"%mpi_inc_path)
buildvars.write("mpi_lib_path=%s\n"%mpi_lib_path)
buildvars.write("lapack=%s\n"%env['lapack'])
buildvars.write("pyvisi=%d\n"%env['pyvisi'])
for i in 'netcdf','parmetis','papi','mkl','umfpack','silo','visit':
    buildvars.write("%s=%d\n"%(i, int(env[i])))
    if env[i]:
        buildvars.write("%s_inc_path=%s\n"%(i, eval(i+'_inc_path')))
        buildvars.write("%s_lib_path=%s\n"%(i, eval(i+'_lib_path')))
buildvars.close()

################### Targets to build and install libraries ###################

target_init = env.Command(env['pyinstall']+'/__init__.py', None, Touch('$TARGET'))
env.Alias('target_init', [target_init])

# The headers have to be installed prior to build in order to satisfy
# #include <paso/Common.h>
env.Alias('build_esysUtils', ['target_install_esysUtils_headers', 'target_esysUtils_a'])
env.Alias('install_esysUtils', ['build_esysUtils', 'target_install_esysUtils_a'])

env.Alias('build_paso', ['target_install_paso_headers', 'target_paso_a'])
env.Alias('install_paso', ['build_paso', 'target_install_paso_a'])

env.Alias('build_escript', ['target_install_escript_headers', 'target_escript_so', 'target_escriptcpp_so'])
env.Alias('install_escript', ['build_escript', 'target_install_escript_so', 'target_install_escriptcpp_so', 'target_install_escript_py'])

env.Alias('build_finley', ['target_install_finley_headers', 'target_finley_so', 'target_finleycpp_so'])
env.Alias('install_finley', ['build_finley', 'target_install_finley_so', 'target_install_finleycpp_so', 'target_install_finley_py'])

env.Alias('build_weipa', ['target_install_weipa_headers', 'target_weipa_so', 'target_weipacpp_so'])
env.Alias('install_weipa', ['build_weipa', 'target_install_weipa_so', 'target_install_weipacpp_so', 'target_install_weipa_py'])

env.Alias('build_escriptreader', ['target_install_weipa_headers', 'target_escriptreader_a'])
env.Alias('install_escriptreader', ['build_escriptreader', 'target_install_escriptreader_a'])

# Now gather all the above into some easy targets: build_all and install_all
build_all_list = []
build_all_list += ['build_esysUtils']
build_all_list += ['build_paso']
build_all_list += ['build_escript']
build_all_list += ['build_finley']
build_all_list += ['build_weipa']
build_all_list += ['build_escriptreader']
if env['usempi']:   build_all_list += ['target_pythonMPI_exe']
build_all_list += ['target_escriptconvert']
env.Alias('build_all', build_all_list)

install_all_list = []
install_all_list += ['target_init']
install_all_list += ['install_esysUtils']
install_all_list += ['install_paso']
install_all_list += ['install_escript']
install_all_list += ['install_finley']
install_all_list += ['install_weipa']
install_all_list += ['install_escriptreader']
install_all_list += ['target_install_pyvisi_py']
install_all_list += ['target_install_modellib_py']
install_all_list += ['target_install_pycad_py']
if env['usempi']:   install_all_list += ['target_install_pythonMPI_exe']
install_all_list += ['target_install_escriptconvert']
env.Alias('install_all', install_all_list)

# Default target is install
env.Default('install_all')

################## Targets to build and run the test suite ###################

env.Alias('build_cppunittest', ['target_install_cppunittest_headers', 'target_cppunittest_a'])
env.Alias('install_cppunittest', ['build_cppunittest', 'target_install_cppunittest_a'])
env.Alias('run_tests', ['install_all', 'target_install_cppunittest_a'])
env.Alias('all_tests', ['install_all', 'target_install_cppunittest_a', 'run_tests', 'py_tests'])
env.Alias('build_full',['install_all','build_tests','build_py_tests'])
env.Alias('build_PasoTests','build/$PLATFORM/paso/profiling/PasoTests')

##################### Targets to build the documentation #####################

env.Alias('api_epydoc','install_all')
env.Alias('docs', ['examples_tarfile', 'examples_zipfile', 'api_epydoc', 'api_doxygen', 'guide_pdf', 'guide_html','install_pdf', 'cookbook_pdf'])
env.Alias('release_prep', ['docs', 'install_all'])

if not IS_WINDOWS:
    try:
        utest=open('utest.sh','w')
        utest.write(GroupTest.makeHeader(env['PLATFORM']))
        for tests in TestGroups:
            utest.write(tests.makeString())
        utest.close()
        Chmod('utest.sh', 0755)
        print("Generated utest.sh.")
    except IOError:
        print("Error attempting to write unittests file.")
        Exit(1)

    # Make sure that the escript wrapper is in place
    if not os.path.isfile(os.path.join(env['bininstall'], 'escript')):
        print("Copying escript wrapper.")
        Execute(Copy(os.path.join(env['bininstall'],'escript'), 'bin/escript'))

