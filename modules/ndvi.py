import os
import georeference
import coordinate
import errorHandler

def ndvi(path_to_band_red_tiff, path_to_band_nir_tiff, path_to_bqa_tiff, path_to_mtl_tiff, output_name_ndvi):

	separator = " "
	command = separator.join( ('./modules/ndvi/run', path_to_band_red_tiff, path_to_band_nir_tiff, path_to_bqa_tiff, path_to_mtl_tiff) )
	command = separator.join( (command, output_name_ndvi + '.tif') )
	exit_code = os.system(command)
	path_ndvi_output = output_name_ndvi + '.tif'
	return path_ndvi_output, exit_code
	
def converter(path_to_band_red_tiff, path_to_band_nir_tiff, path_to_bqa_tiff, path_to_mtl_tiff, output_name_ndvi):
	'''
	Converts Tiled Tiffs to normal Tiffs, returning its paths 
	'''

	separator = " "

	command = separator.join( ('gdal_translate -co', '\"TILED=NO\"', path_to_band_red_tiff,  path_to_band_red_tiff[:-4] + 'C.tif') )
	command = separator.join((command, '2> /tmp/libtiff.out'))

	path_to_band_red_tiff =  path_to_band_red_tiff[:-4] + 'C.tif'
	os.system(command)

	command = separator.join( ('gdal_translate -co', '\"TILED=NO\"', path_to_band_nir_tiff,  path_to_band_nir_tiff[:-4] + 'C.tif') )
	command = separator.join((command, '2> /tmp/libtiff.out'))

	path_to_band_nir_tiff = path_to_band_nir_tiff[:-4] + 'C.tif'
	os.system(command)

	command = separator.join( ('gdal_translate -co', '\"TILED=NO\"', path_to_bqa_tiff,  path_to_bqa_tiff[:-4] + 'C.tif') )
	command = separator.join((command, '2> /tmp/libtiff.out'))
	
	path_to_bqa_tiff =  path_to_bqa_tiff[:-4] + 'C.tif'
	os.system(command)

	return ndvi(path_to_band_red_tiff, path_to_band_nir_tiff, path_to_bqa_tiff, path_to_mtl_tiff, output_name_ndvi)


def calculate_ndvi(raster_path, output_path = "ndvi_scenes/", normalize_output_path = "ndvi_scenes_normalize/"):
	'''
	Takes paths of all needed bands + MTL for one or more scenes, calculates
	the NDVI for each of them and returns paths to resulting tiffs
	'''

	quant_scenes = len(raster_path) / 4

	ndvis_path = []

	os.system('rm -rf ' + output_path)
	os.system('rm -rf ' + normalize_output_path)
	os.system('mkdir -p ' + output_path)
	os.system('mkdir -p ' + normalize_output_path)

	for scene in xrange(quant_scenes):
		path_ndvi_scene, exit_code = ndvi(raster_path[scene*4], raster_path[scene*4+1], raster_path[scene*4+2], raster_path[scene*4+3], output_path + 'ndvi_scene_' + str(scene))

		if (exit_code >> 8) == 2:
			os.system('rm -rf ' + path_ndvi_scene)
			path_ndvi_scene, exit_code = converter(raster_path[scene*4], raster_path[scene*4+1], raster_path[scene*4+2], raster_path[scene*4+3], output_path + 'ndvi_scene_' + str(scene))

		if (exit_code >> 8) == 0:
			UL = coordinate.get_coordinate(raster_path[scene*4])
			georeference.set_georeference(path_ndvi_scene, raster_path[scene*4], UL)

			path_ndvi_normalize_scene = normalize_output_path + 'normalize_ndvi_scene_' + str(scene) + '.tif'
			os.system('gdalwarp -overwrite -t_srs EPSG:32625 ' + path_ndvi_scene + ' ' + path_ndvi_normalize_scene + ' -dstnodata -nan')
			ndvis_path.append(path_ndvi_normalize_scene)
		else:
			errorHandler.throwError( 'Calculate NDVI', exit_code )
	
	os.system('rm -rf ' + output_path)

	return ndvis_path

