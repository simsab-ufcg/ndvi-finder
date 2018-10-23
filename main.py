import sys
from modules import downloader

def main():
    
    sub_regions_raster = []
    for region in regions:
        ndvi_results = []
        for scene in region:
            scene_raster = download( scene )
            ndvi_results.append( ndvi_calculate(scene_raster) )
        sub_region = merge(region)
        sub_regions_raster.append( crop(sub_region) )
    merge( sub_regions_raster )

if __name__ == '__main__':
    main()