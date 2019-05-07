from modules import utils as ut
from modules import compare as comp

def set_up():
    inputs = {
        'test01': ['inputs/crop/shapefile/full.shp', 'inputs/crop/any_tiff.tif', 'results/output_any_tiff_full.tif'],
        'test02': ['inputs/crop/shapefile/empty.shp', 'inputs/crop/any_tiff.tif', 'results/output_any_tiff_empty.tif'],
        'test03': ['inputs/crop/shapefile/top.shp', 'inputs/crop/any_tiff.tif', 'results/output_any_tiff_top.tif'],
        'test04': ['inputs/crop/shapefile/down.shp', 'inputs/crop/any_tiff.tif', 'results/output_any_tiff_down.tif'],
        'test05': ['inputs/crop/shapefile/left.shp', 'inputs/crop/any_tiff.tif', 'results/output_any_tiff_left.tif'],
        'test06': ['inputs/crop/shapefile/right.shp', 'inputs/crop/any_tiff.tif', 'results/output_any_tiff_right.tif']
    }

    outputs = {
        'test01': 'outputs/crop/any_tiff_full.tif',
        'test02': 'outputs/crop/any_tiff_empty.tif',
        'test03': 'outputs/crop/any_tiff_top.tif',
        'test04': 'outputs/crop/any_tiff_down.tif',
        'test05': 'outputs/crop/any_tiff_left.tif',
        'test06': 'outputs/crop/any_tiff_right.tif'
    }

    return inputs, outputs

def test_crop(inputs, outputs, tests):
    for test in tests:
        exit_code = ut.run_crop(inputs[test])
        ut.verify_result(exit_code)

        exit_code = comp.compare_tiffs(outputs[test], inputs[test][2])
        ut.verify_result(exit_code)

        ut.remove_file(inputs[test][2])

if __name__ == '__main__':
    tests = ['test01', 'test02', 'test03', 'test04', 'test05', 'test06']

    inputs, outputs = set_up()
    test_crop(inputs, outputs, tests)