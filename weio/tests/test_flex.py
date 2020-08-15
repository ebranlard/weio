import unittest
import os
import numpy as np
from .helpers_for_test import MyDir, reading_test 
import weio

class Test(unittest.TestCase):
 
    def test_001_read_all(self, DEBUG=True):
        reading_test('FLEX*.*', weio.read)

    def DF(self,FN):
        """ Reads a file with weio and return a dataframe """ 
        return weio.read(os.path.join(MyDir,FN)).toDataFrame()

    def test_FLEX(self):
        self.assertAlmostEqual(self.DF('FLEXProfile.pro')['pc_set_2_t_57.0'].values[2,2],0.22711022)
        Bld=self.DF('FLEXBlade002.bld')
        self.assertAlmostEqual(Bld['r_[m]'].values[-1],61.5)
        self.assertAlmostEqual(Bld['Mass_[kg/m]'].values[-1],10.9)
        self.assertAlmostEqual(Bld['Chord_[m]'].values[3],3.979815059)
