import os
import coordinate
import georeference

def mergePair(path_list, output_name):
	'''
	Takes paths of two distinct ndvi_tiff files, 
	merge those files and returns the path of merged tiff
	'''

	X_INDEX = 0
	Y_INDEX = 1

	tiff1 = path_list[0]
	tiff2 = path_list[1]

	tiff1_coord = coordinate.get_coordinate(tiff1)
	tiff2_coord = coordinate.get_coordinate(tiff2)

	separator = " "
	command = separator.join( ("./run", tiff1, str(tiff1_coord[X_INDEX]), str(tiff1_coord[Y_INDEX])) )
	command = separator.join( (command, tiff2, str(tiff2_coord[X_INDEX]), str(tiff2_coord[Y_INDEX])) )
	command = separator.join( (command, output_name + '.tif') )

	os.system(command)
	output_path = output_name + '.tif'

	maxY = max(tiff1_coord[Y_INDEX], tiff2_coord[Y_INDEX])
	minX = min(tiff1_coord[X_INDEX], tiff2_coord[X_INDEX])

	output_coord = (minX, maxY)

	georeference.set_georeference(output_path, tiff1, output_coord)
	return output_path

def merge(path_list, output_name="output"):
	'''
	Takes paths of N distinct ndvi_tiff files, merge all
	of them in a single big tiff and returns the path to this tiff
	'''

	alt = 1
	resulting_tiff_path = path_list[0]

	for i in xrange(1, len(path_list)):
		alt ^= 1
		os.system("rm -f " + output_name + str(alt))
		resulting_tiff_path = mergePair( [resulting_tiff_path, path_list[i]], output_name + str(alt) )

	os.system("rm -f " + output_name + str(alt^1))
	os.system("rm -f aux.tif")

	output_path = output_name + '.tif'
	return output_path


path_list = ['ndvi_scenes/ndvi_scene_0.tif', 'ndvi_scenes/ndvi_scene_1.tif', 'ndvi_scenes/ndvi_scene_2.tif']
merge(path_list)