from __future__ import division,unicode_literals,print_function,absolute_import
from builtins import map, range, chr, str
from io import open
from future import standard_library
standard_library.install_aliases()

from .File import File, WrongFormatError, BrokenFormatError
import numpy as np
import pandas as pd

# from pandas import ExcelWriter
from pandas import ExcelFile

class ExcelFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.xls','.xlsx']

    @staticmethod
    def formatName():
        return 'Excel file'

    def _read(self):
        self.data=dict()
        # Reading all sheets
        xls = pd.ExcelFile(self.filename)
        dfs = {}
        for sheet_name in xls.sheet_names:
            # Reading sheet
            df = xls.parse(sheet_name, header=None)
            # TODO detect sub tables
            # Dropping empty rows and cols
            df.dropna(how='all',axis=0,inplace=True)
            df.dropna(how='all',axis=1,inplace=True)
            print(df.shape)
            if df.shape[0]>0:
                # Setting first row as header
                df=df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True)
                #print(df)
                self.data[sheet_name]=df

    #def toString(self):
    #    s=''
    #    return s

    #def _write(self):
    #    with open(self.filename,'w') as f:
    #        f.write(self.toString)

    def __repr__(self):
        s ='Class XXXX (attributes: data)\n'
        return s


    def _toDataFrame(self):
        #cols=['Alpha_[deg]','Cl_[-]','Cd_[-]','Cm_[-]']
        #dfs[name] = pd.DataFrame(data=..., columns=cols)
        #df=pd.DataFrame(data=,columns=) 
        return self.data

