# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 11:51:31 2021

@author: viniciuscarius
"""

from aedesUFJF.Mosquito import mosquito
import numpy as np
import random

class aedespopulation(object):
    
    def __init__(self):
        self.population = []
    
    def __PercentageEggSurvivalTemperature(self, T):
        
            if (15.0<=T<21.0):
                return 0.5966
            elif (21.0<=T<27.0):
                return 0.7895
            elif(27.0<=T<32.0): 
                return 0.8510
            elif(32.0<=T<=35.0): 
                return 0.6674
            else:
                return 0.0
            #35=T     : 61.21%
        
    def __PercentageEggSurvivalHumidity(self, H):

        if (15.0<=H<35.0):
            return 0.6284
        elif (35.0<=H<55.0):
            return 0.6822
        elif(55.0<=H<75.0): 
            return 0.7283
        elif(75.0<=H<95.0): 
            return 0.7263
        elif(95<=H):
            return 0.7741
        else:
            return 0.0
        
    def __PercentageImmatureSurvivalTemperature(self, T):

        if (15.0<=T<20.0):
            return 0.235
        elif (20.0<=T<25.0):
            return 0.90
        elif(25.0<=T<27.0): 
            return 0.88
        elif(27.0<=T<30.0): 
            return 0.93
        elif(30.0<=T<35.0): 
            return 0.88
        elif(35.0<=T<40.0): 
            return 0.67
        else:
            return 0.0
    
    def create_population(self, data=None): #data is a numpy array of list [[negg, nlarvae, npupae, nadult]]
        
        def f(point, negg, nlarvae, npupae, nadult):
            self.population.extend([mosquito(point, 1, 0, 0, 0) for _ in range(int(negg))])
            self.population.extend([mosquito(point, 0, 1, 0, 0) for _ in range(int(nlarvae))])
            self.population.extend([mosquito(point, 0, 0, 1, 0) for _ in range(int(npupae))])
            self.population.extend([mosquito(point, 0, 0, 0, 1) for _ in range(int(nadult))])


        list_p = np.where(np.sum(data, axis=1)!=0.)[0]
        
        for point in list_p:
            
            f(point, data[point][0], data[point][1], data[point][2], data[point][3])
    
    def fly(self,orig, dest, prob=0.8):
        
        individuals = np.array([i for i in range(len(self.population)) if self.population[i].adult>0 and self.population[i].point==orig])
               
        flew = [self.population[i].alter_point(dest) if random.uniform(0, 1)<prob else False for i in individuals]   
        
        return flew
        
    def reproduction(self, point, negg):
        self.population.extend([mosquito(point, 1, 0, 0, 0) for _ in range(int(negg))])
        
    def development(self, H, T):
         
        def EggHatchingPercentual(H, T):
            
            P = self.__PercentageEggSurvivalHumidity(H)*self.__PercentageEggSurvivalTemperature(T)
            
            return P
        
        ProbHatch = EggHatchingPercentual(H, T)
        
        _ = [self.population[i].alter_stage(0, 1, 0, 0) for i in range(len(self.population)) if self.population[i].egg>1 and random.uniform(0, 1)<ProbHatch]
        
        
        ProbPupation = self.__PercentageImmatureSurvivalTemperature(T) #may be we need change in future
        
        _ = [self.population[i].alter_stage(0, 0, 1, 0) for i in range(len(self.population)) if self.population[i].larvae>3 and random.uniform(0, 1)<ProbPupation]
        
        #pesquisar sobre probabilidade de pupa para adulto
        _ = [self.population[i].alter_stage(0, 0, 0, 1) for i in range(len(self.population)) if self.population[i].pupae>1]
        
        
    def indvadults(self):
        
        individuals = np.array([i if self.population[i].adult > 0 else -1 for i in range(len(self.population))])
        adults = individuals[np.where(individuals!=-1)[0]]
    
        return adults
    
    def hasadult(self):
        def x (a, b):
            try:
                a[b]+=1
            except:
                a[b]=1
        Dict={}
        
        _ = [x(Dict, self.population[i].point) for i in self.indvadults()]
        
        return Dict
        
    def adultsperpoint(self):
        
        def x1 (a, b):
            try:
                a[b]+=1
            except:
                a[b]=1
        
        def x2 (a, b):
            if b not in a.keys():
                a[b]=0
         
        Dict={}
        
        _ = [x1(Dict, self.population[i].point) if self.population[i].adult > 0 else x2(Dict, self.population[i].point) for i in range(len(self.population))]
        
        return Dict
    
    def eggperpoint(self):
        
        def x1 (a, b):
            try:
                a[b]+=1
            except:
                a[b]=1
        
        def x2 (a, b):
            if b not in a.keys():
                a[b]=0
         
        Dict={}
        
        _ = [x1(Dict, self.population[i].point) if self.population[i].egg > 0 else x2(Dict, self.population[i].point) for i in range(len(self.population))]
        
        return Dict
    
    def larvaeperpoint(self):
        
        def x1 (a, b):
            try:
                a[b]+=1
            except:
                a[b]=1
        
        def x2 (a, b):
            if b not in a.keys():
                a[b]=0
         
        Dict={}
        
        _ = [x1(Dict, self.population[i].point) if self.population[i].larvae > 0 else x2(Dict, self.population[i].point) for i in range(len(self.population))]
        
        return Dict
    
    def pupaeperpoint(self):
        
        def x1 (a, b):
            try:
                a[b]+=1
            except:
                a[b]=1
        
        def x2 (a, b):
            if b not in a.keys():
                a[b]=0
         
        Dict={}
        
        _ = [x1(Dict, self.population[i].point) if self.population[i].pupae > 0 else x2(Dict, self.population[i].point) for i in range(len(self.population))]
        
        return Dict
    
    def aging(self):
        
        for i in range(len(self.population)):
            
            if self.population[i].egg > 0:
                self.population[i].egg+=1
                
            elif self.population[i].larvae > 0:
                self.population[i].larvae+=1
                
            elif self.population[i].pupae > 0:
                self.population[i].pupae+=1
            
            else:
                self.population[i].adult+=1
            
    def death(self):
        
        #aleat = random.uniform(0, 1)
        ProbDeathAdults = np.array([0.5 * (1 - 2 * random.uniform(0, 1))+(1 - np.exp(-self.population[i].adult/42.)) if self.population[i].adult > 0 else 0 for i in range(len(self.population))])
        #ProbDeathAdults = np.array([0.4+(1 - np.exp(-self.population[i].adult/42.)) if self.population[i].adult > 0 else 0 for i in range(len(self.population))])
        to_remove = np.where(ProbDeathAdults >=0.98)[0] #this probability (0.98) can be a user parameter
        
        self.__remove(to_remove)
        
        ProbDeathLarvae = np.array([0.5 * (1 - 2 * random.uniform(0, 1))+(1 - np.exp(-self.population[i].larvae/10.)) if self.population[i].larvae > 0 else 0 for i in range(len(self.population))])
        to_remove = np.where(ProbDeathLarvae >=0.98)[0] #this probability (0.98) can be a user parameter
        
        self.__remove(to_remove)
        
        ProbDeathPupae = np.array([0.5 * (1 - 2 * random.uniform(0, 1))+(1 - np.exp(-self.population[i].pupae/10.)) if self.population[i].pupae > 0 else 0 for i in range(len(self.population))])
        to_remove = np.where(ProbDeathPupae >=0.98)[0] #this probability (0.98) can be a user parameter
        
        self.__remove(to_remove)
    
    def remove_immature(self, point):
        immature_to_remove = [ i for i in range(len(self.population)) if (self.population[i].egg > 0 or self.population[i].larvae > 0 or self.population[i].pupae > 0) and self.population[i].point == point]
        self.__remove(immature_to_remove)
    
    def remove_adult(self, point):
        adults_to_remove = [ i for i in range(len(self.population)) if self.population[i].adult > 0 and self.population[i].point == point]
        self.__remove(adults_to_remove)
        
    def __remove(self, list_r):
        objects = [self.population[i] for i in list_r]
        _ = [self.population.remove(i) for i in objects]