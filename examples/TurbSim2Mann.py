""" 
Converts a turbsim file to a mann box

"""
from weio.turbsim_file import TurbSimFile
from weio.mannbox_file import MannBoxFile

# --- Read turbsim file
ts_filename='test.bts'
ts=TurbSimFile(ts_filename)
print(ts)

# --- Convert to Hawc2 format
mn = MannBoxFile()
mn.fromTurbSim(ts['u'],0)
mn.write(ts_filename.replace('.bts','.u'))
mn.fromTurbSim(ts['u'],1)
mn.write(ts_filename.replace('.bts','.v'))
mn.fromTurbSim(ts['u'],2)
mn.write(ts_filename.replace('.bts','.w'))

print(mn)

