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
    #F=weio.FASTOutFile('_TODO/OUT.elm')
    #print(F.toDataFrame())
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
            s=s[:s.find('(')].replace('file','')[:20]
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
