from osgeo import gdal, osr
import os

def get_coordinate(source_tif_path):

	source_tiff = gdal.Open(source_tif_path)
	coord_tiff = source_tiff.GetGeoTransform()
	width_tiff = source_tiff.RasterXSize
	height_tiff = source_tiff.RasterYSize

	# Constants
	INDEX_X = 0
	INDEX_Y = 1

	UL = (coord_tiff[0], coord_tiff[3])

	# Getting upper left point
	#UL = (coord_tiff[INDEX_X], coord_tiff[INDEX_Y])

	source_tif = None

	return UL