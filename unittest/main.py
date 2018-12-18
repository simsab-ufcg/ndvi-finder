import os, sys

def test_ndvi_run():
    return os.system('python tests/testNdvi.py > logs/out_ndvi')

def test_merge_run():
    return os.system('python tests/testMerge.py > logs/out_merge')

def test_crop_run():
    return os.system('python tests/testCrop.py > logs/out_crop')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Insufficient arguments. Use 'python main.py run|setup'"
    elif sys.argv[1] == 'setup':
        os.system("make -C ../modules/merge/")
        os.system("make -C ../modules/ndvi/")
        os.system("rm -rf results logs")
        os.system("mkdir -p results logs")
    elif sys.argv[1] == 'run':
        test_ndvi = not test_ndvi_run()
        test_merge = not test_merge_run()
        test_crop = not test_crop_run()

        if test_ndvi and test_merge and test_crop:
            print 'PASSED ALL TESTS'
        else:
            print '# STATUS TEST #'
            print 'TEST NDVI    :' , ('OK' if test_ndvi else 'BREAK')
            print 'TEST MERGE   :' , ('OK' if test_merge else 'BREAK')
            print 'TEST CROP    :' , ('OK' if test_crop else 'BREAK')