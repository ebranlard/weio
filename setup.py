from setuptools import setup, find_packages

setup(
    name='weio',
    version='1.0',
    description='Library to read and write files',
    url='http://github.com/elmanuelito/weio/',
    author='Emmanuel Branlard',
    author_email='lastname@gmail.com',
    license='MIT',
    packages=find_packages(include=['weio'],exclude=['./__init__.py']),
    zip_safe=False
)
#     packages=['weio'],
