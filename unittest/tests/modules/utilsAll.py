import os

separator = ' '

def compare_tiffs(tiff1, tiff2):
    command = separator.join( ('gdalcompare.py', tiff1, tiff2 ) )
    return os.system(command)

def verify_result(exit_code):
    if exit_code != 0:
        exit(1)

def remove_file(path_file):
    os.system('rm -rf ' + path_file)