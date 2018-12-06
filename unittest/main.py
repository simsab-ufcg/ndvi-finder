import os

def test_ndvi_run():
    print '# NDVI TEST #'
    return os.system('python -m tests/testNdvi')

def test_merge_run():
    print '# MERGE TEST #'
    return os.system('python -m tests/testMerge')

def test_crop_run():
    print '# CROP TEST #'
    return os.system('python -m tests/testCrop')

if __name__ == '__main__':
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