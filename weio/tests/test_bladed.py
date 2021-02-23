import os
import numpy as np
import re
import pandas as pd
import weio
import unittest
try:
    from .helpers_for_test import MyDir, reading_test 
except ImportError:
    from helpers_for_test import MyDir, reading_test 

from weio.bladed_out_file import BladedFile



class Test(unittest.TestCase):
 
    def test_001_read_all(self):
        reading_test('Bladed_out*.*', BladedFile)   
    

    def test_Bladed(self):
        F = weio.read(os.path.join(MyDir,'Bladed_out_binary.$41')) 
        #F = BladedFile(os.path.join(MyDir,'Bladed_out_binary.$41'))
        DF = F.toDataFrame()
        self.assertAlmostEqual(DF['0.0m-Blade 1 Fx (Root axes)[0.0m-N]'].values[0],146245.984375)

        F = weio.read(os.path.join(MyDir,'Bladed_out_ascii.$41'))
        # TODO TODO check that ascii works fine




if __name__ == '__main__':
    Test().test_Bladed()
    
