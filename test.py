from __future__ import print_function, absolute_import
import weio
import glob

def tests():
    nError=0

    #F = myFastBintest('../DLC1.1_StepSweepHuge.outb')
    #F=weio.FASTInFile('_tests/FASTAirfoil.dat')
    #F=weio.FASTInFile('_TODO/FASTIn_AD14_arfl.dat')
    #fileformat,F = weio.detectFormat('_tests/FASTIn_AD15_bld.dat')
    #print(fileformat)
    #F=weio.CSVFile('_tests/FASTIn_AD15_bld.dat')
    #F=weio.HAWC2AEFile('_tests/FASTIn_BD.dat')
    #F=weio.FASTInFile('_tests/FASTIn_AD15_arfl.dat')
    #F=weio.FASTOutFile('_tests/FASTOut_HD.elev')
    #F=weio.CSVFile('_TODO/template_YYYYMMDD_wtg_response_steady_state.txt')
#     F=weio.HAWC2DatFile('_TODO/Hawc2ascii.dat')
    #F=weio.HAWC2DatFile('_tests/HAWC2_out_bin.dat')
    #F=weio.HAWC2DatFile('_TODO/FLEX_wetb/test.int')
    #F=weio.HAWC2DatFile('_TODO/hawc2bin_chantest_2.sel')
    #print(F.toDataFrame().mean())
    #return
    #return

    for f in glob.glob('_tests/*.*'):
        try:
            fileformat=None
            fileformat,F = weio.detectFormat(f)
            #fr=weio.read(f,fileformat)
            dfs = F.toDataFrame()
            # 
            if not isinstance(dfs,dict):
                if dfs is None:
                    n = 0
                elif len(dfs)==0:
                    n = 0
                else:
                    n = 1
            else:
                n=len(dfs)
            #print(fr.toDataFrame())
            s=fileformat.name
            s=s.replace('file','')[:20]
            print('[ OK ] {:30s}\t{:20s}\t{}'.format(f[:30],s,n))
        except weio.FormatNotDetectedError:
            nError += 1
            print('[FAIL] {:30s}\tFormat not detected'.format(f[:30]))
        except:
            nError += 1
            print('[FAIL] {:30s}\tException occured'.format(f[:30]))
            raise 

    if nError>0:
        raise Exception('Some tests failed')


if __name__ == '__main__':
    tests()
