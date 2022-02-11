[![Build status](https://github.com/ebranlard/weio/workflows/Tests/badge.svg)](https://github.com/ebranlard/weio/actions?query=workflow%3A%22Tests%22)
<a href="https://www.buymeacoffee.com/hTpOQGl" rel="nofollow"><img alt="Donate just a small amount, buy me a coffee!" src="https://warehouse-camo.cmh1.psfhosted.org/1c939ba1227996b87bb03cf029c14821eab9ad91/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4275792532306d6525323061253230636f666665652d79656c6c6f77677265656e2e737667"></a>

# weio

Library to read and write files, in particular files used by the Wind Energy community. 
This library is for instance used by the GUI tool [pyDatView](https://github.com/ebranlard/pydatview/) to plot, export and compare these different files. 

## Typical file formats supported
- Various CSV and delimited files
- Simple Excel files
- FAST input and output files (including some turbulence files)
- HAWC2 and HawcStab2 input and output files (still some missing)
- Bladed output files
- FLEX output files
- NetCDF files (partial support for 1D and 2D data for now)


## Quickstart
Download, install dependencies, install package and run tests:
```bash
git clone https://github.com/ebranlard/weio
cd weio
python -m pip install --user -r requirements.txt  
python -m pip install -e .      # install
python -m unittest discover -v  # run test
```

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
Example to change an OpenFAST input file:
```python
import weio 
ED=weio.read('ElastoDyn.dat')
print(ED.keys())
ED['NacMass'] = 100000 # changing nacelle mass value
ED['HubMass'] = 10000  # changing hub mass value
ED.write('ElastoDyn_modified.dat')
```
Example to change an OpenFAST aerodynamic blade file :
```python
import weio
import numpy as np
Bld=weio.read('NREL5MW_AD15_blade.dat')
nSpan = 10
Spn   = np.linspace(0, 15, nSpan)       # BlSpn, radial stations [m]
CrvAC = np.zeros((nSpan,))              # BlCrvAC, prebend (usually <0) [m]
SwpAC = np.zeros((nSpan,))              # BlSwpC,  sweep                [m]
CrvAng = np.concatenate(([0], np.arctan2((CrvAC[1:]-CrvAC[:-1]),(Spn[1:]-Spn[:-1]))*180/np.pi))
Twist  = np.zeros((nSpan,)) + 1         # BlTwist [deg]
Chord  = np.zeros((nSpan,)) + 5         # BlChord [m]
AFID   = np.zeros((nSpan,)).astype(int) # BlAFID [-]
ADProp = np.column_stack((Spn,CrvAC,SwpAC,CrvAng,Twist,Chord,AFID))
Bld['NumBlNds']     = ADProp.shape[0]
Bld['BldAeroNodes'] = ADProp
Bld.write('AeroDyn_Blade_Modified.dat')
```

## Requirements
The library is compatible python 2.7 and python 3, and has limited requirements.
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
There are two ways to add a file format. If your file format is fairly generic (e.g. CSV, Excel) you can add it directly to weio (see Option 1 below). Otherwise, it is recommended to use Option 2 below. 

### Option 1: Adding a generic/wind energy file format to this repository
Additional file formats (that are either generic, or commonly used by the wind energy community) can be added as follows: 

- Copy paste the template file `weio/_NEWFILE_TEMPLATE.py`, to, for instance `weio/my_format_file.py`
- Edit this file.  Adjust the classname and the default extensions. Implement the reader (function `_read()`) and optionally the writer. Look for XXX in this file and replace them with appropriate value for your file format.
- Register the fileformat in `weio/__init__.py` by adding an import line in the function `fileFormats()`.
Registering the fileformat is useful when using `weio` with `pyDatView`, or, when using the automatic reader functionality: `weio.read('any_file.ext')` 

That's it. If possible, add some unittests and examples files:

-  Unittests are found in the folder `weio/tests/`. You can create a file `test_myformat.py` in this folder, using existing tests for inspiration. 
- Examples files can be placed in the folder `weio/tests/example_files/`. Try to use a minimal size for the example files (e.g. a couple of bytes/Kb). 
- To run your test from the repository root, type `python -m weio.tests.tests_myformat`. 

### Option 2: Adding specific/confidential file formats
Specific file formats can be added in the `<UserData>` folder of weio.
Depending on your platform, the `<UserData>` directory will be:

- `C:/Users/<USERNAME>/AppData/Roaming/weio` on Windows
- `<HOME>/.local/share/weio/` on Linux
- `<HOME>/Library/Application Support/weio/` on MacOS

To add specfic file formats, follow the following steps:

- Create the `<UserData>` directory if it doesn't exist.

- Copy paste the template file `weio/_NEWFILE_TEMPLATE.py`, to, for instance `<UserData>/my_format_file.py`. 

- Edit this file.  Adjust the classname and the default extensions. Implementing the reader (function `_read()`) and optionally the writer. Look for XXX in this file and replace them with appropriate values for your file format. NOTE: it's important to have "File" in your classname, for instance the class name could be "MyFormatFile". You can also adjust the priority level (the priority static method), which will define how early the fileformat will be tried in the list of fileformats.

The fileformats should now be available within weio. The function `weio.read` will loop through all available file formats and attempt to read a given file. You can call `weio.fileFormats` to see the list of supported fileformats and see where your newly added format is located in this list. The added class may be accessed as follows `from weio.user import MyFormatFile". 

## Contributing
Any contributions to this project are welcome! If you find this project useful, you can also buy me a coffee (donate a small amount) with the link below:


<a href="https://www.buymeacoffee.com/hTpOQGl" rel="nofollow"><img alt="Donate just a small amount, buy me a coffee!" src="https://warehouse-camo.cmh1.psfhosted.org/1c939ba1227996b87bb03cf029c14821eab9ad91/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4275792532306d6525323061253230636f666665652d79656c6c6f77677265656e2e737667"></a>



