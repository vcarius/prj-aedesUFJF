# prj-aedesUFJF

This is a developer version of the Aedes aegypti dispersion model. The proposal is to develop an algorithm that will predict the
A. aegypti dispersion based on information from weather forecast (temperature, humidity, and rainfall).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


To perform the weather forecast, it is necessary to create a key for the climatempo API.

### Prerequisites

What things you need to install the software and how to install them

First of all it is necessary to previously install the GEOS libraries (Geometry Engine, Open Source) for python.

For linux systems (ubuntu distribution):

```
apt-get install libgeos-3.3.3 libgeos-c1 libgeos-dev
```

For Windowns systems (windows 10 distribution) 32-bits with python3.7:

```
1) pip install GDAL-3.2.1-cp37-cp37m-win32.whl (https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)

2) pip install Fiona-1.8.18-cp37-cp37m-win32.whl (https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona)
```

For Windowns systems (windows 10 distribution) 64-bits with python3.7:

```
1) pip install GDAL-3.2.1-cp37-cp37m-win_amd64.whl (https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)

2) pip install Fiona-1.8.18-cp37-cp37m-win_amd64.whl (https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona)
```


### Installing

After downloading the project in zip format and unzipping it. You must do:

For linux systems (ubuntu distribution)

```
pip install prj-aedesUFJF-master

pip install git+https://github.com/matplotlib/basemap.git
```

For Windows systems (Windows 10 distribution), considering that the python3.7 version has been installed:

```
pip install prj-aedesUFJF-master/

for 32-bit systems:

pip install basemap-1.2.2-cp37-cp37m-win32.whl (https://www.lfd.uci.edu/~gohlke/pythonlibs/#basemap)

for 64-bit systems:

pip install basemap-1.2.2-cp37-cp37m-win_amd64.whl (https://www.lfd.uci.edu/~gohlke/pythonlibs/#basemap)
```

## Running the tests

Importing package modules:

In the environment python type:

```
>>> import aedesUFJF

>>> from aedesUFJF.Forecast import forecast

>>> from aedesUFJF.Plot import plot

>>> from aedesUFJF.Mosquito import mosquito

>>> from aedesUFJF.AedesPopulation import aedespopulation

```

Running the mosquito dispersion according to the weather forecast.

```
python -m aedesUFJF --data_file1 st_luzia_itanhy.csv
```

For google-map graphics, you need to create a key for the Google Maps JavaScript API.

