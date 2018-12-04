import os, sys

def crop(src_path, shape_path, output_name):
    '''
    Crops a tiff based on a shapefile, then returns the resulting tiff path.
    '''

    output_path = 'crop_sub_regions/'
    os.system('mkdir -p ' + output_path)

    output_path_src_cropped = output_path + output_name + '.tif'

    separator = ' '
    command = separator.join( ('gdalwarp --config GDALWARP_IGNORE_BAD_CUTLINE YES -cutline', shape_path, src_path) )
    command = separator.join( (command, output_path_src_cropped, '-dstnodata -nan') )

    print 'Execution crop'

    exit_code = os.system(command)

    print 'Exit code:', exit_code

    if (exit_code >> 8) != 0:
    	raise SystemExit

    os.system('rm -r ' + src_path)

    return output_path_src_cropped

if __name__ == '__main__':
  src_path = sys.argv[1]
  shapefile_path = sys.argv[2]
  output_path = sys.argv[3]
  print crop(src_path, shapefile_path, output_path)