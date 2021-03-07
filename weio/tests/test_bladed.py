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
        ## check for binary
        F = weio.read(os.path.join(MyDir,'Bladed_out_binary.$41')) 
        #F = BladedFile(os.path.join(MyDir,'Bladed_out_binary.$41'))
        DF = F.toDataFrame()
        self.assertAlmostEqual(DF['0.0m-Blade 1 Fx (Root axes) [N]'].values[0],146245.984375)

        ## check for ASCII
        F = weio.read(os.path.join(MyDir,'Bladed_out_ascii.$41'))
        DF = F.toDataFrame()
        self.assertAlmostEqual(DF['0.0m-Blade 1 Fx (Root axes) [N]'].values[0],146363.8)

    def test_Bladed_project(self):
        return # Not ready
        F = weio.read(os.path.join(MyDir,'Bladed_out_demo_a_44.$PJ')) 
        DFS = F.toDataFrame()
        DF=DFS['Misc']

        #print(DF.shape)
        #print(DF.columns[0])
        #print(DF.columns[50])
        #print(DF.columns[100])
        #print(DF.columns[191])
        self.assertEqual(DF.shape, (1200, 193))
        self.assertEqual(DF.columns[0]  , 'Time [s]')
        self.assertEqual(DF.columns[1]  , 'Time from start of simulation [s]')
        self.assertEqual(DF.columns[48] , '26.407m-DPMOM1 [Nm/m]')
        self.assertEqual(DF.columns[97], '38.75m-Blade 1 y-deflection (blade root axes) [m]')
        self.assertEqual(DF.columns[192], 'Foundation Fz [N]')
        self.assertAlmostEqual(DF['Time from start of simulation [s]'][0]    ,  7.0  ) 
        self.assertAlmostEqual(DF['26.407m-DPMOM1 [Nm/m]'][0]       , -226.85083, 5  ) 
        self.assertAlmostEqual(DF['38.75m-Blade 1 y-deflection (blade root axes) [m]'].values[0], -0.5294779, 5 ) 
        self.assertAlmostEqual(DF['Foundation Fz [N]'][0]             , -1092165.5  ) 
        

    def test_Bladed_demo(self):
        return # Not ready
        F = weio.read(os.path.join(MyDir,'Bladed_out_demo_a_44.$12')) 
        DF=F.toDataFrame()
#         print(DF.columns)
#         print(DF)
        self.assertEqual(DF.shape, (1200, 14))
        self.assertEqual(DF.columns[0]  , 'Time [s]')
        self.assertEqual(DF.columns[1]  , 'POW2 [W]')

        F = weio.read(os.path.join(MyDir,'Bladed_out_demo_a_44.$25')) 
        DF=F.toDataFrame()
#         print(DF.columns)
        self.assertEqual(DF.shape, (1200, 17))
        self.assertEqual(DF.columns[0]  , 'Time [s]')
        self.assertEqual(DF.columns[1]  , '-15.0m-MXT [Nm]')

        F = weio.read(os.path.join(MyDir,'Bladed_out_demo_a_44.$69')) 
        DF=F.toDataFrame()
#         print(DF.columns)
        self.assertEqual(DF.shape, (1200, 7))
        self.assertEqual(DF.columns[0]  , 'Time [s]')
        self.assertEqual(DF.columns[1]  , 'Foundation Mx [Nm]')


        F = weio.read(os.path.join(MyDir,'Bladed_out_demo_a_44.$37')) 
        DF=F.toDataFrame()
#         print(DF.columns)
        self.assertEqual(DF.shape, (4413, 6))
        self.assertEqual(DF.columns[0]  , 'Time [s]')
        self.assertEqual(DF.columns[1]  , 'Simulation Time [s]')

        F = weio.read(os.path.join(MyDir,'Bladed_out_demo_a_44.$55')) 
        DF=F.toDataFrame()
#         print(DF.columns)
        self.assertEqual(DF.shape, (50, 1))
        self.assertEqual(DF.columns[0]  , 'Step size histogram [N]')




if __name__ == '__main__':
     unittest.main()
#     Test().test_001_read_all()
#     Test().test_Bladed()
#     Test().test_Bladed_demo()
#     Test().test_Bladed_project()
    
