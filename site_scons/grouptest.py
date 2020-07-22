##############################################################################
#
# Copyright (c) 2003-2018 by The University of Queensland
# http://www.uq.edu.au
#
# Primary Business: Queensland, Australia
# Licensed under the Apache License, version 2.0
# http://www.apache.org/licenses/LICENSE-2.0
#
# Development until 2012 by Earth Systems Science Computational Center (ESSCC)
# Development 2012-2013 by School of Earth Sciences
# Development from 2014 by Centre for Geoscience Computing (GeoComp)
#
##############################################################################

from __future__ import print_function, division
import os, re

__copyright__="""Copyright (c) 2003-2018 by The University of Queensland
http://www.uq.edu.au
Primary Business: Queensland, Australia"""
__license__="""Licensed under the Apache License, version 2.0
http://www.apache.org/licenses/LICENSE-2.0"""
__url__="https://launchpad.net/escript-finley"


IS_WINDOWS = (os.name == 'nt')

class GroupTest(object):
    _allfuncs = []
    repEnv = None

    def __init__(self, name, exec_cmd, evars, python_dir, working_dir, test_list, single_process_tests=[]):
        self.name=name
        self.python_dir=python_dir
        self.working_dir=working_dir
        self.test_list=test_list
        self.exec_cmd=exec_cmd
        self.evars=evars
        self.mkdirs=[]
        self.single_process_tests=single_process_tests
        self._allfuncs.append(name)
        if IS_WINDOWS:
            self.exec_cmd = self.setWinEnvs(self.exec_cmd)
            self.python_dir = self.setWinEnvs(self.python_dir)
            self.working_dir = self.setWinEnvs(self.working_dir)
            self.evars = [(e[0], self.setWinEnvs(e[1])) for e in self.evars]
            rep = re.compile(r'/')
            self.test_list = [rep.sub('\\'+os.sep, t) for t in self.test_list]
            rep = re.compile(r':')
            self.python_dir = rep.sub(os.pathsep, self.python_dir)
        
    def makeDir(self,dirname):
        if IS_WINDOWS:
            dirname = self.setWinEnvs(dirname)
        self.mkdirs.append(dirname)

    def setWinEnvs(self,path):
        if self.repEnv is None:
            self.repEnv = re.compile(r'[$]([a-zA-Z_][a-zA-Z0-9_]*)')
        return self.repEnv.sub(r'%\1%', path)

    #stdloc means that the files are in standard locations so don't use prefix
    def makeHeader(build_platform, prefix, stdloc):
        if IS_WINDOWS:
            return GroupTest._makeHeaderPy(build_platform, prefix, stdloc)
        res="""#!/bin/sh
#############################################
# This file is autogenerated by scons.
# It will be regenerated each time scons is run
#############################################

failed () {
    echo "Execution failed for $@"
    exit 1
}

if [ $# -lt 2 ]; then
    echo "Usage: $0 build_dir wrapper_options [groupname]"
    echo Runs all or a group of unit tests. Options must be a single string.
    exit 2
fi

case "$1" in
   /*) ;;
   *) echo "build_dir needs to be an absolute path"; exit 4;;
esac

NUMPROCS=1
NUMNODES=1
while getopts ':n:p:' option $2
do
    case "$option" in
        "n")  NUMNODES=$OPTARG ;;
        "p")  NUMPROCS=$OPTARG ;;
    esac
done
MPIPROD=$(($NUMPROCS * $NUMNODES))
"""
        res+="BUILD_DIR=$1"+"/"+build_platform
        res+="\nif [ ! -d $BUILD_DIR ]\nthen\n    echo Can not find build directory $BUILD_DIR\n     exit 2\nfi\n" 
        if stdloc:
            res+="""MPITYPE=`run-escript -c | grep mpi=`
export OLD_PYTHON=$PYTHONPATH
BATCH_ROOT=`pwd`
BINRUNNER="run-escript -b $2"
PYTHONRUNNER="run-escript $2"
PYTHONTESTRUNNER="run-escript $2 $BATCH_ROOT/tools/testrunner.py"
"""
        else:
            res+="""MPITYPE=`{0}/bin/run-escript -c | grep mpi=`
BATCH_ROOT=`pwd`            
export LD_LIBRARY_PATH={0}/lib:$LD_LIBRARY_PATH
export OLD_PYTHON={0}:$PYTHONPATH
BINRUNNER="{0}/bin/run-escript -b $2"
PYTHONRUNNER="{0}/bin/run-escript $2"
PYTHONTESTRUNNER="{0}/bin/run-escript $2 {0}/tools/testrunner.py"
""".format(prefix)
        if build_platform=='darwin':
            res+="export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DYLD_LIBRARY_PATH\n"
        return res
    makeHeader=staticmethod(makeHeader)

    def makeString(self):
        if IS_WINDOWS:
            return self._makeStringPy()
        res="%s () {\n"%self.name
        tt="\t"
        build_dir = self.working_dir.replace("$BATCH_ROOT", "$BUILD_DIR")
        for d in self.mkdirs:
            res=res+tt+"if [ ! -d "+str(d)+" ]\n"+tt+"then\n"+tt+"\tmkdir -p "+str(d)+"\n"+tt+"fi\n"
        for v in self.evars:
            res=res+tt+"export "+str(v[0])+"="+str(v[1])+"\n"
        res=res+tt+"if [ ! -d "+str(self.working_dir)+" ]\n"+tt+"then\n"+tt+"\tmkdir -p "+str(self.working_dir)+"\n"+tt+"fi\n"
        if len(self.python_dir)>0:
            res=res+tt+"export PYTHONPATH="+self.python_dir+":$OLD_PYTHON"+"\n"+tt+"cd "+self.working_dir+"\n"
        else:
            res=res+tt+"export PYTHONPATH=$OLD_PYTHON"+"\n"+tt+"cd "+self.working_dir+"\n"
        if len(self.single_process_tests) > 0:
            res+=tt+"if [ $MPIPROD -le 1 ]; then\n"
            #res+=tt+'if [ "$MPITYPE" == "mpi=none" ]; then\n'
            tt+="\t"
            for t in self.single_process_tests:
                res=res+tt+"echo Starting "+t+"\n"+tt+"date\n"
                skipoutputfile = ""
                failoutputfile = ""
                cmd = self.exec_cmd
                exit_on_failure = " || failed %s"%t
                if "examples" not in build_dir and "PYTHONRUNNER" in self.exec_cmd \
                        and "/tools/" not in build_dir:
                    skipoutputfile = " -skipfile={0}/{1}".format(build_dir, t.replace(".py", ".skipped"))
                    failoutputfile = " -failfile={0}/{1}".format(build_dir, t.replace(".py", ".failed"))
                    cmd = cmd.replace("PYTHONRUNNER", "PYTHONTESTRUNNER")
                res += "".join([tt, cmd, t, failoutputfile, skipoutputfile, exit_on_failure, "\n"])
                res += tt+"echo Completed "+t+"\n"
            tt="\t"
            res+=tt+"fi\n"
        for t in self.test_list:
            res=res+tt+"echo Starting "+t+"\n"+tt+"date\n"
            skipoutputfile = ""
            failoutputfile = ""
            cmd = self.exec_cmd
            exit_on_failure = " || failed %s"%t
            if "examples" not in build_dir and "PYTHONRUNNER" in self.exec_cmd \
                    and "/tools/" not in build_dir:
                skipoutputfile = " -skipfile={0}/{1}".format(build_dir, t.replace(".py", ".skipped"))
                failoutputfile = " -failfile={0}/{1}".format(build_dir, t.replace(".py", ".failed"))
                cmd = cmd.replace("PYTHONRUNNER", "PYTHONTESTRUNNER")
            res += "".join([tt, cmd, t, failoutputfile, skipoutputfile, exit_on_failure, "\n"])
            res += tt+"echo Completed "+t+"\n"
        res=res+"}\n"
        return res
    
    def makeFooter(self):
        if IS_WINDOWS:
            return self._makeFooterPy()
        res="if [ $# -gt 2 ]; then\n\teval $3\nelse\n\t"
        res+="\n\t".join(self._allfuncs)
        res+="\nfi\nfind $BUILD_DIR -name '*.failed' | xargs cat; find $BUILD_DIR -name '*.failed' | xargs cat | diff -q - /dev/null >/dev/null\n"
        return res

    @staticmethod
    def _makeHeaderPy(build_platform, prefix, stdloc):
        res='''#!/usr/bin/env python
#############################################
# This file is autogenerated by scons.
# It will be regenerated each time scons is run
#############################################

import datetime, getopt, os, re, subprocess, sys

def failed(msg):
    print('Execution failed for {}'.format(msg))
    exit(1)

def now():
    return datetime.datetime.now().strftime('%%Y-%%m-%%d %%H:%%M:%%S')

opts, args = getopt.getopt(sys.argv[1:], ':np:')

if len(args) < 2:
    print('Usage: {} build_dir wrapper_options [groupname]'.format(sys.argv[0]))
    print('Runs all or a group of unit tests. Options must be a single string.')
    exit(2)

if os.name == 'nt':
    vols = subprocess.Popen('mountvol', stdout=subprocess.PIPE).stdout.read().decode(sys.stdout.encoding)
    path_prefix = re.findall(r'[A-Z]+:\\\\', vols, re.MULTILINE)
else:
    path_prefix = [os.sep]

path_prefix_match = False
for p in path_prefix:
    if sys.argv[1].startswith(p):
        path_prefix_match = True
if not path_prefix_match:
    print('build_dir needs to be an absolute path')
    exit(4)

build_platform = '%(bldplat)s'
prefix = r'%(prefix)s'
prefix_bin = r'%(prefix_bin)s'
prefix_lib = r'%(prefix_lib)s'

NUMPROCS = 1
NUMNODES = 1
for opt, arg in opts:
    if opt == '-n':
        NUMNODES = int(arg)
    elif opt == '-p':
        NUMPROCS = int(arg)
    else:
        print("unknown option")
        exit(5)
MPIPROD = NUMPROCS * NUMNODES
build_dir = os.path.join(args[0], build_platform)
if not os.path.isdir(build_dir):
    print("Can not find build directory "+build_dir)
    exit(2)

os.environ['BUILD_DIR'] = build_dir
os.environ['BATCH_ROOT'] = os.getcwd()
run_args = '' if len(args) < 2 else args[1]
os.environ['BINRUNNER'] = os.path.join(prefix_bin, 'run-escript -b '+run_args)
os.environ['PYTHONRUNNER'] = os.path.join(prefix_bin, 'run-escript '+run_args)

if len(prefix) > 0:
    os.environ['PYTHONTESTRUNNER'] = os.path.join(prefix_bin, 'run-escript '+run_args)+' '+os.path.join(
        prefix, 'tools', 'testrunner.py')
    os.environ['LD_LIBRARY_PATH'] = prefix_lib+os.pathsep+os.environ.get('LD_LIBRARY_PATH', '')
    os.environ['OLD_PYTHON'] = prefix+os.pathsep+os.environ.get('PYTHONPATH', '')
else:
    os.environ['PYTHONTESTRUNNER'] = 'run-escript '+run_args+' '+os.path.join(os.getcwd(), 'tools', 'testrunner.py')
    os.environ['OLD_PYTHON'] = os.environ.get('PYTHONPATH', '')

'''
        if stdloc:
            prefix_bin = ''
            prefix_lib = ''
        else:
            prefix_bin = os.path.join(prefix, 'bin')
            prefix_lib = os.path.join(prefix, 'lib')
        return res % { 'bldplat': build_platform, 'prefix': prefix, 'prefix_bin': prefix_bin,
            'prefix_lib': prefix_lib }

    def _makeStringPy(self):
        res = 'def %s():\n'%self.name
        tt = '    '
        build_dir = self.working_dir.replace('BATCH_ROOT', 'BUILD_DIR')
        for d in self.mkdirs:
            res += tt+"if not os.path.isdir(os.path.expandvars(r'"+d+"')):\n"+tt+tt+ \
                "os.makedirs(os.path.expandvars(r'"+d+"'))\n"
        for v in self.evars:
            res += tt+"os.environ['"+str(v[0])+"'] = os.path.expandvars(r'"+str(v[1])+"')\n"
        res += tt+"if not os.path.isdir(os.path.expandvars(r'"+self.working_dir+"')):\n"+tt+tt+ \
            "os.makedirs(os.path.expandvars(r'"+self.working_dir+"'))\n"
        if len(self.python_dir) > 0:
            res += tt+"os.environ['PYTHONPATH'] = os.path.expandvars(r'"+self.python_dir+"')+os.pathsep+os.environ.get('OLD_PYTHON', '')\n"
        else:
            res += tt+"os.environ['PYTHONPATH'] = os.environ.get('OLD_PYTHON', '')\n"
        res += tt+"os.chdir(os.path.expandvars(r'"+self.working_dir+"'))\n"
        if len(self.single_process_tests) > 0:
            res += tt+'if MPIPROD <= 1:\n'
            tt += '    '
            for t in self.single_process_tests:
                res += tt+"print(r'Starting "+t+"'+'\\n"+tt+"'+now())\n"
                skipoutputfile = ''
                failoutputfile = ''
                cmd = self.exec_cmd
                if 'examples' not in build_dir and 'PYTHONRUNNER' in self.exec_cmd \
                        and '/tools/' not in build_dir:
                    skipoutputfile = ' -skipfile={0}{1}'.format(build_dir, t.replace('.py', '.skipped'))
                    failoutputfile = ' -failfile={0}{1}'.format(build_dir, t.replace('.py', '.failed'))
                    cmd = cmd.replace('PYTHONRUNNER', 'PYTHONTESTRUNNER')
                res += tt+"if subprocess.call(r'"+cmd+t+failoutputfile+skipoutputfile+"', shell=True) != 0:\n"
                res += tt+tt+"failed(r'"+t+"')\n"
                res += tt+"print(r'Completed "+t+"')\n"
            tt = '    '
        for t in self.test_list:
            res += tt+"print(r'Starting "+t+"'+'\\n"+tt+"'+now())\n"
            skipoutputfile = ''
            failoutputfile = ''
            cmd = self.exec_cmd
            if 'examples' not in build_dir and 'PYTHONRUNNER' in self.exec_cmd \
                    and '/tools/' not in build_dir:
                skipoutputfile = ' -skipfile={0}{1}'.format(build_dir, t.replace('.py', '.skipped'))
                failoutputfile = ' -failfile={0}{1}'.format(build_dir, t.replace('.py', '.failed'))
                cmd = cmd.replace('PYTHONRUNNER', 'PYTHONTESTRUNNER')
            res += tt+"if subprocess.call(r'"+cmd+t+failoutputfile+skipoutputfile+"', shell=True) != 0:\n"
            res += tt+tt+"failed(r'"+t+"')\n"
            res += tt+"print(r'Completed "+t+"')\n"
        res += '\n'
        return res

    def _makeFooterPy(self):
        res = "if len(args) > 2:\n    globals()[args[2]]()\nelse:\n"
        for f in self._allfuncs:
            res += '    '+f+'()\n'
        #TODO:
        #res+="\nfind $BUILD_DIR -name '*.failed' | xargs cat; find $BUILD_DIR -name '*.failed' | xargs cat | diff -q - /dev/null >/dev/null\n"
        return res
        #try this
        #for root, dirs, files in os.walk('.'):
        #    for f in files:
        #        if f.endswith('.py'):
        #            print(os.path.join(root, f))
