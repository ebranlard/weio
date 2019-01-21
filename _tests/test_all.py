import unittest
import glob
import weio
import os
MyDir=os.path.dirname(__file__)

class Test(unittest.TestCase):

    def test_read_all(self):
        #fileformat,F = weio.detectFormat('_tests/FASTIn_ED_bld.dat')
        #F = weio.FASTInFile('_tests/FASTIn_AD15.dat')
        #F.toDataFrame()
        #print(fileformat)
        #print(F.toDataFrame())
        #print(F)
        #return
        DEBUG=False
        nError=0
        for f in glob.glob(os.path.join(MyDir,'*.*')):
            if os.path.splitext(f)[-1] in ['.py','.pyc']:
                continue
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
                if DEBUG:
                    print('[ OK ] {:30s}\t{:20s}\t{}'.format(f[:30],s,n))
            except weio.FormatNotDetectedError:
                nError += 1
                if DEBUG:
                    print('[FAIL] {:30s}\tFormat not detected'.format(f[:30]))
            except:
                nError += 1
                if DEBUG:
                    print('[FAIL] {:30s}\tException occured'.format(f[:30]))
                raise 

        if nError>0:
            raise Exception('Some tests failed')


    def test_FASTOut(self):
        F=weio.read(os.path.join(MyDir,'FASTOut.out'))
        M=F.toDataFrame()
        self.assertEqual(M.values[-1,1],1036)

    def test_FASTOutBin(self):
        F=weio.read(os.path.join(MyDir,'FASTOutBin.outb'))
        M=F.toDataFrame()
        self.assertAlmostEqual(M['GenPwr_[kW]'].values[-1],40.57663190807828)
 
if __name__ == '__main__':
    unittest.main()
