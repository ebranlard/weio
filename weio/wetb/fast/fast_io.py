'''
Created on 03/09/2015

@author: MMPE
'''
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from io import open
from builtins import map
from builtins import range
from builtins import chr
from future import standard_library
standard_library.install_aliases()
import os
import numpy as np
import struct

def load_output(filename):
    """Load a FAST binary or ascii output file

    Parameters
    ----------
    filename : str
        filename

    Returns
    -------
    data : ndarray
        data values
    info : dict
        info containing:
            - name: filename
            - description: description of dataset
            - attribute_names: list of attribute names
            - attribute_units: list of attribute units
    """

    assert os.path.isfile(filename), "File, %s, does not exists" % filename
    with open(filename, 'r') as f:
        try:
            f.readline()
        except UnicodeDecodeError:
            return load_binary_output(filename)
    return load_ascii_output(filename)

def load_ascii_output(filename):
    with open(filename) as f:
        info = {}
        info['name'] = os.path.splitext(os.path.basename(filename))[0]
        # Header is whatever is before the keyword `time`
        in_header = True
        header = []
        while in_header:
            l = f.readline()
            if not l:
                raise Exception('Error finding the end of FAST out file header. Keyword Time missing.')
            in_header= (l+' dummy').lower().split()[0] != 'time'
            if in_header:
                header.append(l)
            else:
                info['description'] = header
                info['attribute_names'] = l.split()
                info['attribute_units'] = [unit[1:-1] for unit in f.readline().split()]

        # Data, up to end of file or empty line (potential comment line at the end)
        split_lines=[]
        while True:
            l = f.readline().strip()
            if not l or len(l)==0:
                break
            split_lines.append(l.split())
        data = np.array(split_lines).astype(np.float)

        # Harcoded 8 line header and 
        #header = [f.readline() for _ in range(8)]
        #info['description'] = header[4].strip()
        #info['attribute_names'] = header[6].split()
        #info['attribute_units'] = [unit[1:-1] for unit in header[7].split()]  #removing "()"
        #data = np.array([line.split() for line in f.readlines() if len(line)]).astype(np.float)

        return data, info


def load_binary_output(filename,use_buffer=False):
    """Ported from ReadFASTbinary.m by Mads M Pedersen, DTU Wind
    Buffered version by E. Branlard, NREL
    Info about ReadFASTbinary.m:
    % Author: Bonnie Jonkman, National Renewable Energy Laboratory
    % (c) 2012, National Renewable Energy Laboratory
    %
    %  Edited for FAST v7.02.00b-bjj  22-Oct-2012
    """
    def fread(fid, n, type):
        fmt, nbytes = {'uint8': ('B', 1), 'int16':('h', 2), 'int32':('i', 4), 'float32':('f', 4), 'float64':('d', 8)}[type]
        return struct.unpack(fmt * n, fid.read(nbytes * n))

    def freadBuffered(fid, n, type):
        fmt, nbytes = {'uint8': ('B', 1), 'int16':('h', 2), 'int32':('i', 4), 'float32':('f', 4), 'float64':('d', 8)}[type]
        data = np.zeros((1,n),dtype='float32') # NOTE: loss of precision
        BufferSize=4096*40
        nBuff = int(n/BufferSize)
        try:
            nRead=0
            while nRead<n:
                nToRead = min(nPts-nRead, BufferSize)
                I = struct.unpack(fmt * nToRead, fid.read(nbytes * nToRead))
                data[0,nRead:(nRead+nToRead)] = I
                nRead=nRead+nToRead
            return data
        except:
            raise Exception('Read only %d of %d values in file:' % (nRead, n, filename, nRead, n))


    FileFmtID_WithTime = 1  #% File identifiers used in FAST
    FileFmtID_WithoutTime = 2
    LenName = 10  #;  % number of characters per channel name
    LenUnit = 10  #;  % number of characters per unit name

    with open(filename, 'rb') as fid:
        FileID = fread(fid, 1, 'int16')  #;             % FAST output file format, INT(2)

        NumOutChans = fread(fid, 1, 'int32')[0]  #;             % The number of output channels, INT(4)
        NT = fread(fid, 1, 'int32')[0]  #;             % The number of time steps, INT(4)

        if FileID == FileFmtID_WithTime:
            TimeScl = fread(fid, 1, 'float64')  #;           % The time slopes for scaling, REAL(8)
            TimeOff = fread(fid, 1, 'float64')  #;           % The time offsets for scaling, REAL(8)
        else:
            TimeOut1 = fread(fid, 1, 'float64')  #;           % The first time in the time series, REAL(8)
            TimeIncr = fread(fid, 1, 'float64')  #;           % The time increment, REAL(8)




        ColScl = fread(fid, NumOutChans, 'float32')  #; % The channel slopes for scaling, REAL(4)
        ColOff = fread(fid, NumOutChans, 'float32')  #; % The channel offsets for scaling, REAL(4)

        LenDesc = fread(fid, 1, 'int32')[0]  #;  % The number of characters in the description string, INT(4)
        DescStrASCII = fread(fid, LenDesc, 'uint8')  #;  % DescStr converted to ASCII
        DescStr = "".join(map(chr, DescStrASCII)).strip()



        ChanName = []  # initialize the ChanName cell array
        for iChan in range(NumOutChans + 1):
            ChanNameASCII = fread(fid, LenName, 'uint8')  #; % ChanName converted to numeric ASCII
            ChanName.append("".join(map(chr, ChanNameASCII)).strip())


        ChanUnit = []  # initialize the ChanUnit cell array
        for iChan in range(NumOutChans + 1):
            ChanUnitASCII = fread(fid, LenUnit, 'uint8')  #; % ChanUnit converted to numeric ASCII
            ChanUnit.append("".join(map(chr, ChanUnitASCII)).strip()[1:-1])


        #    %-------------------------
        #    % get the channel time series
        #    %-------------------------

        nPts = NT * NumOutChans  #;           % number of data points in the file


        if FileID == FileFmtID_WithTime:
            PackedTime = fread(fid, NT, 'int32')  #; % read the time data
            cnt = len(PackedTime)
            if cnt < NT:
                raise Exception('Could not read entire %s file: read %d of %d time values' % (filename, cnt, NT))

        if use_buffer:
            data = freadBuffered(fid, nPts, 'int16') #; % read the channel data
            data = data.reshape(NT, NumOutChans)
        else:
            PackedData = fread(fid, nPts, 'int16')  #; % read the channel data
            cnt = len(PackedData)
            if cnt < nPts:
                raise Exception('Could not read entire %s file: read %d of %d values' % (filename, cnt, nPts))
            data = np.array(PackedData).reshape(NT, NumOutChans)
            del PackedData

    #    %-------------------------
    #    % Scale the packed binary to real data
    #    %-------------------------
    
    if use_buffer:
        for iCol in range(NumOutChans):
            data[:,iCol] = (data[:,iCol] - ColOff[iCol]) / ColScl[iCol]
    else:
        data = (data - ColOff) / ColScl
        print(data.dtype)

    if FileID == FileFmtID_WithTime:
        time = (np.array(PackedTime) - TimeOff) / TimeScl;
    else:
        time = TimeOut1 + TimeIncr * np.arange(NT)

    # TODO, better memory management below
    data = np.concatenate([time.reshape(NT, 1), data], 1)

    info = {'name': os.path.splitext(os.path.basename(filename))[0],
            'description': DescStr,
            'attribute_names': ChanName,
            'attribute_units': ChanUnit}
    return data, info

