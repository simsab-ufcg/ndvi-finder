import sys, os
from modules import mergeTool, crop, ndvi, downloader

def build_directory_ndvi(normalize_ndvi_path = "ndvi_scenes_normalize/"):
    os.system('rm -rf ' + normalize_ndvi_path)
    os.system('mkdir -p ' + normalize_ndvi_path)

def main(regions, time_ranges, shape_files):
    sub_regions_raster = []
    for region in regions:
        ndvi_results = []
        build_directory_ndvi()
        for scene in regions[region]:
            scenes_raster = downloader.search(scene['path'], scene['row'], time_ranges[region]['start_date'], time_ranges[region]['end_date'])
            raster_paths = downloader.download_scene(scenes_raster, 'semi-arid/' + region + '/')
            ndvi_results += ndvi.calculate_ndvi(raster_paths, len(ndvi_results))
        sub_regions_raster += crop.crop ( mergeTool.merge( ndvi_results ), shape_files[region] , region)
    mergeTool.merge( sub_regions_raster )

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Insufficient arguments. Use 'python main.py run|setup'"
    elif sys.argv[1] == 'setup':
        os.system("make -C modules/merge/")
        os.system("make -C modules/ndvi/")
        downloader.setup()
    elif sys.argv[1] == 'run':
        regions = downloader.parse_path_and_rows('samples/semi-arid/path_row.txt')
        time_ranges = downloader.parse_time_periods('samples/semi-arid/time_range.csv')
        shape_files = downloader.get_shape_files(regions, 'samples/semi-arid/')
        main(regions, time_ranges, shape_files)
    else:
        print "Unsupported operation"