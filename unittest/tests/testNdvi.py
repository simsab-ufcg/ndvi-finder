from modules import utils as ut

def set_up_l8():
    inputs = {
        'test01': ['inputs/ndvi/l8_b4.tif', 'inputs/ndvi/l8_b5.tif', 'inputs/ndvi/l8_bqa_full.tif', 'inputs/ndvi/l8_mtl.txt', 'results/output_ndvi_t1.tif'],
        'test02': ['inputs/ndvi/l8_b4.tif', 'inputs/ndvi/l8_b5.tif', 'inputs/ndvi/l8_bqa_empty.tif', 'inputs/ndvi/l8_mtl.txt', 'results/output_ndvi_t2.tif'],
        'test03': ['inputs/ndvi/l8_b4.tif', 'inputs/ndvi/l8_b5.tif', 'inputs/ndvi/l8_bqa_top.tif', 'inputs/ndvi/l8_mtl.txt', 'results/output_ndvi_t3.tif'],
        'test04': ['inputs/ndvi/l8_b4.tif', 'inputs/ndvi/l8_b5.tif', 'inputs/ndvi/l8_bqa_down.tif', 'inputs/ndvi/l8_mtl.txt', 'results/output_ndvi_t4.tif'],
        'test05': ['inputs/ndvi/l8_b4.tif', 'inputs/ndvi/l8_b5.tif', 'inputs/ndvi/l8_bqa_left.tif', 'inputs/ndvi/l8_mtl.txt', 'results/output_ndvi_t5.tif'],
        'test06': ['inputs/ndvi/l8_b4.tif', 'inputs/ndvi/l8_b5.tif', 'inputs/ndvi/l8_bqa_right.tif', 'inputs/ndvi/l8_mtl.txt', 'results/output_ndvi_t6.tif'],
    }

    outputs = {
        'test01': 'outputs/ndvi/l8_ndvi_full.tif',
        'test02': 'outputs/ndvi/l8_ndvi_empty.tif',
        'test03': 'outputs/ndvi/l8_ndvi_top.tif',
        'test04': 'outputs/ndvi/l8_ndvi_down.tif',
        'test05': 'outputs/ndvi/l8_ndvi_left.tif',
        'test06': 'outputs/ndvi/l8_ndvi_right.tif',
    }

    return inputs, outputs

def set_up_l5():
    inputs = {
        'test01': ['inputs/ndvi/l5_b3.tif', 'inputs/ndvi/l5_b4.tif', 'inputs/ndvi/l5_bqa_full.tif', 'inputs/ndvi/l5_mtl.txt', 'results/output_ndvi_t1.tif'],
        'test02': ['inputs/ndvi/l5_b3.tif', 'inputs/ndvi/l5_b4.tif', 'inputs/ndvi/l5_bqa_empty.tif', 'inputs/ndvi/l5_mtl.txt', 'results/output_ndvi_t2.tif'],
        'test03': ['inputs/ndvi/l5_b3.tif', 'inputs/ndvi/l5_b4.tif', 'inputs/ndvi/l5_bqa_top.tif', 'inputs/ndvi/l5_mtl.txt', 'results/output_ndvi_t3.tif'],
        'test04': ['inputs/ndvi/l5_b3.tif', 'inputs/ndvi/l5_b4.tif', 'inputs/ndvi/l5_bqa_down.tif', 'inputs/ndvi/l5_mtl.txt', 'results/output_ndvi_t4.tif'],
        'test05': ['inputs/ndvi/l5_b3.tif', 'inputs/ndvi/l5_b4.tif', 'inputs/ndvi/l5_bqa_left.tif', 'inputs/ndvi/l5_mtl.txt', 'results/output_ndvi_t5.tif'],
        'test06': ['inputs/ndvi/l5_b3.tif', 'inputs/ndvi/l5_b4.tif', 'inputs/ndvi/l5_bqa_right.tif', 'inputs/ndvi/l5_mtl.txt', 'results/output_ndvi_t6.tif'],
    }

    outputs = {
        'test01': 'outputs/ndvi/l5_ndvi_full.tif',
        'test02': 'outputs/ndvi/l5_ndvi_empty.tif',
        'test03': 'outputs/ndvi/l5_ndvi_top.tif',
        'test04': 'outputs/ndvi/l5_ndvi_down.tif',
        'test05': 'outputs/ndvi/l5_ndvi_left.tif',
        'test06': 'outputs/ndvi/l5_ndvi_right.tif',
    }

    return inputs, outputs


def test_ndvi(inputs, outputs, tests):
    for test in tests:
        exit_code = ut.run_ndvi(inputs[test])
        ut.verify_result(exit_code)

        exit_code = ut.compare_tiffs(outputs[test], inputs[test][4])
        ut.verify_result(exit_code)

        ut.remove_file(inputs[test][4])


if __name__ == '__main__':
    tests = ['test01', 'test02', 'test03', 'test04', 'test05', 'test06']

    inputs_l8, outputs_l8 = set_up_l8()
    test_ndvi(inputs_l8, outputs_l8, tests)

    inputs_l5, outputs_l5 = set_up_l5()
    test_ndvi(inputs_l5, outputs_l5, tests)