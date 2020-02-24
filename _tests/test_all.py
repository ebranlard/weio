import unittest
import glob
import weio
import os
MyDir=os.path.dirname(__file__)

class Test(unittest.TestCase):
    def test_000_debug(self):
        #fileformat,F = weio.detectFormat('_tests/FASTIn_ED_bld.dat')
        #F = weio.CSVFile('_tests/CSVComma_Fail.csv')
        #F = weio.FASTInFile('../_tests/FASTIn_ExtPtfm_SubSef.dat')
        #F = weio.FASTLinFile('../_tests/FASTOutLin_New.lin')
        #dfs=F.toDataFrame()
        #print(F.toDataFrame())
        #print(F)
        #return
        #print(fileformat)
        pass

    def test_001_read_all(self):
        DEBUG=True
        nError=0
        for f in glob.glob(os.path.join(MyDir,'*.*')):
            if os.path.splitext(f)[-1] in ['.py','.pyc'] or f.find('_TMP')>0:
                continue
            try:
                fileformat=None
                F=None
                fileformat,F = weio.detectFormat(f)
                #fr=weio.read(f,fileformat)
                dfs = F.toDataFrame()
                ## 
                if not isinstance(dfs,dict):
                    if dfs is None:
                        n = 0
                    elif len(dfs)==0:
                        n = 0
                    else:
                        n = 1
                else:
                    n=len(dfs)
                ##print(fr.toDataFrame())
                s=fileformat.name
                s=s.replace('file','')[:20]
                if DEBUG:
                    print('[ OK ] {:30s}\t{:20s}\t{}'.format(os.path.basename(f)[:30],s,n))
            except weio.FormatNotDetectedError:
                nError += 1
                if DEBUG:
                    print('[FAIL] {:30s}\tFormat not detected'.format(os.path.basename(f)[:30]))
            except:
                nError += 1
                if DEBUG:
                    print('[FAIL] {:30s}\tException occurred'.format(os.path.basename(f)[:30]))
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

    def test_FASTWnd(self):
        F=weio.read(os.path.join(MyDir,'FASTWnd.wnd'))
        F.test_ascii(bCompareWritesOnly=False,bDelete=True)

    def test_FASTIn(self):
        F=weio.read(os.path.join(MyDir,'FASTIn_BD.dat'))
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        self.assertEqual(F['PitchK'],2.0e+07)
        self.assertEqual(F['MemberGeom'][-1,2],61.5)
        self.assertEqual(F['MemberGeom'][-2,3],0.023000)

        F=weio.read(os.path.join(MyDir,'FASTIn_ED.dat'))
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        self.assertEqual(F['RotSpeed'],0.2)

        F=weio.read(os.path.join(MyDir,'FASTIn_ED_bld.dat'))
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        self.assertEqual(F['BldEdgSh(6)'],-0.6952)

        F=weio.read(os.path.join(MyDir,'FASTIn_ED_twr.dat'))
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        self.assertEqual(F['AdjFASt'],1)

        F=weio.read(os.path.join(MyDir,'FASTIn_AD15.dat'))
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        self.assertEqual(F['TipLoss'],'True')

        F=weio.read(os.path.join(MyDir,'FASTIn_ExtPtfm_SubSef.dat'))
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        self.assertEqual(F['StiffnessMatrix'][2,2],1.96653266e+09)

        F=weio.read(os.path.join(MyDir,'FASTIn_HD.dat'))
        #F.test_ascii(bCompareWritesOnly=True,bDelete=True) # TODO
        self.assertEqual(F['RdtnDT'],0.0125)

        F=weio.read(os.path.join(MyDir,'FASTIn_IF_NoHead.dat'))
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        self.assertEqual(F['Z0'],0.03)

        F=weio.read(os.path.join(MyDir,'FASTIn_SbD.dat'))
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        self.assertEqual(F['Joints'][0,3],-100)
        self.assertEqual(int(F['Members'][0,1]),1)
        self.assertEqual(int(F['Members'][0,2]),2)

        F=weio.read(os.path.join(MyDir,'FASTIn_SD.dat'))
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        self.assertEqual(F['PitManRat(1)'],2)

 
    def test_FASTOut(self):
        self.assertEqual(self.DF('FASTOut.out').values[-1,1],1036)
 
    def test_FASTOutBin(self):
        F=weio.read(os.path.join(MyDir,'FASTOutBin.outb'))
        M=F.toDataFrame()
        self.assertAlmostEqual(M['GenPwr_[kW]'].values[-1],40.57663190807828)

    def test_FASTLin(self):
        F=weio.FASTLinFile(os.path.join(MyDir,'FASTOutLin.lin'))
        self.assertAlmostEqual(F['A'][3,1], 3.91159454E-04 )
        self.assertAlmostEqual(F['u'][7]   ,4.00176055E+04)

        F=weio.FASTLinFile(os.path.join(MyDir,'FASTOutLin_EDM.lin'))
        dfs=F.toDataFrame()
        M=dfs['M']
        self.assertAlmostEqual(M['7_TwFADOF1']['7_TwFADOF1'],0.436753E+06)
        self.assertAlmostEqual(M['13_GeAz']['13_GeAz']     , 0.437026E+08)

 
    def test_FLEX(self):
        self.assertAlmostEqual(self.DF('FLEXProfile.pro')['pc_set_2_t_57.0'].values[2,2],0.22711022)
        Bld=self.DF('FLEXBlade002.bld')
        self.assertAlmostEqual(Bld['r_[m]'].values[-1],61.5)
        self.assertAlmostEqual(Bld['Mass_[kg/m]'].values[-1],10.9)
        self.assertAlmostEqual(Bld['Chord_[m]'].values[3],3.979815059)

    def test_HAWC2(self):
        F=weio.read(os.path.join(MyDir,'HAWC2_out_ascii.dat'))
        DF=F.toDataFrame()
        self.assertEqual(DF.values[-1,1],-1.72572E+03)
        self.assertEqual(DF.values[-1,-1], 3.63349E+03)
        self.assertEqual(DF.columns[0], 'Time_[s]')
        self.assertEqual(DF.columns[1], 'WSP gl. coo.,Vy_[m/s]')

        # Test that "exported dat files" are the same
        # NOTE: cannot do comparison of sel files since names are different
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        os.remove(os.path.join(MyDir,'HAWC2_out_ascii_TMP.sel'))
        os.remove(os.path.join(MyDir,'HAWC2_out_ascii_TMP2.sel'))

    def test_BHAWC(self):
        F=weio.read(os.path.join(MyDir,'BHAWC_out_ascii.sel'))
        DF=F.toDataFrame()
        self.assertEqual(DF.values[-1,1], 147.85)
        self.assertEqual(DF.columns[0], 't_[s]')
        self.assertEqual(DF.columns[1], 'ang_azi_[deg]')

        # Testing that "exported" sel files are the same
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        os.remove(os.path.join(MyDir,'BHAWC_out_ascii_TMP.dat'))
        os.remove(os.path.join(MyDir,'BHAWC_out_ascii_TMP2.dat'))

        # Testing that "exported" dat files are the same
        F=weio.read(os.path.join(MyDir,'BHAWC_out_ascii.dat'))
        F.test_ascii(bCompareWritesOnly=True,bDelete=True)
        os.remove(os.path.join(MyDir,'BHAWC_out_ascii_TMP.sel'))
        os.remove(os.path.join(MyDir,'BHAWC_out_ascii_TMP2.sel'))

    def test_HAWCStab2(self):
        # power file
        F=weio.read(os.path.join(MyDir,'HAWCStab2_out.pwr'))
        DF=F.toDataFrame()
        self.assertEqual(DF.values[-1,1],0.1553480512E+05)
        self.assertEqual(DF.values[-1,-1], 0.3181950053E+09)
        self.assertEqual(DF.columns[0], 'V_[m/s]')
        self.assertEqual(DF.columns[1], 'P_[kW]')


if __name__ == '__main__':
#     Test().test_000_debug()
    unittest.main()
