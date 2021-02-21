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
        pass
        #reading_test('bladed*.*', Read_bladed_file)   
    

    def test_Bladed(self):
        F = weio.read(MyDir,'Bladed_out_binary.$41')
        DF = F.toDataFrame()
        self.assertAlmostEqual(DF['0.0m-Blade 1 Fx (Root axes)[0.0m-N]'].values[0],4.27116e+06)




if __name__ == '__main__':
    Test().test_Bladed()
    
