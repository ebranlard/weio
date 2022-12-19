from setuptools import setup, find_packages

VERSION='1.0.0'


setup(
    name='weio',
    version=VERSION,
    url='http://github.com/elmanuelito/weio/',
    author='Emmanuel Branlard',
    author_email='lastname@gmail.com',
    license='MIT',
    python_requires=">=2.7",
    description='Library to read and write files for wind energy',
    long_description="""
weio is a library to read and write files, in particular files used by the Wind Energy community. 
This library is for instance used by the GUI tool [pyDatView](https://github.com/ebranlard/pydatview/) to plot, export and compare these different files. 

##Typical file formats supported:
- Various CSV and delimited files
- Simple Excel files
- FAST input and output files (including some turbulence files)
- HAWC2 and HawcStab2 input and output files (still some missing)
- Bladed output files
- FLEX output files
- NetCDF files (partial support for 1D and 2D data for now)


##Quickstart:
Download, install dependencies, install package and run tests:
```bash
git clone https://github.com/ebranlard/weio
cd weio
python -m pip install --user -r requirements.txt  
python -m pip install -e .      # install
python -m unittest discover -v  # run test
""",
    long_description_content_type = 'text/markdown',
    packages=find_packages(include=['weio'],exclude=['./__init__.py']),
    install_requires=[
        'matplotlib',
        'future',
        'chardet',
        'openpyxl ;    python_version>"3.0"',
        'numpy>=1.16.5; python_version>"3.0"',
        'numpy        ; python_version<"3.0"',
        'pandas>=1.0.1; python_version>"3.0"',
        'pandas; python_version<="3.0"',
        'xlrd==1.2.0; python_version<"3.0"',
        'pyarrow',
        'scipy'],
    zip_safe=False,
    classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Environment :: Console',
              'Intended Audience :: Science/Research',
              'Intended Audience :: Education',
              'Intended Audience :: End Users/Desktop',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: MIT License',
              'Operating System :: MacOS :: MacOS X',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Programming Language :: Python',
              'Topic :: Scientific/Engineering',
              'Topic :: Scientific/Engineering :: Atmospheric Science',
              'Topic :: Scientific/Engineering :: Hydrology',
              'Topic :: Scientific/Engineering :: Mathematics',
              'Topic :: Scientific/Engineering :: Physics'
              ],
)
