from .file  import File, WrongFormatError, BrokenFormatError, FileNotFoundError, EmptyFileError
from .file_formats  import FileFormat
# User defined formats
# --- TODO all these imports will likely be removed in the future to avoid loading them all at init
from .fast_input_file         import FASTInputFile
from .fast_output_file        import FASTOutputFile
from .fast_wind_file          import FASTWndFile
from .fast_linearization_file import FASTLinearizationFile
from .fast_summary_file       import FASTSummaryFile
from .csv_file                import CSVFile
from .hawc2_pc_file           import HAWC2PCFile
from .hawc2_ae_file           import HAWC2AEFile
from .hawc2_dat_file          import HAWC2DatFile
from .hawcstab2_pwr_file      import HAWCStab2PwrFile
from .hawcstab2_ind_file      import HAWCStab2IndFile
from .flex_blade_file         import FLEXBladeFile
from .flex_profile_file       import FLEXProfileFile
from .flex_out_file           import FLEXOutFile
from .flex_doc_file           import FLEXDocFile
from .flex_wavekin_file       import FLEXWaveKinFile
from .excel_file              import ExcelFile
from .turbsim_ts_file         import TurbSimTSFile
from .turbsim_file            import TurbSimFile
from .netcdf_file             import NetCDFFile
from .tdms_file               import TDMSFile
from .tecplot_file            import TecplotFile 
from .bladed_out_file         import BladedFile

class FormatNotDetectedError(Exception):
    pass

def fileFormats():
    from .vtk_file import VTKFile
    formats = []
    formats.append(FileFormat(CSVFile))
    formats.append(FileFormat(TecplotFile))
    formats.append(FileFormat(ExcelFile))
    formats.append(FileFormat(FASTInputFile))
    formats.append(FileFormat(FASTOutputFile))
    formats.append(FileFormat(FASTWndFile))
    formats.append(FileFormat(FASTLinearizationFile))
    formats.append(FileFormat(FASTSummaryFile))
    formats.append(FileFormat(TurbSimTSFile))
    formats.append(FileFormat(TurbSimFile))
    formats.append(FileFormat(HAWC2DatFile))
    formats.append(FileFormat(HAWC2PCFile))
    formats.append(FileFormat(HAWC2AEFile))
    formats.append(FileFormat(HAWCStab2PwrFile))
    formats.append(FileFormat(HAWCStab2IndFile))
    formats.append(FileFormat(FLEXBladeFile))
    formats.append(FileFormat(FLEXProfileFile))
    formats.append(FileFormat(FLEXOutFile))
    formats.append(FileFormat(FLEXWaveKinFile))
    formats.append(FileFormat(FLEXDocFile))
    formats.append(FileFormat(NetCDFFile))
    formats.append(FileFormat(VTKFile))
    formats.append(FileFormat(TDMSFile)) 
    formats.append(FileFormat(BladedFile))
    return formats


def detectFormat(filename):
    """ Detect the file formats by looping through the known list. 
        The method may simply try to open the file, if that's the case
        the read file is returned. """
    import os
    formats=fileFormats()
    ext = os.path.splitext(filename.lower())[1]
    detected = False
    i = 0 
    while not detected and i<len(formats):
        myformat = formats[i]
        if ext in myformat.extensions:
            valid, F = myformat.isValid(filename)
            if valid:
                #print('File detected as :',myformat)
                detected=True
                return myformat,F

        i += 1

    if not detected:
        raise FormatNotDetectedError('The file format could not be detected for the file: '+filename)

def read(filename,fileformat=None):
    F = None
    # Detecting format if necessary
    if fileformat is None:
        fileformat,F = detectFormat(filename)
    # Reading the file with the appropriate class if necessary
    if not isinstance(F,fileformat.constructor):
        F=fileformat.constructor(filename=filename)
    return F




