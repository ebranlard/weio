[![Build Status](https://travis-ci.org/ebranlard/weio.svg?branch=master)](https://travis-ci.org/ebranlard/weio)
<a href="https://www.buymeacoffee.com/hTpOQGl" rel="nofollow"><img alt="Donate just a small amount, buy me a coffee!" src="https://warehouse-camo.cmh1.psfhosted.org/1c939ba1227996b87bb03cf029c14821eab9ad91/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4275792532306d6525323061253230636f666665652d79656c6c6f77677265656e2e737667"></a>

# weio

Library to read and write files, in particular files used by the Wind Energy community. 
This library is for instance used by the GUI tool [pyDatView](https://github.com/ebranlard/pydatview/) to plot, export and compare these different files. 

## Typical file formats supported
- Various CSV and delimited files
- FAST input and output files
- Main HAWC2 input and output files (still some missing)
- FLEX output files
- NetCDF files (partial support for 1D and 2D data for now)

## Python package usage
```python
import weio 
f=weio.read('file.csv')
print(f.toDataFrame())
f.write('out.csv')
```
Example for an OpenFAST binary file:
```python
import weio 
df=weio.read('Output.outb').toDataFrame()
plt.plot(df['Time_[s]'], df['GenPwr_[kW']))
```


## Requirements
The library is compatible python 2.7 and python 3.
The script relies on the following python packages: `numpy`, `pandas`, `xarray`

If you have pip installed on your system, you can install them by typing in a terminal: 
```bash
pip install -r requirements.txt
```
or type `make dep` from the main directory.


## Download 
From the github page, click on the "Clone or download" button, and you may chose to download as Zip.
Alternatively, from a command line:
```bash
git clone https://github.com/ebranlard/weio
cd weio
```

## Installation
The python packages mentioned in the Requirements section need to be installed.
```bash
pip install -e .
```
or
```bash
python setup.py install
```


## Adding more file formats
File formats can be added by implementing a subclass of `weio/File.py`, for instance `weio/VTKFile.py`. Existing examples are found in the folder `weio`.
Once implemented the fileformat needs to be registered in `weio/__init__.py` by adding an import line at the beginning of this script and adding a line in the function `fileFormats()` of the form `formats.append(FileFormat(VTKFile))`



## Contributing
Any contributions to this project are welcome! If you find this project useful, you can also buy me a coffee (donate a small amount) with the link below:


<a href="https://www.buymeacoffee.com/hTpOQGl" rel="nofollow"><img alt="Donate just a small amount, buy me a coffee!" src="https://warehouse-camo.cmh1.psfhosted.org/1c939ba1227996b87bb03cf029c14821eab9ad91/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4275792532306d6525323061253230636f666665652d79656c6c6f77677265656e2e737667"></a>



