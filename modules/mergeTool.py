import os
import coordinate
import georeference
import errorHandler

def mergePair(path_list, output_name, aux_path = ""):
	'''
	Takes paths of two distinct ndvi_tiff files, 
	merge those files and returns the path of merged tiff.
	'''

	X_INDEX = 0
	Y_INDEX = 1

	tiff1 = path_list[0]
	tiff2 = path_list[1]

	tiff1_coord = coordinate.get_coordinate(tiff1)
	tiff2_coord = coordinate.get_coordinate(tiff2)

	separator = " "
	command = separator.join( ("./modules/merge/run", tiff1, str(tiff1_coord[X_INDEX]), str(tiff1_coord[Y_INDEX])) )
	command = separator.join( (command, tiff2, str(tiff2_coord[X_INDEX]), str(tiff2_coord[Y_INDEX])) )
	command = separator.join( (command, output_name + '.tif', aux_path) )

	exit_code = os.system(command)
	output_path = output_name + '.tif'

	maxY = max(tiff1_coord[Y_INDEX], tiff2_coord[Y_INDEX])
	minX = min(tiff1_coord[X_INDEX], tiff2_coord[X_INDEX])

	output_coord = (minX, maxY)

	georeference.set_georeference(output_path, tiff1, output_coord)
	return output_path, exit_code

def merge(path_list, merged_path = "", output_name="output", aux_path = ""):
	'''
	Takes paths of N distinct ndvi_tiff files, merge all of them
	in a single big tiff and returns the path to this tiff.
	'''

	if len(path_list) == 1:
		result_path = output_name + '0.tif'
		os.system(' '.join(['mv', path_list[0], result_path]))
		return result_path
	
	merged = True if (len(merged_path)) else False
	alt = int(merged_path[-5]) if (merged) else 1
	resulting_tiff_path = merged_path if(merged) else path_list[0]

	for i in xrange(int(not merged), len(path_list)):
		alt ^= 1
		os.system("rm -f " + output_name + str(alt) + '.tif')
		resulting_tiff_path, exit_code = mergePair( [resulting_tiff_path, path_list[i]], output_name + str(alt), aux_path + 'aux.tif')

		if(exit_code >> 8) != 0:
			errorHandler.throwError('merge', exit_code)

	for i in path_list:
		os.system('rm -rf ' + i)

	os.system("rm -rf " + output_name + str(alt^1) + ".tif")
	os.system("rm -rf " + aux_path + "aux.tif")

	return resulting_tiff_path

def bestMerge(path_list, merged_path = "", output_name="output", aux_path = ""):
	if len(path_list) == 1:
		return [path_list[0]]
	elif len(path_list) == 2:
		result = merge(path_list, merged_path, output_name, aux_path)
		os.system("mv " + result + " " + path_list[0])
		return [path_list[0]]
	else:
		m = len(path_list)/2
		result = merge( 
			bestMerge(path_list[:m], merged_path, output_name, aux_path) + 
			bestMerge(path_list[m:], merged_path, output_name, aux_path)
		, merged_path, output_name, aux_path)
		
		os.system("mv " + result + " " + path_list[0])
		return [path_list[0]]