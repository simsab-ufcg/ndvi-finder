import os

def crop(src_path, shape_path, output_name, output_path = 'crop_sub_regions/'):

    os.system('mkdir -p ' + output_path)

    output_path_src_cropped = output_path + output_name + '.tif'

    separator = ' '
    command = separator.join( ('gdalwarp -cutline', shape_path, src_path) )
    command = separator.join( (command, output_path_src_cropped, '-dstnodata -nan') )

    os.system(command)

    #os.system('rm -r src_path')

    return output_path_src_cropped

crop('sample1/ndvi.tif', 'shapefile/Limite_Externo_AMJJ.shp', 'AMJJ')