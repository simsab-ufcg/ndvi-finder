import os

def mergePair(path_list, output_name):
	# path_list format: ["path/tif1", "path/tif2"]
	# returns path to merged_tif

	separator = " "
	command = separator.join( ("./run", path_list[0], path_list[1]) )
	command = separator.join( (command, output_name + '.tif', output_name + '.txt') )

	os.system(command)

	# it may be necessary to generate a MTL.txt for output tiff

	path_to_output = output_name + '.tif'
	return path_to_output

def merge(path_list, output_name="output"):
	auxiliar_path = path_list[0]

	for i in xrange(1, len(path_list)):
		auxiliar_path = mergePair([auxiliar_path, path_list[i]], output_name)

	path_to_output = output_name + '.tif'
	return path_to_output