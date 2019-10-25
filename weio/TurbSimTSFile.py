from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from io import open
from .File import File, isBinary, WrongFormatError, BrokenFormatError
import pandas as pd
import numpy as np
from itertools import takewhile


class TurbSimTSFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.txt']

    @staticmethod
    def formatName():
        return 'TurbSim time series'

    def _read(self, *args, **kwargs):
        self.header=[]
        nHeaderMax=10
        # Reading 
        iFirstData=-1
        with open(self.filename, 'r', errors="surrogateescape") as f:
            for i, line in enumerate(f):
                if i>nHeaderMax:
                    raise BrokenFormatError('`nComp` not found in file')
                if line.lower().find('ncomp')>=0:
                    iFirstData=i
                    break
                self.header.append(line.strip())
            self.nComp   = int(line.split()[0])
            line    = f.readline().strip()
            nPoints = int(line.split()[0])
            line    = f.readline().strip()
            self.ID      = int(line.split()[0])
            f.readline()
            f.readline()
            self.Points=np.zeros((nPoints,2))
            for i in np.arange(nPoints):
                line = f.readline().strip()
                self.Points[i,:]= np.array(line.split()).astype(float)
            f.readline()
            f.readline()
            f.readline()
            lines=[]
            # reading full data
            self.data = np.array([l.strip().split() for l in takewhile(lambda x: len(x.strip())>0, f.readlines())]).astype(np.float)

    def columns(self):
        Comp=['u','v','w']
        return ['Elapsed Time ']+['Point{}{}'.format(ip+1,Comp[ic]) for ic in np.arange(self.nComp) for ip in np.arange(len(self.Points))]

    def units(self):
        nPoints = self.Points.shape[0]
        return ['(s)'] +  ['(m/s)']*nPoints*self.nComp

    def toString(self):
        s='\n'.join(self.header)+'\n'
        nPoints = self.Points.shape[0]
        s+='{} nComp - Number of velocity components in the file\n'.format(self.nComp)
        s+='{} nPoints - Number of time series points contained in this file (-)\n'.format(nPoints)
        s+='{} RefPtID - Index of the reference point (1-nPoints)\n'.format(self.ID)
        s+='Pointyi Pointzi ! nPoints listed in order of increasing height\n'
        s+=''.join([' (m) ']*2)+'\n'
        for row in self.Points:
            s+=' '.join([str(v) for v in row])+'\n'
        s+='--------Time Series-------------------------------------------------------------\n'
        s+=' '.join(self.columns())+'\n'
        s+=' '.join(self.units())+'\n'
        s+='\n'.join(''.join('{:16.8e}'.format(x) for x in y) for y in self.data)
        return s

    def _write(self):
        with open(self.filename,'w') as f:
            f.write(self.toString())

        

    def _toDataFrame(self):
        Cols = ['{}_{}'.format(c.replace(' ','_'), u.replace('(','[').replace(')',']')) for c,u in zip(self.columns(),self.units())]
        dfs={}
        dfs['Points']     = pd.DataFrame(data = self.Points,columns = ['PointYi','PointZi'])
        dfs['TimeSeries'] = pd.DataFrame(data = self.data ,columns = Cols)

        return dfs


