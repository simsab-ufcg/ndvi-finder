import os
import georeference
import coordinate

def ndvi(path_to_b4_tiff, path_to_b5_tiff, path_to_bqa_tiff, path_to_mtl_tiff, output_name_ndvi):

	separator = " "
	command = separator.join( ('./modules/ndvi/run', path_to_b4_tiff, path_to_b5_tiff, path_to_bqa_tiff, path_to_mtl_tiff) )
	command = separator.join( (command, output_name_ndvi + '.tif') )

	os.system(command)

	path_ndvi_output = output_name_ndvi + '.tif'
	return path_ndvi_output
	

def calculate_ndvi(raster_path, output_path = "ndvi_scenes/", normalize_output_path = "ndvi_scenes_normalize/"):
	quant_scenes = len(raster_path) / 4

	ndvis_path = []

	os.system('rm -rf ' + output_path)
	os.system('rm -rf ' + normalize_output_path)
	os.system('mkdir -p ' + output_path)
	os.system('mkdir -p ' + normalize_output_path)

	for scene in xrange(quant_scenes):
		path_ndvi_scene = ndvi(raster_path[scene*4], raster_path[scene*4+1], raster_path[scene*4+2], raster_path[scene*4+3], output_path + 'ndvi_scene_' + str(scene))

		UL = coordinate.get_coordinate(raster_path[scene*4])
		georeference.set_georeference(path_ndvi_scene, raster_path[scene*4], UL)

		path_ndvi_normalize_scene = normalize_output_path + 'normalize_ndvi_scene_' + str(scene) + '.tif'
		os.system('gdalwarp -overwrite -t_srs EPSG:32625 ' + path_ndvi_scene + ' ' + path_ndvi_normalize_scene + ' -dstnodata -nan')
		ndvis_path.append(path_ndvi_normalize_scene)

	os.system('rm -rf ' + output_path)

	return ndvis_path