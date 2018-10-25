from .File import File, WrongFormatError
import pandas as pd

class CSVFile(File):

    @staticmethod
    def defaultExtensions():
        return ['.csv','.txt']

    @staticmethod
    def formatName():
        return 'CSV file (.csv)'

    def __init__(self, filename=None, sep=None, colNames=[], commentChar=None, commentLines=[],\
                       colNamesLine=None, **kwargs):
        self.sep          = sep
        self.colNames     = colNames
        self.commentChar  = commentChar
        self.commentLines = commentLines
        self.colNamesLine = colNamesLine
        self.data=[]
        self.header=[]
        self.nHeader=0
        if (len(self.commentLines)>0) and (self.commentChar is not None):
            raise Exception('Provide either `commentChar` or `commentLines` for CSV file types')
        if (len(self.colNames)>0) and (self.colNamesLine is not None):
            raise Exception('Provide either `colNames` or `colNamesLine` for CSV file types')
        super(CSVFile, self).__init__(filename=filename,**kwargs)

    def _read(self):
        def readline(iLine):
            with open(self.filename) as f:
                for i, line in enumerate(f):
                    if i==iLine:
                        return line.strip()
                    elif i>iLine:
                        break
        def split(s):
            if self.sep=='\s+':
                return s.strip().split()
            else:
                return s.strip().split(self.sep)
        def strIsFloat(s):
            try:
                float(s)
                return True
            except:
                return False
        # --- Safety
        if self.sep=='' or self.sep==' ':
            self.sep='\s+'

        iStartLine=0
        # --- Headers (i.e. comments)
        self.header = []
        if len(self.commentLines)>0:
            # We read the lines
            with open(self.filename) as f:
                for i in range(max(self.commentLines)+1):
                    l = f.readline()
                    if i in self.commentLines:
                        self.header.append(l.strip())
        elif self.commentChar is not None:
            # we detect the comments lines that start with comment char
            with open(self.filename) as f:
                while True:
                    l = f.readline()
                    if (not l) or (l+'_dummy')[0] != self.commentChar[0]:
                        break
                    self.header.append(l.strip())
            self.commentLines=range(len(self.header))
        iStartLine = len(self.header)

        # --- File separator 
        if self.sep is None:
            # Detecting separator by reading first lines of the file
            with open(self.filename) as f:
                dummy=[next(f).strip() for x in range(iStartLine)]
                head=[next(f).strip() for x in range(2)]
            # comma, semi columns or tab
            if head[1].find(',')>0:
                self.sep=','
            elif head[1].find(';')>0:
                self.sep=';'
            else:
                self.sep='\s+'

        # --- ColumnNames
        if self.colNamesLine is not None:
            if self.colNamesLine<0:
                # The column names are hidden somwhere in the header 
                line=readline(iStartLine+self.colNamesLine).strip()
                # Removing comment if present (should be present..)
                if self.commentChar is not None:
                    if line.find(self.commentChar)==0:
                        line=line[len(self.commentChar):].strip()
                self.colNames = split(line)
            else:
                line=readline(self.colNamesLine)
                self.colNames=split(line)
                iStartLine = max(iStartLine,self.colNamesLine+1)
        elif len(self.colNames)>0:
            pass
        else:
            # Looking at first line of data, if mainly floats -> it's not the column names
            colNames = split(readline(iStartLine))
            nFloat = sum([strIsFloat(s) for s in colNames])
            if nFloat <= len(colNames)-1:
                self.colNames=colNames
                self.colNamesLine = iStartLine
                iStartLine = max(iStartLine,self.colNamesLine+1)
            
        # --- Reading data
        #print(self)
        skiprows = range(iStartLine)
        try:
            self.data = pd.read_csv(self.filename,sep=self.sep,skiprows=skiprows,header=None)
        except pd.errors.ParserError as e:
            raise WrongFormatError('CSV File {}: '.format(self.filename)+e.args[0])

        if (len(self.colNames)==0) or (len(self.colNames)!=len(self.data.columns)):
            self.colNames=['C{}'.format(i) for i in range(len(self.data.columns))]
        self.data.columns = self.colNames;
        self.data.rename(columns=lambda x: x.strip(),inplace=True)
        #import pdb
        #pdb.set_trace()

    def _write(self):
        # --- Safety
        if self.sep=='\s+' or self.sep=='':
            self.sep='\t'
        # Write
        if len(self.header)>0:
            with open(self.filename, 'w') as f:
                f.write('\n'.join(self.header)+'\n')
            with open(self.filename, 'a') as f:
                self.data.to_csv(f,        sep=self.sep,index=False,header=False)
        else:
            self.data.to_csv(self.filename,sep=self.sep,index=False)

    def __repr__(self):
        s = 'CSVFile: {}\n'.format(self.filename)
        s += 'sep=`{}` commentChar=`{}` commentLines={} colNamesLine={} '.format(self.sep,self.commentChar,self.commentLines,self.colNamesLine)
        s += 'colNames={}'.format(self.colNames)
        s += '\n'
        if len(self.header)>0:
            s += 'header:\n'+ '\n'.join(self.header)+'\n'
        if len(self.data)>0:
            s += 'size: {}x{}'.format(len(self.data),len(self.data.columns))
        return s

    def _toDataFrame(self):
        return self.data

