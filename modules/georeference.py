from osgeo import gdal, osr

def set_georeference(src_filename, base_filename, coord_upper_left):

	base_ds = gdal.Open(base_filename)
	base_coord = base_ds.GetGeoTransform()
	base_proj = base_ds.GetProjection()

	src_ds = gdal.Open(src_filename, gdal.GA_Update)

	base_coord[0] = coord_upper_left[0]
	base_coord[3] = coord_upper_left[1]

	src_ds.SetGeoTransform(base_coord)
	src_ds.SetProjection(base_proj)

	src_ds = None
	base_ds = None