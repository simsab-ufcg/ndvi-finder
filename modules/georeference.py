from osgeo import gdal, osr

def set_georeference(src_path, base_path, coord_upper_left):

	base_ds = gdal.Open(base_path)
	base_coord = base_ds.GetGeoTransform()
	base_proj = base_ds.GetProjection()

	src_ds = gdal.Open(src_path, gdal.GA_Update)

	result_coord = (coord_upper_left[0], 29.996139493, base_coord[2], coord_upper_left[1], base_coord[4], -29.996139493)

	#for i in xrange(6):
	#	if i == 0 or i == 3:
	#		result_coord.append(coord_upper_left[i/3])
	#	else:
	#		result_coord.append(base_coord[i])

	src_ds.SetGeoTransform(result_coord)
	src_ds.SetProjection(base_proj)

	src_ds = None
	base_ds = None