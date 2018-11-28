import os
import georeference
import coordinate
import errorHandler

def ndvi(path_to_band_red_tiff, path_to_band_nir_tiff, path_to_bqa_tiff, path_to_mtl_tiff, output_name_ndvi):
	'''
	Executing cplusplus code to calculate ndvi for a given scene, returning path to resulting tiff and the exit code.
	'''

	separator = " "
	command = separator.join( ('./modules/ndvi/run', path_to_band_red_tiff, path_to_band_nir_tiff, path_to_bqa_tiff, path_to_mtl_tiff) )
	command = separator.join( (command, output_name_ndvi + '.tif') )
	exit_code = os.system(command)
	path_ndvi_output = output_name_ndvi + '.tif'
	return path_ndvi_output, exit_code
	
def converter(path_to_band_red_tiff, path_to_band_nir_tiff, path_to_bqa_tiff, path_to_mtl_tiff, output_name_ndvi):
	'''
	Converts Tiled Tiffs to normal Tiffs, calculates ndvi for the given scene and returns resulting tiff path.
	'''

	separator = " "

	command = separator.join( ('gdal_translate -co', '\"TILED=NO\"', path_to_band_red_tiff,  path_to_band_red_tiff[:-4] + 'C.tif') )
	path_to_band_red_tiff =  path_to_band_red_tiff[:-4] + 'C.tif'
	os.system(command)

	command = separator.join( ('gdal_translate -co', '\"TILED=NO\"', path_to_band_nir_tiff,  path_to_band_nir_tiff[:-4] + 'C.tif') )
	path_to_band_nir_tiff = path_to_band_nir_tiff[:-4] + 'C.tif'
	os.system(command)

	command = separator.join( ('gdal_translate -co', '\"TILED=NO\"', path_to_bqa_tiff,  path_to_bqa_tiff[:-4] + 'C.tif') )	
	path_to_bqa_tiff =  path_to_bqa_tiff[:-4] + 'C.tif'
	os.system(command)

	path_ndvi_output, exit_code = ndvi(path_to_band_red_tiff, path_to_band_nir_tiff, path_to_bqa_tiff, path_to_mtl_tiff, output_name_ndvi)

	command_deleted_converted_tiffs = separator.join( ('rm -rf', path_to_band_red_tiff, path_to_band_nir_tiff, path_to_bqa_tiff) )
	os.system(command_deleted_converted_tiffs)

	return path_ndvi_output, exit_code


def calculate_ndvi(raster_path, output_path = "ndvi_scenes/", normalize_output_path = "ndvi_scenes_normalize/"):
	'''
	Takes paths of all needed bands + MTL for one or more scenes, calculates
	the NDVI for each of them and returns paths to resulting tiffs.
	'''

	quant_scenes = len(raster_path) / 4

	ndvis_path = []

	os.system('mkdir -p ' + output_path)
	os.system('rm -rf ' + normalize_output_path)
	os.system('mkdir -p ' + normalize_output_path)

	for scene in xrange(quant_scenes):
		path_ndvi_scene, exit_code = ndvi(raster_path[scene*4], raster_path[scene*4+1], raster_path[scene*4+2], raster_path[scene*4+3], output_path + 'ndvi_scene_' + str(scene))

		if (exit_code >> 8) == (2 << 3):
			os.system('rm -rf ' + path_ndvi_scene)
			path_ndvi_scene, exit_code = converter(raster_path[scene*4], raster_path[scene*4+1], raster_path[scene*4+2], raster_path[scene*4+3], output_path + 'ndvi_scene_' + str(scene))

		if (exit_code >> 8) == 0:
			UL = coordinate.get_coordinate(raster_path[scene*4])
			georeference.set_georeference(path_ndvi_scene, raster_path[scene*4], UL)

			path_ndvi_normalize_scene = normalize_output_path + 'normalize_ndvi_scene_' + str(scene) + '.tif'
			os.system('gdalwarp -overwrite -t_srs EPSG:31984 ' + path_ndvi_scene + ' ' + path_ndvi_normalize_scene + ' -dstnodata -nan')
			ndvis_path.append(path_ndvi_normalize_scene)
		else:
			errorHandler.throwError( 'Calculate NDVI', exit_code )
	
	for raster in raster_path:
		os.system('rm -rf ' + raster)

	os.system('rm -rf ' + output_path)

	real_ndvis_path = []

	for ndvi_path in ndvis_path:
		bread = ndvi_path.split('/')
		bread[-1] = 'n' + bread[-1]
		real_ndvi_path = '/'.join(bread)
		cmd = 'gdal_merge.py ' + ndvi_path + ' -o ' + real_ndvi_path + ' -ps 30 30'
		os.system(cmd)
		os.system('rm -rf ' + ndvi_path)
		real_ndvis_path.append(real_ndvi_path)

	return real_ndvis_path

