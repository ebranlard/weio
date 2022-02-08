import numpy as np
import pandas as pd
import os

from pymatreader import read_mat

try:
    from .file import File, WrongFormatError, BrokenFormatError
except:
    EmptyFileError    = type('EmptyFileError', (Exception,),{})
    WrongFormatError  = type('WrongFormatError', (Exception,),{})
    BrokenFormatError = type('BrokenFormatError', (Exception,),{})
    File=dict

class MatlabStatisticsFile(File):

    # Expected format/ structure of matlab file:
    #   filename: {runs×1 cell} chars in cell array
    # sensorname: {sensors×1 cell} chars in cell array
    #   unitname: {sensors×1 cell} chars in cell array
    #        max: [runs×sensors double] 
    #       mean: [runs×sensors double]
    #        min: [runs×sensors double]
    #        std: [runs×sensors double]
    #  where runs = number of runs/values and sensors = number of sensors for each run/value
    
    @staticmethod
    def defaultExtensions():
        return ['.mat']

    @staticmethod
    def formatName():
        return 'StatisticsSummary.mat'

    def __init__(self,filename=None,**kwargs):
        self.filename = filename
        if filename:
            self.read(**kwargs)

    def read(self, filename=None, **kwargs):
        """ read self, or read filename if provided """
        if filename:
            self.filename = filename
        if not self.filename:
            raise Exception('No filename provided')
        if not os.path.isfile(self.filename):
            raise OSError(2,'File not found:',self.filename)
        if os.stat(self.filename).st_size == 0:
            raise EmptyFileError('File is empty:',self.filename)
        # Calling children function
        self._read(**kwargs)

    def write(self, filename=None):
        """ write self, or to filename if provided """
        if filename:
            self.filename = filename
        if not self.filename:
            raise Exception('No filename provided')
        # Calling children function
        self._write()

    def _read(self):
        """ """
        self.datadict = read_mat(self.filename)

    def _write(self):
        """ """
        with open(self.filename,'w') as f:
            f.write(self.toString)

    def toDataFrame(self):

        BL_ChannelUnit = [ name+' ['+unit+']' for name,unit in zip(self.datadict['sensorname'],self.datadict['unitname'])]
        
        df_mean=pd.DataFrame(data=self.datadict['mean'],columns=BL_ChannelUnit)
        df_min=pd.DataFrame(data=self.datadict['min'],columns=BL_ChannelUnit)
        df_max=pd.DataFrame(data=self.datadict['max'],columns=BL_ChannelUnit)
        df_std=pd.DataFrame(data=self.datadict['std'],columns=BL_ChannelUnit)
        df_filename=pd.DataFrame(data=self.datadict['filename'],columns=['filename'])

        df=pd.DataFrame()
        df["filename"]=df_filename['filename'].tolist()
        for k in df_mean.keys():
            idx=int(np.argwhere(df_mean.keys()==k)[0])
            df["mean "+k]=df_mean.iloc[:,idx]
            df["min "+k]=df_min.iloc[:,idx]
            df["max "+k]=df_max.iloc[:,idx]
            df["std "+k]=df_std.iloc[:,idx]
        return df
    
    def toString(self):
        s=''
        return s

    def __repr__(self):
        s ='Class XXXX (attributes: data)\n'
        return s


