
from setuptools import setup, find_packages

import os
here = os.path.abspath(os.path.dirname(__file__))

import sys
if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[0:2] < (3, 2):
    raise RuntimeError("Python version 2.7 or >= 3.2 required.")

# Get the long description from the relevant file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()
lines = long_description.splitlines(True)
long_description = ''.join(lines[8:])

# Get the version from the relevant file
d = {}
execfile('fluiddyn/_version.py', d)
__version__ = d['__version__']

# Get the development status from the version string
if 'a' in __version__:
    devstatus = 'Development Status :: 3 - Alpha'
elif 'b' in __version__:
    devstatus = 'Development Status :: 4 - Beta'
else:
    devstatus = 'Development Status :: 5 - Production/Stable'

packages = find_packages(exclude=['doc'])
install_requires = ['numpy', 'matplotlib', 'scipy', 'psutil']

on_rtd = os.environ.get('READTHEDOCS')
if not on_rtd:
    install_requires += ['h5py', 'subprocess32']


setup(name='fluiddyn',
      version=__version__,
      description=('Framework for studying fluid dynamics.'),
      long_description=long_description,
      keywords='Fluid dynamics, research',
      author='Pierre Augier',
      author_email='pierre.augier@legi.cnrs.fr',
      url='https://bitbucket.org/fluiddyn/fluiddyn',
      license='CeCILL',
      classifiers=[
          # How mature is this project? Common values are
          # 3 - Alpha
          # 4 - Beta
          # 5 - Production/Stable
          devstatus,
          'Intended Audience :: Science/Research',
          'Intended Audience :: Education',
          'Topic :: Scientific/Engineering',
          'License :: OSI Approved :: BSD License',
          # Actually CeCILL-B License (BSD compatible license for French laws,
          # see http://www.cecill.info/index.en.html
          #
          # Specify the Python versions you support here. In particular,
          # ensure that you indicate whether you support Python 2,
          # Python 3 or both.
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          # 'Programming Language :: Python :: 3',
          # 'Programming Language :: Python :: 3.3',
          # 'Programming Language :: Python :: 3.4',
          'Programming Language :: Cython',
          'Programming Language :: C'],
      packages=packages,
      install_requires=install_requires,
      extras_require=dict(
          doc=['Sphinx>=1.1', 'numpydoc']))
