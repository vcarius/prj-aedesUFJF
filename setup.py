# coding=UTF-8
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import os
import glob

def read(filename):
    return [req.strip() for req in open(filename).readlines()]

def readdirs(list_d):
    l = []
    for i in list_d:
        l.extend(glob.glob(i+"/*"))
    return l


here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
try:
    with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''

setup(
    # Ver PEP 426 (name)
    # Iniciar ou terminar com letra ou número
    name='prj-aedesUFJF',

    # Ver PEP 440
    # O formato pode ser assim:

    # 1.2.0.dev1  # Development release
    # 1.2.0a1     Alpha Release
    # 1.2.0b1     Beta Release
    # 1.2.0rc1    Release Candidate
    # 1.2.0       Final Release
    # 1.2.0.post1 Post Release
    # 15.10       Date based release
    # 23          Serial release

    version='0.1.0.dev1',

    
    description='This is a developer version of the Aedes aegypti dispersion model.',
    long_description=long_description,

    # A página do projeto
    #url='http://',

    # Detalhes do Autor
    author=u'Vinicius Carius de Souza',
    author_email='vinicius.carius@ice.ufjf.br',

    # Choose your license
    #license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 1 - dev1',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Education :: Testing',

        # Pick your license as you wish (should match "license" above)
        #'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='Developer version of the Aedes aegypti dispersion model.',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages= find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=False,
    #package_dir={'aedesUFJF':'aedesUFJF'},
    package_data={'aedesUFJF': readdirs(["keys", "shapes/ShapefileMap/Brazil/SE"])},
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=read("requirements.txt"),
    extras_require={"dev": read("requirements-dev.txt")},

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     'data': ['dados.json'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('aedesUFJF/keys', glob.glob(os.path.join('keys/', "*"))), ('aedesUFJF/shapes/ShapefileMap', glob.glob(os.path.join('shapes/', "ShapefileMap", "*")))],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
        # 'console_scripts': [
            # 'sample=sample:main',
        # ],
    # },
)
