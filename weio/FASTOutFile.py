from __future__ import absolute_import
from .File import File
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
        return ['.out','.outb']

    @staticmethod
    def formatName():
        return 'FAST output file (.out,.outb)'

    def _read(self):
        ext = os.path.splitext(self.filename.lower())[1]
        if ext=='.out':
            self.data, self.info = fast_io.load_ascii_output(self.filename)
        elif ext=='.outb':
            self.data, self.info = fast_io.load_binary_output(self.filename)
        else:
            self.data, self.info = fast_io.load_output(self.filename)

        self.info['attribute_units'] = [re.sub('[()\[\]]','',u) for u in self.info['attribute_units']]


    #def _write(self): # TODO
    #    pass

    def _toDataFrame(self):
        cols=[n+'_['+u+']' for n,u in zip(self.info['attribute_names'],self.info['attribute_units'])]
        return pd.DataFrame(data=self.data,columns=cols)


if __name__ == "__main__":
    B=FASTOutFile('Turbine.outb')
    print(B.data)



