import os

execute_ndvi = './../modules/ndvi/run'
separator = ' '

def run_ndvi(path_list):
    command = execute_ndvi
    command = separator.join( (command, path_list[0], path_list[1]) )
    command = separator.join( (command, path_list[2], path_list[3]) )
    command = separator.join( (command, path_list[4]) )

    return os.system(command)