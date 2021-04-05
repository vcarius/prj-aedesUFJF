# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 06:10:14 2021

@author: viniciuscarius
"""

import requests
import numpy.random as rn
import copy

class getData(object):
    def __init__(self):
        self.__keys = ["2gLiS4J4rifPOp0KXCA2JURmWwfEYdsEvAFNdec0", "MzW39YcEPw6H4YJRpy0uSmGWgSJ2VkJSKvX05lL4"]
    
    def __get_codes(self):
        url = "https://vetores.back4app.io/classes/Vetor"
    
        payload={}
        headers = {
          'X-Parse-Application-Id': self.__keys[0],
          'X-Parse-REST-API-Key': self.__keys[1]
        }
    
        response = requests.request("GET", url, headers=headers, data=payload)
        
        codes = {}
        for i in response.json()["results"]:
            codes[i["nome"]]=i["objectId"]
        
        return codes
        
    def __init_dict(self, variables=None, Dict=None):

        for var in variables:
            Dict[var]={}
        return Dict
    
    def get_points(self):
        
        codes= self.__get_codes()
        vector_code = codes["Aedes Aegypti"]
           
        variables_ = ['N egg','A1','C','B','E','N larvae','Type','Altitude', 'Longitude', 'N pupae', 'A2', 'Latitude', 'N adults', 'D1', 'D2']
        
        url = "https://vetores.back4app.io/classes/Foco"
    
        payload={}
        headers = {
           'X-Parse-Application-Id': self.__keys[0],
          'X-Parse-REST-API-Key': self.__keys[1]
        }
    
        response = requests.request("GET", url, headers=headers, data=payload)
        
        points={}
        points = self.__init_dict(Dict=points,variables=variables_)    
        
        index=0
        for i in response.json()["results"]:
            if i["vetor"]["objectId"] == vector_code:
                points['Latitude'][index]=i["coordenadas"]["latitude"]
                points['Longitude'][index]=i["coordenadas"]["longitude"]
                points['Altitude'][index]=0.0
                points['N egg'][index]=0.0
                points['N larvae'][index]=rn.randint(low=0, high=11)
                points['N pupae'][index]=rn.randint(low=0, high=11)
                points['N adults'][index]=rn.randint(low=0, high=3)
                points['A1'][index]=rn.randint(low=0, high=2)
                points['A2'][index]=rn.randint(low=0, high=2)
                points['B'][index]=rn.randint(low=0, high=5)
                points['C'][index]=rn.randint(low=0, high=5)
                points['D1'][index]=rn.randint(low=0, high=5)
                points['D2'][index]=rn.randint(low=0, high=5)
                points['E'][index]=rn.randint(low=0, high=5)
                points['Type'][index]='O'
                
                index+=1
        
        return points
    
    def update_dict(self, Dict1=None, Dict2=None):

        Dict = copy.deepcopy(Dict2)

        size = len(Dict2['Latitude'].keys())
        
        for i, lat1, lon1 in zip(Dict1['Latitude'].keys(), Dict1['Latitude'].values(), Dict1['Longitude'].values()):
            flag=0
            for j, lat2, lon2 in zip(Dict2['Latitude'].keys(), Dict2['Latitude'].values(), Dict2['Longitude'].values()):
                if lat1 == lat2 and lon1==lon2:
                    print(lat1, lat2)
                    print(lon1, lon2)
                    Dict['Altitude'][j]=Dict1['Altitude'][i]
                    Dict['N egg'][j]=Dict1['N egg'][i]
                    Dict['N larvae'][j]=Dict1['N larvae'][i]
                    Dict['N pupae'][j]=Dict1['N pupae'][i]
                    Dict['N adults'][j]=Dict1['N adults'][i]
                    Dict['A1'][j]=Dict1['A1'][i]
                    Dict['A2'][j]=Dict1['A2'][i]
                    Dict['B'][j]=Dict1['B'][i]
                    Dict['C'][j]=Dict1['C'][i]
                    Dict['D1'][j]=Dict1['D1'][i]
                    Dict['D2'][j]=Dict1['D2'][i]
                    Dict['E'][j]=Dict1['E'][i]
                    Dict['Type'][j]=Dict1['Type'][i]
    
                    flag=1
                    break
                    
            if flag == 0:
                k = size+i
    
                Dict['Latitude'][k]=Dict1['Latitude'][i]
                Dict['Longitude'][k]=Dict1['Longitude'][i]
                Dict['Altitude'][k]=Dict1['Altitude'][i]
                Dict['N egg'][k]=Dict1['N egg'][i]
                Dict['N larvae'][k]=Dict1['N larvae'][i]
                Dict['N pupae'][k]=Dict1['N pupae'][i]
                Dict['N adults'][k]=Dict1['N adults'][i]
                Dict['A1'][k]=Dict1['A1'][i]
                Dict['A2'][k]=Dict1['A2'][i]
                Dict['B'][k]=Dict1['B'][i]
                Dict['C'][k]=Dict1['C'][i]
                Dict['D1'][k]=Dict1['D1'][i]
                Dict['D2'][k]=Dict1['D2'][i]
                Dict['E'][k]=Dict1['E'][i]
                Dict['Type'][k]=Dict1['Type'][i]
        
        return Dict