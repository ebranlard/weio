""" 
Input/output class for the fileformat XXX
"""
import numpy as np
import pandas as pd
import os

try:
    from .file import File, WrongFormatError, BrokenFormatError
except:
    File=dict
    EmptyFileError    = type('EmptyFileError', (Exception,),{})
    WrongFormatError  = type('WrongFormatError', (Exception,),{})
    BrokenFormatError = type('BrokenFormatError', (Exception,),{})

class XXXFile(File):
    """ 
    Read/write a XXX file. The object behaves as a dictionary.
    
    Main methods
    ------------
    - read, write, toDataFrame, keys
    
    Examples
    --------
        f = XXXXFile('file.xxx')
        print(f.keys())
        print(f.toDataFrame().columns)  
    
    """

    @staticmethod
    def defaultExtensions():
        """ List of file extensions expected for this fileformat"""
        return ['.XXX']

    @staticmethod
    def formatName():
        """ Short string (~100 char) identifying the file format"""
        return 'XXX file'

    @staticmethod
    def priority(): return 60 # Priority in weio.read fileformat list between 0=high and 100:low


    def __init__(self, filename=None, **kwargs):
        """ Class constructor. If a `filename` is given, the file is read. """
        self.filename = filename
        if filename:
            self.read(**kwargs)

    def read(self, filename=None, **kwargs):
        """ Reads the file self.filename, or `filename` if provided """
        
        # --- Standard tests and exceptions (generic code)
        if filename:
            self.filename = filename
        if not self.filename:
            raise Exception('No filename provided')
        if not os.path.isfile(self.filename):
            raise OSError(2,'File not found:',self.filename)
        if os.stat(self.filename).st_size == 0:
            raise EmptyFileError('File is empty:',self.filename)
        # --- Calling (children) function to read
        self._read(**kwargs)

    def write(self, filename=None):
        """ Rewrite object to file, or write object to `filename` if provided """
        if filename:
            self.filename = filename
        if not self.filename:
            raise Exception('No filename provided')
        # Calling (children) function to write
        self._write()

    def _read(self, streaming=False, **kwargs):
        """
        Reads self.filename and stores data into self. Self is (or behaves like) a dictionary

        Parameters
        ----------
        streaming : bool
            If True, read only headers and keep file open for later reading.
            Requires context manager. Default: False (read entire file)
        """
        # --- Example (normal mode - read everything):
        #self['data']=[]
        #with open(self.filename, 'r', errors="surrogateescape") as f:
        #    for i, line in enumerate(f):
        #        self['data'].append(line)

        # --- Example (with streaming support):
        # if streaming:
        #     # Read headers only, keep file open
        #     self._fid = open(self.filename, 'r', errors="surrogateescape")
        #     # Read header lines
        #     self['header_line'] = self._fid.readline()
        #     # Parse header info
        #     self['attribute_names'] = self['header_line'].split()
        #     # File is now positioned at start of data
        # else:
        #     # Normal mode: read entire file
        #     self['data']=[]
        #     with open(self.filename, 'r', errors="surrogateescape") as f:
        #         f.readline()  # skip header
        #         for i, line in enumerate(f):
        #             self['data'].append(line)
        raise NotImplementedError()

    def _readAll(self):
        """
        Read all remaining data after header in streaming mode.
        Only called when streaming=True and readAll() is invoked.
        """
        # --- Example:
        # if self._fid is None:
        #     raise RuntimeError("No open file handle")
        #
        # # Read all remaining lines from current position
        # self['data'] = []
        # for line in self._fid:
        #     self['data'].append(line.strip())
        raise NotImplementedError(f"{self.__class__.__name__} does not support readAll()")

    def _readChunk(self, **kwargs):
        """
        Read a chunk of data from current position in streaming mode.
        Only called when streaming=True and readChunk() is invoked.

        Parameters
        ----------
        **kwargs : dict
            Format-specific parameters (e.g., nlines=1000, nrows=100, nbytes=1024)
            Different file formats can implement different chunking strategies.

        Returns
        -------
        chunk : data
            The chunk of data read, or None if end of file
        """
        # --- Example:
        # if self._fid is None:
        #     raise RuntimeError("No open file handle")
        #
        # nlines = kwargs.get('nlines', 1000)  # default chunk size
        #
        # chunk = []
        # for i in range(nlines):
        #     line = self._fid.readline()
        #     if not line:
        #         return None if not chunk else chunk
        #     chunk.append(line.strip())
        # return chunk
        raise NotImplementedError(f"{self.__class__.__name__} does not support readChunk()")

    def _write(self):
        """ Writes to self.filename"""
        # --- Example:
        #with open(self.filename,'w') as f:
        #    f.write(self.toString)
        raise NotImplementedError()

    def toDataFrame(self):
        """ Returns object into one DataFrame, or a dictionary of DataFrames"""
        # --- Example (returning one DataFrame):
        #  return pd.DataFrame(data=np.zeros((10,2)),columns=['Col1','Col2'])
        # --- Example (returning dict of DataFrames):
        #dfs={}
        #cols=['Alpha_[deg]','Cl_[-]','Cd_[-]','Cm_[-]']
        #dfs['Polar1'] = pd.DataFrame(data=..., columns=cols)
        #dfs['Polar1'] = pd.DataFrame(data=..., columns=cols)
        # return dfs
        raise NotImplementedError()

    # --- Optional functions
    def __repr__(self):
        """ String that is written to screen when the user calls `print()` on the object. 
        Provide short and relevant information to save time for the user. 
        """
        s='<{} object>:\n'.format(type(self).__name__)
        s+='|Main attributes:\n'
        s+='| - filename: {}\n'.format(self.filename)
        # --- Example printing some relevant information for user
        #s+='|Main keys:\n'
        #s+='| - ID: {}\n'.format(self['ID'])
        #s+='| - data : shape {}\n'.format(self['data'].shape)
        s+='|Main methods:\n'
        s+='| - read, write, toDataFrame, keys'
        return s
    
    def toString(self):
        """ """
        s=''
        return s



