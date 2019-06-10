import unittest
import glob
import weio
import os
MyDir=os.path.dirname(__file__)

class Test(unittest.TestCase):

    def test_read_all(self):
        #fileformat,F = weio.detectFormat('_tests/FASTIn_ED_bld.dat')
        #F = weio.CSVFile('_tests/CSVComma_Fail.csv')
        #F = weio.FLEXBladeFile('_TODO/.bla')
        #F.toDataFrame()
        #print(F)
        #print(fileformat)
        #print(F.toDataFrame())
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
                    print('[ OK ] {:30s}\t{:20s}\t{}'.format(os.path.basename(f)[:30],s,n))
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

    def DF(self,FN):
        """ Reads a file with weio and return a dataframe """ 
        return weio.read(os.path.join(MyDir,FN)).toDataFrame()
 
    def test_CSV(self):
        self.assertEqual(self.DF('CSVAutoCommentChar.txt').shape,(11,6))
 
        DF=self.DF('CSVColInHeader.csv')
        self.assertEqual(all(DF.columns.values==['ColA','ColB','ColC']),True)
        self.assertEqual(DF.shape,(2,3))
 
        DF=self.DF('CSVColInHeader2.csv')
        self.assertEqual(all(DF.columns.values==['ColA','ColB','ColC']),True)
        self.assertEqual(DF.shape,(2,3))
 
        DF=self.DF('CSVColInHeader3.csv')
        self.assertEqual(all(DF.columns.values==['ColA','ColB','ColC']),True)
        self.assertEqual(DF.shape,(2,3))

        DF=self.DF('CSVComma_UTF16.csv')
        self.assertEqual(DF.shape,(4,3))

 
        self.assertEqual(self.DF('CSVComma.csv').shape,(4,2))
        self.assertEqual(self.DF('CSVDateNaN.csv').shape,(11,2))
        self.assertEqual(self.DF('CSVNoHeader.csv').shape,(4,2))
        self.assertEqual(self.DF('CSVSemi.csv').shape,(3,2))
        self.assertEqual(self.DF('CSVSpace_ExtraCol.csv').shape,(5,4))
        self.assertEqual(self.DF('CSVTab.csv').shape,(5,2))
 
        DF = self.DF('CSVTwoLinesHeaders.txt')
        self.assertEqual(DF.columns.values[-1],'GenTq_(kN m)')
        self.assertEqual(DF.shape,(9,6))
 
    def test_FASTOut(self):
        self.assertEqual(self.DF('FASTOut.out').values[-1,1],1036)
 
    def test_FASTOutBin(self):
        F=weio.read(os.path.join(MyDir,'FASTOutBin.outb'))
        M=F.toDataFrame()
        self.assertAlmostEqual(M['GenPwr_[kW]'].values[-1],40.57663190807828)
 
    def test_FLEX(self):
        self.assertAlmostEqual(self.DF('FLEXProfile.pro')['pc_set_2_t_57.0'].values[2,2],0.22711022)
        Bld=self.DF('FLEXBlade002.bld')
        self.assertAlmostEqual(Bld['r_[m]'].values[-1],61.5)
        self.assertAlmostEqual(Bld['Mass_[kg/m]'].values[-1],10.9)
        self.assertAlmostEqual(Bld['Chord_[m]'].values[3],3.979815059)
if __name__ == '__main__':
    unittest.main()
