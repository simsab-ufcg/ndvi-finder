from osgeo import gdal, osr
import errorHandler
import os

def get_coordinate(source_tif_path):

	source_tiff = gdal.Open(source_tif_path)
	if source_tiff == None:
		errorHandler.throwError( "Get Coordinate" , 256)

	coord_tiff = source_tiff.GetGeoTransform()
	if coord_tiff == None:
		errorHandler.throwError( "Get Coordinate" , (6 << 8))

	width_tiff = source_tiff.RasterXSize
	height_tiff = source_tiff.RasterYSize

	# Constants
	INDEX_X = 0
	INDEX_Y = 1

	UL = (coord_tiff[0], coord_tiff[3])
	source_tif = None

	return UL