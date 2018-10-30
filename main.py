import sys
from modules import mergeTool, crop, ndvi, downloader

def main(regions, time_ranges, shape_files):
    sub_regions_raster = []
    for region in regions:
        ndvi_results = []
        for scene in regions[region]:
            scenes_raster = downloader.search(scene['path'], scene['row'], time_ranges[region]['start_date'], time_ranges[region]['end_date'])
            raster_paths = downloader.download_scene(scenes_raster, 'semi-arid/' + region + '/')
            ndvi_results += ndvi.calculate_ndvi(raster_paths)
        sub_regions_raster += crop.crop ( mergeTool.merge( ndvi_results ), shape_files[region] , region)
    mergeTool.merge( sub_regions_raster )

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