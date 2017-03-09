
from setuptools import setup, find_packages

import os
from runpy import run_path
import sys

here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[0:2] < (3, 3):
    raise RuntimeError('Python version 2.7 or >= 3.3 required.')

# Get the long description from the relevant file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()
lines = long_description.splitlines(True)
long_description = ''.join(lines[14:])

# Get the version from the relevant file
d = run_path('fluiddyn/_version.py')
__version__ = d['__version__']

# Get the development status from the version string
if 'a' in __version__:
    devstatus = 'Development Status :: 3 - Alpha'
elif 'b' in __version__:
    devstatus = 'Development Status :: 4 - Beta'
else:
    devstatus = 'Development Status :: 5 - Production/Stable'


install_requires = ['numpy', 'matplotlib', 'psutil', 'future']
# Even though we also use scipy, we don't require its installation
# because it can be heavy to install.

# subprocess32 should not be used on Windows and should not be
# a required dependency
if not sys.platform.startswith('win') and sys.version_info[0] < 3:
    install_requires.append('subprocess32')


setup(name='fluiddyn',
      version=__version__,
      description=('framework for studying fluid dynamics.'),
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
          # actually CeCILL-B License (BSD compatible license for French laws)
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Cython',
          'Programming Language :: C'],
      packages=find_packages(exclude=['doc']),
      install_requires=install_requires,
      extras_require=dict(
          doc=['Sphinx>=1.1', 'numpydoc']))
