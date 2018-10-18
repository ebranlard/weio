from .File import File
from .FileFormats import FileFormat
# User defined formats
from .FASTInFile import FASTInFile
from .FASTOutFile import FASTOutFile
from .CSVFile import CSVFile
from .HAWC2PcFile import HAWC2PcFile
import os

def fileFormats():
    formats = []
    formats.append(FileFormat(FASTInFile))
    formats.append(FileFormat(FASTOutFile))
    formats.append(FileFormat(HAWC2PcFile))
    formats.append(FileFormat(CSVFile))
    return formats


def detectFormat(filename):
    formats=fileFormats()
    ext = os.path.splitext(filename.lower())[1]
    detected = False
    i = 0 
    while not detected and i<len(formats):
        myformat = formats[i]
        if ext in myformat.extensions:
            if myformat.isValid(filename):
                detected=True
                #print('File detected as :',myformat)
                return myformat

        i += 1

    if not detected:
        raise Exception('The file was not detected by detectFormat():'+filename)

def read(filename,fileformat=None):
    if fileformat is None:
        fileformat = detectFormat(filename)
    # Reading the file with the appropriate class
    return fileformat.constructor(filename)
