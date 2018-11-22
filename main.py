import sys, os, subprocess
from modules import mergeTool, crop, ndvi, downloader, sort, subregion

def getPathRow(path, row):
    return str(path) + str(row)

def main(regions):
    sub_regions_raster = []
    subprocesses = []
    resume = False
    for region in regions:

        print 'Processing ' + region + ' subregion.'
        sub_regions_raster.append('crop_sub_regions/' + region + '.tif')
        FNULL = open(os.devnull, 'w')
        subprocesses.append((subprocess.Popen(' '.join(['python', 'subregion.py', region]), 
          shell=True, stdout=FNULL, stderr=FNULL), region))

    for subprocesse, region in subprocesses:
        print 'Finish ' + region + 'subregion.'
        subprocesse.wait()

    mergeTool.merge( sub_regions_raster, "", "NDVI_FINAL")

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
        regions = downloader.parse_path_and_rows('samples/semi-arid/path_row.txt').keys()
        main(regions)
        os.system('rm .secretFlag')
    else:
        print "Unsupported operation"