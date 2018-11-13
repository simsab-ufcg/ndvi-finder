import os

def crop(src_path, shape_path, output_name):
    '''
    Crops a tiff based on a shapefile, then returns the resulting tiff path.
    '''

    output_path = 'crop_sub_regions/'
    os.system('mkdir -p ' + output_path)

    output_path_src_cropped = output_path + output_name + '.tif'

    separator = ' '
    command = separator.join( ('gdalwarp -cutline', shape_path, src_path) )
    command = separator.join( (command, output_path_src_cropped, '-dstnodata -nan') )

    exit_code = os.system(command)

    if (exit_code >> 8) != 0:
    	raise SystemExit

    os.system('rm -r ' + src_path)

    return output_path_src_cropped