##############################################################################
#
# Copyright (c) 2003-2016 by The University of Queensland
# http://www.uq.edu.au
#
# Primary Business: Queensland, Australia
# Licensed under the Open Software License version 3.0
# http://www.opensource.org/licenses/osl-3.0.php
#
# Development until 2012 by Earth Systems Science Computational Center (ESSCC)
# Development 2012-2013 by School of Earth Sciences
# Development from 2014 by Centre for Geoscience Computing (GeoComp)
#
##############################################################################

from __future__ import print_function, division

__copyright__="""Copyright (c) 2003-2016 by The University of Queensland
http://www.uq.edu.au
Primary Business: Queensland, Australia"""
__license__="""Licensed under the Open Software License version 3.0
http://www.opensource.org/licenses/osl-3.0.php"""
__url__="https://launchpad.net/escript-finley"



class GroupTest(object):
    _allfuncs = []

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
        
    def makeDir(self,dirname):
        self.mkdirs.append(dirname)

    #stdloc means that the files are in standard locations so don't use prefix
    def makeHeader(build_platform, prefix, stdloc):
        res="#!/bin/sh\n"
        res=res+"\n#############################################\n"
        res=res+"# This file is autogenerated by scons.\n"
        res=res+"# It will be regenerated each time scons is run\n"
        res=res+"#############################################\n\n"
        res=res+"failed ()\n{\n  echo ""Execution failed for $@""\n  exit 1\n}\n"
        res=res+"if [ $# -lt 2 ]\nthen\n echo \"Usage: $0 build_dir wrapper_options [groupname]\"\necho Runs all or a group of unit tests. Options must be a single string.\nexit 2\nfi\n"
        res=res+'CMDSTR="getopt p:n: -- $2" #Not using -uq -o because that is GNU only\nSTR=`$CMDSTR`\nNUMPROCS=1\n'
        if stdloc:
            res=res+'MPITYPE=`run-escript -c | grep mpi=`\n'
        else:
            res=res+'MPITYPE=`%s/bin/run-escript -c | grep mpi=`\n'%prefix
        res=res+'NUMNODES=1\n#This little complication is required because set --\n'
        res=res+'#does not seem to like -n as the first positional parameter\n'
        res=res+'STATE=0\nfor name in $STR\ndo \n'
        res=res+'case $STATE in\n'
        res=res+'     0) case $name in\n'
        res=res+'          -n) STATE=1;;\n'
        res=res+'          -p) STATE=2;;\n'
        res=res+'          --) break 2;;\n'
        res=res+'        esac;;\n'
        res=res+'     1) if [ $name == "--" ];then break; fi; NUMNODES=$name; STATE=0;;\n'
        res=res+'     2) if [ $name == "--" ];then break; fi; NUMPROCS=$name; STATE=0;;\n'
        res=res+'   esac\n'
        res=res+'done\n'
        res=res+'MPIPROD=$(($NUMPROCS * $NUMNODES))\n'
        if not stdloc:
            res=res+"\nexport LD_LIBRARY_PATH=%s/lib:$LD_LIBRARY_PATH\n"%prefix
        if build_platform=='darwin':
                res=res+"export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DYLD_LIBRARY_PATH\n"
        if stdloc:
            res=res+"\nexport OLD_PYTHON=$PYTHONPATH\nBINRUNNER=\"run-escript -b $2\"\nPYTHONRUNNER=\"run-escript $2\"\nBATCH_ROOT=`pwd`\n"
            res=res+"PYTHONTESTRUNNER=\"run-escript $2 $BATCH_ROOT/tools/testrunner.py\"\n"
        else:
            res=res+"""\nexport OLD_PYTHON={0}:$PYTHONPATH
BINRUNNER=\"{0}/bin/run-escript -b $2\"
PYTHONRUNNER=\"{0}/bin/run-escript $2\"
PYTHONTESTRUNNER=\"{0}/bin/run-escript $2 {0}/tools/testrunner.py\"
BATCH_ROOT=`pwd`\n""".format(prefix)
        res=res+"BUILD_DIR=$1"+"/"+build_platform
        res=res+"\nif [ ! -d $BUILD_DIR ]\nthen\n echo Can not find build directory $BUILD_DIR\n exit 2\nfi\n" 
        #res=res+"if [ $# -lt 2 ]\nthen\n echo Usage: $0 bin_run_cmd python_run_cmd\n exit 2\nfi\n"
        return res
    makeHeader=staticmethod(makeHeader)

    def makeString(self):
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
                    exit_on_failure = ""
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
                exit_on_failure = ""
            res += "".join([tt, cmd, t, failoutputfile, skipoutputfile, exit_on_failure, "\n"])
            res += tt+"echo Completed "+t+"\n"
        res=res+"}\n"
        return res
    
    def makeFooter(self):
        res="if [ $# -gt 2 ]; then\n\teval $3\nelse\n\t"
        res+="\n\t".join(self._allfuncs)
        res+="\nfi\nfind $BUILD_DIR -name '*.failed' | xargs cat; find $BUILD_DIR -name '*.failed' | xargs cat | diff -q - /dev/null >/dev/null\n"
        return res

