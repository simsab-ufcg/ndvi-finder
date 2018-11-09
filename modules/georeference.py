from osgeo import gdal, osr
import errorHandler

def set_georeference(src_path, base_path, coord_upper_left):
	'''
	Sets georeference and projection of a tiff based on a source tiff.
	'''

	base_ds = gdal.Open(base_path)
	if base_ds == None:
		errorHandler.throwError("Set georeference", 256)

	base_coord = base_ds.GetGeoTransform()
	if base_coord == None:
		errorHandler.throwError("Set georeference", (6 << 8))

	base_proj = base_ds.GetProjection()
	if base_proj == None:
		errorHandler.throwError("Set georeference", (6 << 8))

	src_ds = gdal.Open(src_path, gdal.GA_Update)
	if src_ds == None:
		errorHandler.throwError("Set georeference", 256)

	result_coord = (coord_upper_left[0], 29.996139493, base_coord[2], coord_upper_left[1], base_coord[4], -29.996139493)

	src_ds.SetGeoTransform(result_coord)
	src_ds.SetProjection(base_proj)

	src_ds = None
	base_ds = None