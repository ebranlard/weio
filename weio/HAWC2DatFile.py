from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from io import open
from builtins import map
from builtins import range
from builtins import chr
from builtins import str
from future import standard_library
standard_library.install_aliases()
import os 
import numpy as np

from .File import File, WrongFormatError, FileNotFoundError
import pandas as pd

from .wetb.hawc2.Hawc2io import ReadHawc2

class HAWC2DatFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.dat','.sel']

    @staticmethod
    def formatName():
        return 'HAWC2 dat file'

    def _read(self):
        self.bHawc=False

        try:
            res_file  = ReadHawc2(self.filename)
            self.data = res_file.ReadAll()
            self.info={}
            self.info['attribute_names'] = res_file.ChInfo[0]
            self.info['attribute_units'] = res_file.ChInfo[1]
            self.info['attribute_descr'] = res_file.ChInfo[2]
            if res_file.FileFormat=='BHAWC_ASCII':
                self.bHawc=True
        except FileNotFoundError:
            raise
            #raise WrongFormatError('HAWC2 dat File {}:  '.format(self.filename)+' File Not Found:'+e.filename)
        except Exception as e:    
#             raise e
            raise WrongFormatError('HAWC2 dat File {}: '.format(self.filename)+e.args[0])

    #def _write(self):
        #self.data.to_csv(self.filename,sep=self.false,index=False)

    def _toDataFrame(self):
        if self.info['attribute_units'] is not None:
            units = [u.replace('(','').replace(')','').replace('[','').replace(']','') for u in self.info['attribute_units']]
            cols=[n+'_['+u+']' for n,u in zip(self.info['attribute_names'],units)]
        else:
            cols=self.info['attribute_names']
        return pd.DataFrame(data=self.data,columns=cols)
#
    def _write(self):
        if self.bHawc:
#         if len(self.header)>0:
            filename=self.filename
            ext = os.path.splitext(filename)[-1].lower()
            if ext=='.dat':
                datfilename=filename
            elif ext=='.sel':
                datfilename=filename.replace(ext,'.dat')
            else:
                datfilename=filename+'.dat'
            selfilename=datfilename[:-4]+'.sel'
            nScans=self.data.shape[0]
            nChannels=self.data.shape[1]
            SimTime=self.data[-1,0]-self.data[0,0]
            # --- dat file
            np.savetxt(datfilename, self.data, fmt='%16.8e')
            # --- Sel file
            with open(selfilename, 'w') as f:
                f.write(
"""BHawC channel reference file (sel):
+===================== (Name) =================== (Time stamp) ========= (Path) ==========================================================+
Original BHAWC file    : NA.dat                    2001.01.01  00:00:00  C:\\
Channel reference file : NA.sel                    2001.01.01  00:00:00  C:\\
Result file            : NA.dat                    2001.01.01  00:00:00  C:\\
+=========================================================================================================================================+
Scans             \tChannels                      \tTime [sec]                \tCoordinate convention: Siemens
""")
                f.write('{:19s}\t{:25s}\t{:25s}\n\n'.format(str(nScans),str(nChannels),'{:.3f}'.format(SimTime)))
                f.write('{:19s}\t{:25s}\t{:25s}\t{:25s}\n'.format('Channel','Variable descriptions','Labels','Units'))
                for chan,(label,descr,unit) in enumerate(zip(self.info['attribute_names'],self.info['attribute_descr'],self.info['attribute_units'])):
                    f.write('{:19s}\t{:25s}\t{:25s}\t{:25s}\n'.format(str(chan+1),descr[0:26],label[0:26],'['+unit+']'))


#    1  Time                                                                                     t                     [s]

# #                 f.write('\n'.join(self.header)+'\n')
# #             with open(self.filename, 'a') as f:
# #                 self.data.to_csv(f,        sep=self.sep,index=False,header=False)
# 
#             print(self.info)
