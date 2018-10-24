from __future__ import print_function, absolute_import
import weio
import glob

def tests():
    nError=0

    #F = myFastBintest('../Test.outb')
    #F = myFastBintest('../DLC1.1_StepSweepHuge.outb')
    #F=weio.FASTOutFile('../Test.outb');
    #F=weio.FASTOutFile('../Test.outb');
    #F=weio.wetb.fast.fast_io.load_ascii_output('_tests/FASTOut_Hydro.out')
    #F=weio.FASTOutFile('../DLC1.1_StepSweepHuge.outb')

    #return

    for f in glob.glob('_tests/*.*'):
        fileformat=None
        try:
            fileformat,F = weio.detectFormat(f)
            fr=weio.read(f,fileformat)
            #print(fr.toDataFrame())
            print('[ OK ] '+f + ' read as {}'.format(fileformat))
        except:
            nError += 1
            print('[FAIL] '+f + ' read as {}'.format(fileformat))
            raise 

    if nError>0:
        raise Exception('Some tests failed')


if __name__ == '__main__':
    tests()
