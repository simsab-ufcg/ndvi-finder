import os
import coordinate
import georeference

def mergePair(path_list, output_name):
	'''
	This function takes the paths of two distinct ndvi_tif
	files, merge them and returns the path of merged tif
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

	#print command
	#os.system(command)

	output_path = output_name + '.tif'

	if tiff1_coord[Y_INDEX] > tiff2_coord[Y_INDEX]:
		output_coord = tiff1_coord
	else:
		output_coord = tiff2_coord

	georeference.set_georeference(output_path, tiff1, output_coord)
	return output_path

def merge(path_list, output_name="output"):
	resulting_tif_path = path_list[0]

	for i in xrange(1, len(path_list)):
		resulting_tif_path = mergePair( [resulting_tif_path, path_list[i]], output_name )

	output_path = output_name + '.tif'
	return output_path


#path_list = ["inputTeste/maceio/ndviMaceio.tif", "inputTeste/natal/ndviNatal.tif"]
#merge(path_list)