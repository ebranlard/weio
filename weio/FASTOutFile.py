from __future__ import absolute_import
from .File import File, WrongFormatError
from .CSVFile import CSVFile
import numpy as np
import pandas as pd
import struct
import os
import re

from .wetb.fast import fast_io



# --------------------------------------------------------------------------------}
# --- OUT FILE 
# --------------------------------------------------------------------------------{
class FASTOutFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.out','.outb','.elm']

    @staticmethod
    def formatName():
        return 'FAST output file (.out,.outb,.elm)'

    def _read(self):
        ext = os.path.splitext(self.filename.lower())[1]
        self.info={}
        try:
            if ext=='.out':
                self.data, self.info = fast_io.load_ascii_output(self.filename)
            elif ext=='.outb':
                self.data, self.info = fast_io.load_binary_output(self.filename)
            elif ext=='.elm':
                F=CSVFile(filename=self.filename, sep=' ', commentLines=[0,2],colNamesLine=1)
                self.data = F.data
                del F
                self.info['attribute_units']=None
                self.info['attribute_names']=self.data.columns.values
            else:
                self.data, self.info = fast_io.load_output(self.filename)
        except Exception as e:    
            raise WrongFormatError('FAST Out File {}: '.format(self.filename)+e.args[0])

        if self.info['attribute_units'] is not None:
            self.info['attribute_units'] = [re.sub('[()\[\]]','',u) for u in self.info['attribute_units']]


    #def _write(self): # TODO
    #    pass

    def _toDataFrame(self):
        if self.info['attribute_units'] is not None:
            cols=[n+'_['+u+']' for n,u in zip(self.info['attribute_names'],self.info['attribute_units'])]
        else:
            cols=self.info['attribute_names']
        return pd.DataFrame(data=self.data,columns=cols)


if __name__ == "__main__":
    B=FASTOutFile('Turbine.outb')
    print(B.data)


