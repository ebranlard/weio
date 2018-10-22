from .CSVFile import CSVFile
import pandas as pd

class FASTWndFile(CSVFile):

    @staticmethod
    def defaultExtensions():
        return ['.wnd']

    @staticmethod
    def formatName():
        return 'FAST determ. wind file (.wnd)'

    def __init__(self, *args, **kwargs):
        colNames=['Time','WindSpeed','WindDir','VertSpeed','HorizShear','VertShear','LinVShead','GustSpeed']
        super(FASTWndFile, self).__init__(sep=' ',commentChar='!',colNames=colNames,*args, **kwargs)

    #def _read(self):
        # Detecting separator by reading first lines of the file
        #self.header = []
        #with open(self.filename) as f:
        #    while True:
        #        l = f.readline()
        #        if (not l) or (l+'_dummy')[0] != '!':
        #            break
        #        self.header.append(l)
        #nHeader = len(self.header)
        #self.data = pd.read_csv(self.filename,sep=self.sep,skiprows=range(nHeader),names=colNames)
        ##import pdb
        ##pdb.set_trace()

    #def _write(self):
    #    self.data.to_csv(self.filename,sep=self.sep,index=False,header=self.header)

    def _toDataFrame(self):
        return self.data

