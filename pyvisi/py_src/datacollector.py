"""
@author: John NGUI
"""

import vtk
from constant import Source 

class DataCollector:
	"""
	Class that defines a data collector which dealrs with the source 
	of data for the visualisation.
	"""

	def __init__(self, source = Source.XML):
		"""
		Initialise the data collector.

		@type source: L{Source <constant.Source>} constant
		@param source: Source data type
		"""

		if(source == Source.XML): # Source is an XML file.
			self.__vtk_xml_reader = vtk.vtkXMLUnstructuredGridReader()

	def setFileName(self, file_name):
		"""
		Set the source file name to read. 

		@type file_name: String
		@param file_name: Name of the file to read
		"""

		self.__vtk_xml_reader.SetFileName(file_name)
		self.__output = self.__vtk_xml_reader.GetOutput()

		# NOTE: Update must be called after SetFileName to make the reader 
		# up to date. Otherwise, some output values may be incorrect.
		self.__vtk_xml_reader.Update() 

	def _setActiveScalar(self, scalar):
		"""
		Specify the scalar field to load from the source file.

		@type scalar: String
		@param scalar: Scalar field to load from the file. 
		"""

		self._getOutput().GetPointData().SetActiveScalars(scalar)

	def _setActiveVector(self, vector):
		"""
		Specify the vector field to load from the source file. 

		@type vector: String
		@param vector: Vector field to load from the file. 
		"""

		self._getOutput().GetPointData().SetActiveVectors(vector)

	def _setActiveTensor(self, tensor):
		"""
		Specify the tensor field to load from the source file.

		@type tensor: String
		@param tensor: Tensor field to load from the file. 
		"""

		self._getOutput().GetPointData().SetActiveTensors(tensor)

	def _getScalarRange(self):
		"""
		Return the scalar range.

		@rtype: Two column tuple
		@return: Scalar range
		"""

		return self._getOutput().GetPointData().GetScalars().GetRange(-1)

	def _getVectorRange(self):
		"""
		Return the vector range.
	
		@rtype: Two column tuple
		@return: Vector range
		"""

		vector_range = self._getOutput().GetPointData().GetVectors().GetRange(-1)

		# NOTE: Generally GetRange(-1) returns the correct vector range. 
		# However, there are certain data sets where GetRange(-1) seems 
		# to return incorrect mimimum vector although the maximum vector is 
		# correct. As a result, the mimimum vector has been hard coded to 0.0
		# to accommodate those incorrect cases.
		return (0.0, vector_range[1])

	def _getTensorRange(self):
		"""
		Return the tensor range.

		@rtype: Two column table
		@return: Tensor range
		"""

		return self._getOutput().GetPointData().GetTensors().GetRange()

	def _getOutput(self):
		"""
		Return the output of the data collector.

		@rtype: vtkUnstructuredGrid
		@return: Unstructured grid
		"""

		return self.__output

	
###############################################################################


from constant import ImageFormat

class ImageReader:
	"""
	Class that defines an image reader.
	"""

	def __init__(self, format):
		"""	
		Initialise the image reader.

		@type format: String
		@param format: Format of the image 
		"""

		self.__format = format
		self.__vtk_image_reader = self.getImageReader()

	def getImageReader(self):
		"""
		Return the appropriate image reader based on the supplied image 
		format.

		@rtype: vtkImageReader2 (i.e. vtkJPEGReader, etc)
		@return: Image reader 
		"""

		if(self.__format == ImageFormat.JPG):
			return vtk.vtkJPEGReader()	
		elif(self.__format == ImageFormat.BMP):
			return vtk.vtkBMPReader()
		elif(self.__format == ImageFormat.PNM):
			return vtk.vtkPNMReader()
		elif(self.__format == ImageFormat.PNG):
			return vtk.vtkPNGReader()
		elif(self.__format == ImageFormat.TIF):
			return vtk.vtkTIFFReader()

	def setFileName(self, file_name):
		"""
		Set the image file name.

		@type file_name: String
		@param file_name: Image file name to be read 
		"""

		self.__vtk_image_reader.SetFileName(file_name)

	def _getOutput(self):
		"""
		Return the output of the image reader.

		@rtype: vtkImageData
		@return Image data
		"""

		return self.__vtk_image_reader.GetOutput()

