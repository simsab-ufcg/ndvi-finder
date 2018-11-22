import sys, os

import mergeTool, crop, ndvi, downloader, sort

def getPathRow(path, row):
    return str(path) + str(row)

def process(region, time_range, shape_files, scenes):
    
    path_row_raster = []
    region_path = 'semi-arid/' + region + '/'


    if os.path.isfile(region_path + '.secretFlag'):
        return

    for scene in scenes:

        merged_ndvi_result = ""
        ndvi_final_output = region_path + getPathRow(int(scene['path']), int(scene['row'])) + 'NDVI_FINAL.tif'

        if os.path.isfile(region_path + getPathRow(int(scene['path']), int(scene['row'])) + '/.secretFlag'):
            resume = True
            path_row_raster.append(ndvi_final_output)
            continue

        scenes_raster = downloader.search(scene['path'], scene['row'], time_range['start_date'], time_range['end_date'], time_range['pos_rain'])
        sorted_scenes_raster = sort.sort(scenes_raster)
        raster_paths = downloader.download_scene(sorted_scenes_raster, region_path)
        ndvi_results = ndvi.calculate_ndvi(raster_paths)
        
        if ndvi_results:
            merged_ndvi_result = mergeTool.merge(ndvi_results, merged_ndvi_result, region_path + getPathRow(int(scene['path']), int(scene['row'])) + '/output')
            os.system(' '.join(['mv', merged_ndvi_result, ndvi_final_output]))
            path_row_raster.append(ndvi_final_output)

        os.system("echo '' >"+ region_path + getPathRow(int(scene['path']), int(scene['row'])) + '/.secretFlag')

    merged_ndvi_result = mergeTool.bestMerge(path_row_raster, region_path + 'bestMerge/')[0]
    sub_region_raster = crop.crop ( merged_ndvi_result, shape_files , region)
    os.system("echo '' >semi-arid/" + region + '/.secretFlag')

    return

if __name__ == '__main__':
    this_region = sys.argv[1]
    regions = downloader.parse_path_and_rows('samples/semi-arid/path_row.txt')
    time_ranges = downloader.parse_time_periods('samples/semi-arid/time_range.csv')
    shape_files = downloader.get_shape_files(regions, 'samples/semi-arid/')
    process(this_region, time_ranges[this_region], shape_files[this_region], regions[this_region])