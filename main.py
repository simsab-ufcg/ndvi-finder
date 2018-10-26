import sys
from modules import downloader

def main(regions, time_ranges, shape_files):
    sub_regions_raster = []
    for region in regions:
        ndvi_results = []
        for scene in regions[region]:
            scenes_raster = downloader.search(scene['path'], scene['row'], time_ranges[region]['start_date'], time_ranges[region]['end_date'])
            raster_paths = downloader.download_scene(scenes_raster, 'semi-arid/' + region + '/')
            ndvi_results += ndvi_calculate(raster_paths) ## TODO return ndvi_paths and remove unecessary files
        sub_regions_raster += crop ( merge( ndvi_results ), shape_files[region] , region) ## TODO return merged path and remove unecessary files
    merge( sub_regions_raster ) ## TODO return merged path and remove unecessary files

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Insufficient arguments"
    if sys.argv[1] == 'setup':
        downloader.setup()
    elif sys.argv[1] == 'run':
        regions = downloader.parse_path_and_rows('samples/semi-arid/path_row.txt')
        time_ranges = downloader.parse_time_periods('samples/semi-arid/time_range.csv')
        shape_files = downloader.get_shape_files(regions, 'sample/semi-arid/')
        main(regions, time_ranges, shape_files)
    else:
        print "Unsupported operation"