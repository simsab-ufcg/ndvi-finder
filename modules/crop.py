import os

def crop(src_path, shape_path, output_path = 'crop_sub_regions/'):

    os.system('mkdir -p ' + output_path)

    separator = ' '
    comand = separator.join( ('gdalwarp -cutline', shape_path, src_path, '-dstnodata -nan') )

    os.system(comand)

