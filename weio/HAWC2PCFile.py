from .File import File
import pandas as pd

from .wetb.hawc2.pc_file import PCFile

class HAWC2PCFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.dat','.pc','.txt']

    @staticmethod
    def formatName():
        return 'HAWC2 PC file (.dat, .pc, .txt)'

    def _read(self):
        self.data = PCFile(self.filename)
        #self.data = pd.read_csv(self.filename,sep=self.sep)
        #self.data.rename(columns=lambda x: x.strip(),inplace=True)

    #def _write(self):
        #self.data.to_csv(self.filename,sep=self.false,index=False)

    def _toDataFrame(self):
        import pdb
        cols=['alpha_[deg]','Cl_[-]','Cd_[-]','Cm_[-]']

        dfs = {}
        for iset in self.data.pc_sets.keys():
            vt, vpolar = self.data.pc_sets[iset]
            for ipol in range(len(vt)):
                name='pc_set_{}_t_{}'.format(iset,vt[ipol])
                dfs[name] = pd.DataFrame(data=vpolar[ipol], columns=cols)
        return dfs

