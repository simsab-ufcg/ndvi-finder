import os

separator = ' '

def verify_result(exit_code):
    if exit_code != 0:
        exit(1)

def remove_file(path_file):
    os.system('rm -rf ' + path_file)

def run_ndvi(path_list):
    command = './../modules/ndvi/run'
    command = separator.join( (command, path_list[0], path_list[1]) )
    command = separator.join( (command, path_list[2], path_list[3]) )
    command = separator.join( (command, path_list[4]) )

    return os.system(command)

def run_crop(path_list):
    command = 'gdalwarp --config GDALWARP_IGNORE_BAD_CUTLINE YES -cutline'
    command = separator.join( (command, path_list[0], path_list[1], path_list[2]) )
    command = separator.join( (command, '-dstnodata -nan') )

    return os.system(command)

