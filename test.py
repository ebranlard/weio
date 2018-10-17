from __future__ import print_function, absolute_import
import weio
import glob

def tests():
    # for now only weio tests
    for f in glob.glob('_tests/*'):
        weio.read(f)
        print('[ OK ] '+f)


if __name__ == '__main__':
    tests()
