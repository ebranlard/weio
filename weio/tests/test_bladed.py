import os
import numpy as np
import re
import pandas as pd
import weio
import unittest
from helpers_for_test import MyDir, reading_test 
from weio.bladed_out_file import Read_bladed_file



class Test(unittest.TestCase):
 
    def test_001_read_all(self):
        reading_test('bladed*.*', Read_bladed_file)   
    

    def test_Bladed(self):
        F = weio.read(r'e:\Projects\Git_out\weio\weio\tests\example_files\Bladed_output_file\Steady_8ms\Steady_8ms.$PJ')
        DF = F.toDataFrame()


if __name__ == '__main__':
    Test().test_Bladed()
    
