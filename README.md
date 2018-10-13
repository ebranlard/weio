# weio

Library to read and write files, in particular files used by the Wind Energy community

## Python package usage
```python
import weio 
f=weio.CSVFile('file.csv')
print(f.toDataFrame())
f.write('out.csv')
```


## Requirements
The library is compatible python 2.7 and python 3.
The script relies on the following python packages: `numpy` and `pandas`

If you have pip installed on your system, you can install them by typing in a terminal: 
```bash
pip install numpy pandas
```
or type `make dep` from the main directory.


## Download 
From the github page, click on the "Clone or download" button, and you may chose to download as Zip.
Alternatively, from a command line:
```bash
git clone https://github.com/elmanuelito/weio
cd weio
```

## Installation
The python packages mentioned in the Requirements section need to be installed.
```bash
python setup.py install
```


## Adding more file formats
File formats can be added by implementing a subclass of `weio/File.py`, for instance `weio/VTKFile.py`. Existing examples are found in the folder `weio`.
Once implemented the fileformat needs to be registered in `weio/__init__.py` by adding an import line at the beginning of this script and adding a line in the function `fileFormats()` of the form `formats.append(FileFormat(VTKFile))`






