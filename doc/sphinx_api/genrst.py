#!/usr/bin/env python

import os
import inspect
import sys

if len(sys.argv)!=4:
  sys.stderr.write('Usage: startdir startpackage outputdirectory\n')
  sys.exit(1)

#startdir='./esys'
#startpackage='esys'
#outdir='doctest'

startdir=sys.argv[1]
startpackage=sys.argv[2]
outdir=sys.argv[3]

def listmods():
  W=os.walk(startdir,topdown=True)

  main=open(os.path.join(outdir,'index.rst'),'w')
  main.write('.. Generated by Joel\'s script\n\n')
  main.write('Documentation for esys.escript\n')
  main.write('==============================\n')
  main.write('\n')
  main.write('Contents:\n\n')
  main.write('.. toctree::\n')
  main.write('   :maxdepth: 4\n')
  main.write('\n')
  
  for z in W:
    print "Beginning ",z[0]
    # Now make the package name
    n=startpackage+'.'.join(z[0][len(startdir):].split(os.path.sep))
    main.write("   "+n+"\n")
    #Now we need to create a page for this
    pack=open(os.path.join(outdir,n+'.rst'),'w')
    pack.write(n+' Package\n')
    pack.write('='*len(n)+'========\n\n')
    pack.write('.. py:module:: '+n+'\n\n')
    #Automodule does not seem to do what we want so we need to drill down
    exec('import '+n+' as PP')
    clist=[]
    flist=[]
    vlist=[]
    for (name, mem) in inspect.getmembers(PP):
      if inspect.ismodule(mem):
	#pack.write('Module '+name+'\n')
	pass
      elif inspect.isclass(mem):
	clist+=[(name, mem)]
      elif inspect.isfunction(mem):
	flist+=[(name, mem)]
      else:
	if type(mem).__module__+'.'+type(mem).__name__=='Boost.Python.function':
	  flist+=[(name, mem)]
	else:
	  vlist+=[(name, mem)]
    pack.write('Classes\n')
    pack.write('-------\n')
    for (name, mem) in clist:
      pack.write('* `'+name+'`\n')
    pack.write('\n')
    for (name, mem) in clist:
      pack.write('.. autoclass:: '+name+'\n')
      pack.write('   :members:\n   :undoc-members:\n\n')
    pack.write('\n')
    
    pack.write('Functions\n')
    pack.write('---------\n')
    for (name, mem) in flist:
      pack.write('.. autofunction:: '+name+'\n')
    pack.write('\n')
    
    pack.write('Others\n')
    pack.write('------\n')
    for (name, mem) in vlist:
      pack.write('* '+name+'\n')
    pack.write('\n')
    
    
    for m in z[2]:	#This will list the files
      if m.split('.')[1]=='pyc' and m!='__init__.pyc':
	print ".."+n+"."+m
    pack.close()
  main.write('\n')
  main.write('Indices and Tables\n')
  main.write('==================\n')
  main.write('\n')
  main.write('* :ref:`genindex`\n')
  main.write('* :ref:`modindex`\n')
  main.write('\n')
  main.close()	
    
    
listmods()    