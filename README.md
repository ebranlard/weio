[![Build Status](https://travis-ci.org/ebranlard/weio.svg?branch=master)](https://travis-ci.org/ebranlard/weio)
<a href="https://www.buymeacoffee.com/hTpOQGl" rel="nofollow"><img alt="Donate just a small amount, buy me a coffee!" src="https://warehouse-camo.cmh1.psfhosted.org/1c939ba1227996b87bb03cf029c14821eab9ad91/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4275792532306d6525323061253230636f666665652d79656c6c6f77677265656e2e737667"></a>

# weio

Library to read and write files, in particular files used by the Wind Energy community. 
This library is for instance used by the GUI tool [pyDatView](https://github.com/ebranlard/pydatview/) to plot, export and compare these different files. 

## Typical file formats supported
- Various CSV and delimited files
- Simple Excel files
- FAST input and output files (including some turbulence files)
- HAWC2 and HawcStab2 input and output files (still some missing)
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



