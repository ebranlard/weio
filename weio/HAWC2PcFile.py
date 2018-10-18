from .File import File
import pandas as pd

from .wetb.hawc2.pc_file import PCFile

class HAWC2PcFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.dat','.pc','.txt']

    @staticmethod
    def formatName():
        return 'HAWC2 Pc file (.dat, .pc, .txt)'

    def _read(self):
        self.data = PCFile(self.filename)
        #self.data = pd.read_csv(self.filename,sep=self.sep)
        #self.data.rename(columns=lambda x: x.strip(),inplace=True)

    #def _write(self):
        #self.data.to_csv(self.filename,sep=self.false,index=False)

    def _toDataFrame(self):
        import pdb
        # TODO multiData
        cols=['alpha','Cl','Cd','Cm']
        vt, vpolar = self.data.pc_sets[1]
        return pd.DataFrame(data=vpolar[0], columns=cols)

