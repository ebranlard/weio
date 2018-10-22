from __future__ import print_function, absolute_import
import weio
import glob

def tests():
    # for now only weio tests
    nError=0
    #f=weio.FASTInFile('_tests/FASTAirfoil.dat')
    #f=weio.FASTOutFile('_tests/FASTOutBin.outb')
    #df=f.toDataFrame()
    #f=weio.HAWC2AEFile('_tests/HAWC2_ae.dat')
    #df=f.toDataFrame()
    #f=weio.HAWC2PCFile('_tests/HAWC2_pc.dat')
    #df=f.toDataFrame()
    #print(df)
    #f=weio.CSVFile('_tests/CSVComma.csv')
    #f=weio.CSVFile('_tests/FASTWnd.wnd',commentChar='!',colNamesLine=-2)
    #f=weio.FASTWndFile('_tests/FASTWnd.wnd')
    #print(f.toDataFrame())
    #f.test_ascii()
    #return
    #f=weio.CSVFile('_tests/CSVNoHeader.csv')
    #print(f.toDataFrame())
    #f=weio.CSVFile('_tests/CSVDateNaN.csv')
    #print(f.toDataFrame())
    #f=weio.CSVFile('_tests/CSVSemi.csv')
    #print(f.toDataFrame())
    #f=weio.CSVFile('_tests/CSVSemi.csv',commentLines=[0])
    #print(f.toDataFrame())
    #f=weio.CSVFile('_tests/CSVColInHeader.csv')
    #f=weio.CSVFile('_tests/CSVColInHeader.csv',commentChar='!',colNamesLine=-2)
    #print(f.toDataFrame())
    #f=weio.CSVFile('_tests/CSVColInHeader2.csv',commentChar='!',colNamesLine=-1)
    #print(f.toDataFrame())
#     f.read()
#     print(f.toDataFrame())
#     f=weio.CSVFile('_tests/CSVSpace_ExtraCol.csv')
#     print(f.toDataFrame())
#     f=weio.CSVFile('_tests/CSVTab.csv')
#     print(f.toDataFrame())
    #import pdb
    #pdb.set_trace()


    for f in glob.glob('_tests/*.*'):
        fileformat=None
        try:
            fileformat = weio.detectFormat(f)
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
