from osgeo import gdal, osr

def get_coordinate(source_tif_filename, output_mtl_filename):

	source_tiff = gdal.Open(source_tif_filename)
	coord_tiff = source_tiff.GetGeoTransform()
	width_tiff = source_tiff.RasterXSize
	height_tiff = source_tiff.RasterYSize

	# Constants
	INDEX_X = 0
	INDEX_Y = 1

	coord_tiff = (coord_tiff[0], coord_tiff[3])

	# Points Upper Left and Lower Right
	UL = (coord_tiff[INDEX_X], coord_tiff[INDEX_Y])
	LR = (coord_tiff[INDEX_X] + (width_tiff * 30.0), coord_tiff[INDEX_Y] - (height_tiff * 30.0))

	file_mtl.close()
	source_tif = None

	return (UL, LR)