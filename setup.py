#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This work is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License. To view a
# copy of this license, visit
# http://creativecommons.org/licenses/by-nc-sa/4.0/.
# -----------------------------------------------------------------------------

__version__ = '0.0.0-dev'

from setuptools import find_packages, setup

classes = """
    Development Status :: 1 - Planning
    Framework :: IPython
    Intended Audience :: Developers
    Intended Audience :: Education
    Intended Audience :: Science/Research
    Natural Language :: English
    Operating System :: MacOS :: MacOS X
    Operating System :: POSIX
    Operating System :: Unix
    Programming Language :: Python
    Programming Language :: Python :: 2.7
    Topic :: Scientific/Engineering
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

description = ("INFO-H-500 / INFO-H-501: "
               "Interactive lessions in image processing.")

setup(name='An-Introduction-To-Image-Processing',
      version=__version__,
      license='CC BY-NC-SA 4.0',
      description=description,
      long_description=description,
      author='Olivier Debeir',
      author_email='odebeir@ulb.ac.be',
      maintainer='Olivier Debeir',
      maintainer_email='odebeir@ulb.ac.be',
      url='http://lisa.ulb.ac.be/image/index.php/INFO-H-500',
      packages=find_packages(),
      install_requires=['scikit-image == 0.10.0', 'ipython[all]', 'runipy',
                        'future<=0.13.1'],
      classifiers=classifiers)
