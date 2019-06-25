import unittest
import glob
import weio
import os
# MyDir=os.path.dirname(__file__)
#fileformat,F = weio.detectFormat('_tests/FASTIn_ED_bld.dat')
#F = weio.CSVFile('_tests/CSVComma_Fail.csv')
#F = weio.read('_tests/FASTIn_ED.dat')
# F = weio.read('FASTIn_SbD.dat')
# F = weio.FASTInFile(filename='FASTIn_SbD_out.dat')
F = weio.read('_tests/FASTIn_SbD.dat')
F = weio.FASTInFile('FASTIn_HD.dat')
# print(F.toString())
# F.write(F.filename.replace('.dat','_out.dat'))
#F.toDataFrame()
#print(F)
#print(fileformat)
#print(F.toDataFrame())
