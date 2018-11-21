import sys, os
from modules import mergeTool, crop, ndvi, downloader, sort

def getPathRow(path, row):
    return str(path) + str(row)

def main(regions, time_ranges, shape_files):
    sub_regions_raster = []
    resume = False
    for region in regions:
        if os.path.isfile('semi-arid/' + region + '/.secretFlag'):
            sub_regions_raster.append( 'crop_sub_regions/' + region + '.tif')
            resume = True
            continue
        merged_ndvi_result = ""
        for scene in regions[region]:
            if os.path.isfile('semi-arid/' + region + '/' + getPathRow(int(scene['path']), int(scene['row'])) + '/.secretFlag'):
                resume = True
                continue
            if resume:
                resume = False
                os.system("cp backup_merge.tif output0.tif")
                merged_ndvi_result = 'output0.tif'

            scenes_raster = downloader.search(scene['path'], scene['row'], time_ranges[region]['start_date'], time_ranges[region]['end_date'], time_ranges[region]['pos_rain'])
            sorted_scenes_raster = sort.sort(scenes_raster)
            raster_paths = downloader.download_scene(sorted_scenes_raster, 'semi-arid/' + region + '/')
            ndvi_results, ndvi_utils = ndvi.calculate_ndvi(raster_paths)
            
            if ndvi_results:
                merged_ndvi_result = mergeTool.merge(ndvi_results, merged_ndvi_result)
                os.system('rm -rf backup_merge.tif')
                os.system("cp " + merged_ndvi_result + " backup_merge.tif")
            os.system("echo '' >semi-arid/" + region + '/' + getPathRow(int(scene['path']), int(scene['row'])) + '/.secretFlag')
            
        sub_regions_raster += crop.crop ( merged_ndvi_result, shape_files[region] , region)
        os.system("echo '' >semi-arid/" + region + '/.secretFlag')

    mergeTool.merge( sub_regions_raster )

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Insufficient arguments. Use 'python main.py run|setup'"
    elif sys.argv[1] == 'setup':
        os.system("make -C modules/merge/")
        os.system("make -C modules/ndvi/")
        downloader.setup()
    elif sys.argv[1] == 'run':
        if not os.path.isfile('.secretFlag'):
            os.system("find . -iname '.secretFlag' | xargs -n 1 rm -rf")
            os.system("echo '' >.secretFlag")
        regions = downloader.parse_path_and_rows('samples/semi-arid/path_row.txt')
        time_ranges = downloader.parse_time_periods('samples/semi-arid/time_range.csv')
        shape_files = downloader.get_shape_files(regions, 'samples/semi-arid/')
        main(regions, time_ranges, shape_files)
        os.system('rm .secretFlag')
    else:
        print "Unsupported operation"