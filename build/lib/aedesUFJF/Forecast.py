# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 18:30:15 2021

@author: viniciuscarius
"""

import json
import requests
#import time
import sys

city=[]
APIclimatempo = []
paths = ["."]
paths.extend(sys.path)

for path in paths:
    try:
        with open(path+'/aedesUFJF/keys/APIclimatempo.txt', 'r') as infile:
            lines = infile.readlines()
            city = lines[0].rstrip("\n")
            APIclimatempo = lines[1].rstrip("\n")
            
            break
    except:
        pass

class forecast(object):
    def __init__(self):
        self.__city = city
        self.__APIclimatempo = APIclimatempo
        
        #with open('./keys/APIopenweather.txt', 'r') as infile:
        #    line = infile.readline()
        #self.__APIopenweather = line.rstrip("\n")
            
    def getWeatherForecast(self):
        try:
                
            url = "http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/"+self.__city+"/days/15?token="+self.__APIclimatempo
            response = requests.get(url)
            forecast = json.loads(response.content)
            temperatures  = []
            precipitation = []
            humidity      = []
        
            for d in range(len(forecast['data'])):
                T = [forecast['data'][d]["temperature"][i][j] for j in ['min', 'max'] for i in ['morning', 'afternoon', 'dawn', 'night']]
                H = [forecast['data'][d]["humidity"][i][j] for j in ['min', 'max'] for i in ['morning', 'afternoon', 'dawn', 'night']]
                P = forecast['data'][d]['rain']['precipitation']
        
                temperatures.extend([sum(T)/len(T)])
                humidity.extend([sum(H)/len(H)])
                precipitation.extend([P])
                
            return temperatures, humidity, precipitation, len(forecast['data'])
        
        except:
            print("NOTICE: It is not possible to obtain weather forecast. Check your Climatempo API key.")
#    def runOpenWeather(self, latitude=None, longitude=None):
#        
#        url = "http://api.openweathermap.org/data/2.5/weather?lat="+str(latitude)+"&lon="+str(longitude)+"&appid="+self.__APIopenweather
#        time.sleep(0.01)
#        response = requests.get(url)
#        currentWheater = json.loads(response.content)
#        precipitation=None
#        
#        try:
#            precipitation=currentWheater['rain']['1h']
#        except:
#            precipitation=0.
#        
#        temperature=currentWheater['main']['temp']-273.15
#        
#        humidity=currentWheater['main']['humidity']
#        
#        return temperature, humidity, precipitation
