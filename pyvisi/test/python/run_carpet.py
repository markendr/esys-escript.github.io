from esys.pyvisi import DataCollector, Scene, Carpet
from esys.pyvisi.constant import *
import unittest, os
from stat import ST_SIZE

try:
     PYVISI_WORKDIR=os.environ['PYVISI_WORKDIR']
except KeyError:
     PYVISI_WORKDIR='.'
try:
     PYVISI_TEST_DATA_ROOT=os.environ['PYVISI_TEST_DATA_ROOT']
except KeyError:
     PYVISI_TEST_DATA_ROOT='.'
     
PYVISI_TEST_MESHES_PATH = os.path.join(PYVISI_TEST_DATA_ROOT,"data_meshes")
PYVISI_TEST_CARPET_IMAGES_PATH = os.path.join(PYVISI_TEST_DATA_ROOT,"data_sample_images","carpet")
MIN_IMAGE_SIZE = 100
FILE_3D = "interior_3D.xml"

X_SIZE = 400
Y_SIZE = 400

JPG_RENDERER = Renderer.OFFLINE_JPG

class TestCarpet:
	def tearDown(self):
		self.scene
		self.data_collector
		self.contour

	def render(self, file):
		self.scene.render(image_name = \
				PYVISI_TEST_CARPET_IMAGES_PATH + file)

		self.failUnless(os.stat(PYVISI_TEST_CARPET_IMAGES_PATH + \
				file)[ST_SIZE] > MIN_IMAGE_SIZE)

class TestCarpetScalarWarp(unittest.TestCase, TestCarpet):
	def setUp(self):
		self.scene = \
				Scene(renderer = JPG_RENDERER, num_viewport = 1,
						x_size = X_SIZE, y_size = Y_SIZE)

		self.data_collector = DataCollector(source = Source.XML)
		self.data_collector.setFileName(file_name = \
				os.path.join(PYVISI_TEST_MESHES_PATH, FILE_3D))

		self.carpet = Carpet(scene = self.scene,
				data_collector = self.data_collector,
				viewport = Viewport.SOUTH_WEST, warp_mode = WarpMode.SCALAR,
				lut = Lut.COLOR, cell_to_point = False, outline = True)


	def testScalarWarp(self):
		self.carpet.setScaleFactor(1)
		self.carpet.setPlaneToXY()
		self.render(os.path.join(PYVISI_WORKDIR,"TestCarpetScalarWarp.jpg"))
	
class TestCarpetVectorWarp(unittest.TestCase, TestCarpet):
	def setUp(self):
		self.scene = \
				Scene(renderer = JPG_RENDERER, num_viewport = 1,
						x_size = X_SIZE, y_size = Y_SIZE)

		self.data_collector = DataCollector(source = Source.XML)
		self.data_collector.setFileName(file_name = \
				os.path.join(PYVISI_TEST_MESHES_PATH, FILE_3D))

		self.carpet = Carpet(scene = self.scene,
				data_collector = self.data_collector,
				viewport = Viewport.SOUTH_WEST, warp_mode = WarpMode.VECTOR,
				lut = Lut.COLOR, cell_to_point = False, outline = True)


	def testVectorWarp(self):
		self.carpet.setScaleFactor(1)
		self.carpet.setPlaneToXY()
		self.render(os.path.join(PYVISI_WORKDIR,"TestCarpetVectorWarp.jpg"))
	


##############################################################################


if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCarpetScalarWarp))
	suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCarpetVectorWarp))
	unittest.TextTestRunner(verbosity=2).run(suite)

