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

    def _toDataFrame(self):
        return self.data

# --------------------------------------------------------------------------------}
# --- Functions specific to file type  
# --------------------------------------------------------------------------------{
    def stepWind(self,WSstep=1,WSmin=3,WSmax=25,tstep=100,dt=0.5,tmin=0,tmax=999):
        """ Set the wind file to a step wind """
        Steps= np.arange(WSmin,WSmax+WSstep,WSstep)
        nCol = len(self.colNames)
        nRow = len(Steps)*2
        M = np.zeros((nRow,nCol));
        M[0,0] = tmin
        M[0,1] = WSmin
        for i,s in enumerate(Steps[:-1]):
            M[2*i+1,0] = tmin + (i+1)*tstep-dt 
            M[2*i+2,0] = tmin + (i+1)*tstep
            M[2*i+1,1] = Steps[i]
            if i<len(Steps)-1:
                M[2*i+2,1] = Steps[i+1]
            else:
                M[2*i+2,1] = Steps[-1]
        M[-1,0]= max(tmax, (len(Steps)+1)*tstep)
        M[-1,1]= WSmax
        self.data=pd.DataFrame(data=M,columns=self.colNames)
