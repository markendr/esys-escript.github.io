##############################################################################
#
# Copyright (c) 2003-2013 by University of Queensland
# http://www.uq.edu.au
#
# Primary Business: Queensland, Australia
# Licensed under the Open Software License version 3.0
# http://www.opensource.org/licenses/osl-3.0.php
#
# Development until 2012 by Earth Systems Science Computational Center (ESSCC)
# Development since 2012 by School of Earth Sciences
#
##############################################################################

"""
This example shows how to create a netCDF input files for inversion with
inversion in esys.downunder. 
"""

from datetime import datetime
import numpy as np
from scipy.io import netcdf_file

# output filename
FILENAME='output.nc'

# a concise title and summary of the dataset
TITLE="custom_data"
SUMMARY="Bouguer gravity anomaly data"

# Origin longitude (degrees east) and latitude (degrees north)
ORIGIN_X=130.2
ORIGIN_Y=-29.1

# spacing in longitude,latitude direction (degrees)
DELTA_X=0.05
DELTA_Y=0.05

# Number of data points in longitude,latitude direction
NX=20
NY=10

# Dummy value (for unset areas)
MISSING=-9999

# Data error
SIGMA = 3.



# The actual data array, must have shape (NY, NX)
# these are just some random numbers.
DATA=10*np.random.normal(size=(NY, NX), scale=SIGMA)
ERROR=np.ones((NY, NX)) * SIGMA

##############################################################################
###################### Keep everything below this line #######################
##############################################################################
# file log
history=datetime.now().strftime("%d-%m-%Y")+" created using python script"
# license
license="Free to use"

longitude=np.linspace(ORIGIN_X, ORIGIN_X+NX*DELTA_X, NX, endpoint=False)
latitude=np.linspace(ORIGIN_Y, ORIGIN_Y-NY*DELTA_Y, NY, endpoint=False)

o=netcdf_file(FILENAME,'w')
o.history=history
o.license=license
o.title=TITLE
o.summary=SUMMARY
o.createDimension("latitude", NY)
o.createDimension("longitude", NX)

v=o.createVariable("latitude", latitude.dtype, ["latitude"])
v.data[:]=latitude

v=o.createVariable("longitude", longitude.dtype, ["longitude"])
v.data[:]=longitude

v=o.createVariable("data", DATA.dtype, ["latitude","longitude"])
v.missing_value=MISSING
v.data[:]=DATA

# can be omitted.
v=o.createVariable("error", DATA.dtype, ["latitude","longitude"])
v.missing_value=MISSING
v.data[:]=ERROR

o.close()
