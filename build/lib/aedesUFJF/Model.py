# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 19:29:48 2021

@author: viniciuscarius
"""

import numpy as np
import itertools as it
import random
from aedesUFJF.AedesPopulation import aedespopulation
from aedesUFJF.Plot import plot
plot_ = plot()

class aedesmodel(object):
    def __init__(self):
        #super().__init__()
         self.__aedespopulation = aedespopulation()
         self.country_bias=[]
         self.pronvice_bias=[]
         
    def create_aedespopulation(self, n_stages=None):        
        self.__aedespopulation.create_population(data=n_stages)
        
    def create_hotspot_connections(self, coords=None):
        self.coords = coords
        self.__calcVisibility()

    def define_local(self, country_bias="Brazil", pronvice_bias="SE"):
        self.country_bias=country_bias
        self.pronvice_bias = pronvice_bias
    
    def __getDistance(self, P1, P2):
        #def rad (x):
        #    return x * np.pi/180
    
        R = 6371071.0
        dLat = ((P1[0] - P2[0]) * np.pi * R)/180
        dLon = ((P1[1] - P2[1]) * np.pi * R)/180    #dLat = rad(P2[0] - P1[0])
        #dLon = rad(P2[1] - P1[1])
        #v = np.sin(dLat/2.) * np.sin(dLat/2.) + np.cos(rad(P1[0])) *  np.cos(rad(P2[0])) * np.sin(dLon/2.) * np.sin(dLon/2.)
        #c = 2 * np.arctan2(np.sqrt(v), np.sqrt(1-v))
        #d = R * c
        ret = np.power(dLat, 2) + np.power(dLon, 2); ret = np.sqrt(ret)
    
        return ret
    
    def containers_distribution(self, containers=None):        
        
        self.fitness_point = np.array([self.__calcFitness(containers[i]) for i in range(len(containers))])
    
    def __calcVisibility(self):
        
        dist = np.zeros((len(self.coords), len(self.coords)))
        for i in it.combinations(range(len(self.coords)), 2):
            dist[i[0]][i[1]] = self.__getDistance(self.coords[i[0]], self.coords[i[1]])
    
        #DM = (dist + dist.T)
        self.Visibility = (dist + dist.T)
    
        #Visibility = DM.copy()
        self.Visibility = self.Visibility* 0.001
        self.Visibility[np.where(self.Visibility >0.3)] = 1.
        self.Visibility = np.ones(self.Visibility.shape) - self.Visibility # We need to consider sparsity
    
    #def __x (a, b):
    #        a[b]=[]
    
    def __calcFitness(self, P):
        
        sum_ = sum(P)
        if sum_ == 0.:
            sum_ = 1.
        
        fitness = (P[0]*0.9 + P[1]*0.9 + P[2]*0.2 + P[3]*0.5 + P[4]*0.9 + P[5]*0.4 + P[6]*0.5)/sum_
        
        return fitness
    
    def local_weatherForecast(self, temperature=None, humidity=None, precipitation=None):
        self.temperature = temperature
        self.humidity=humidity
        self.precipitation=precipitation
    
    def run_(self, nruns=7, output_path="./"):
        
        #dispersion = {}
        #_ = [self.x(dispersion, i) for i in range(len(Visibility))]
    
        self.edges = []
            
        #verifica onde ha formas adultas
        
        whereadults = self.__aedespopulation.hasadult()
        #print(set(whereadults.keys()))
    
        plot_.plot_shapefile(coords=self.coords, edges=None, points=whereadults.keys(), title="Initial Condition", output_path=output_path, country_bias=self.country_bias, pronvice_bias=self.pronvice_bias)
    
        self.adultsperpoint = self.__aedespopulation.adultsperpoint()
    
        self.prob_risk = [(self.adultsperpoint[i] - min(self.adultsperpoint.values()))/float(max(self.adultsperpoint.values()) - min(self.adultsperpoint.values())) if i in self.adultsperpoint.keys() else 0. for i in range(len(self.coords))]
    
        #vcolors = np.array(["green" if prob_risk[i] < 0.25 else "yellow" if 0.25<= prob_risk[i] < 0.5 else "red" for i in range(len(prob_risk))])
        vcolors = np.array(["lightgray" if self.prob_risk[i]==0 else "red" for i in range(len(self.prob_risk))])
        plot_.plot_gmap(coords=self.coords, vcolors=vcolors, title="Initial Condition", output_path=output_path)
    
        for n in range(nruns):
            print("Run --> "+str(n))
            #Função de calcula numero mosquitos que saem do ponto
            # dO/dt = Ncurrent*Rate_out
    
            # dispersao aerea        
            #Voo aleatorio
            #dO = {}
    
            if len(whereadults.keys()) > 0:
                for i in whereadults.keys():
                    allowed = np.where(self.Visibility[i]>0.)[0]
                    #roulette()
                    total_weight = sum(self.Visibility[i][j] for j in allowed)
                    weight_to_target = random.uniform(0, total_weight)
                    for j in allowed:
                        weight_to_target -= self.Visibility[i][j]
                        if weight_to_target <= 0:
    
                            orig_fitness = self.fitness_point[i]
                            dest_fitness = self.fitness_point[j]
    
                            if dest_fitness > orig_fitness:
    
                                flew = self.__aedespopulation.fly(i, j, 0.8) #aplha = 0.8, it defines whether mosquitoes will fly or not.
                                if True in flew:
                                    #dO[i] = (dest, out)
                                    #dispersion[i].extend([j])
                                    self.edges.append((i, j))    #Função de atualiza número mosquitos no ponto
    
                            break
    
                # dCurrent/dt = Ncurrent + dE/dt - dO/dt
    
                #for v in dO.items():
                #    data.at[data.index[v[1][0]], 'N adults'] += v[1][1]
    
                #for v in dO.items():
                #    data.at[data.index[v[0]], 'N adults'] -= v[1][1]
    
                #reproducao mosquito
                t_fitness_point = self.fitness_point.copy()
    
                if 20.0 <= self.temperature[n] <=30.0 and self.humidity[n]>=70.0:
                    t_fitness_point = 1.5 * self.fitness_point
    
                _ = [self.__aedespopulation.reproduction(i, 200) for i in whereadults.keys() if random.random() < 0.25 and t_fitness_point[i] > 0.2]
                #_ = [population.reproduction(i, 200) for i in whereadults.keys() if random.random() < 0.25]
                #data=None: data is a numpy array [[temperature, humidity, typeofcontainer]]
    
            # desenvolvimento do mosquito
            self.__aedespopulation.development(self.humidity[n], self.temperature[n])
    
            # envelhecimento das formas
            self.__aedespopulation.aging()        
    
            # desenvolvimento do mosquito
            self.__aedespopulation.death()

            #morte por influencia humana
            if random.random() <0.2:

                point = random.choice(range(len(self.coords)))
                
                self.__aedespopulation.remove_adult(point)
                self.__aedespopulation.remove_immature(point)
            
            #verifica onde ha formas adultas
            whereadults = self.__aedespopulation.hasadult()
            
        plot_.plot_shapefile(coords=self.coords, edges=self.edges, points=whereadults.keys(), title="Day "+str(n+1), output_path=output_path, country_bias=self.country_bias, pronvice_bias=self.pronvice_bias)

        self.eggperpoint    = self.__aedespopulation.eggperpoint()
        self.larvaeperpoint = self.__aedespopulation.larvaeperpoint()
        self.pupaeperpoint  = self.__aedespopulation.pupaeperpoint()
        self.adultsperpoint = self.__aedespopulation.adultsperpoint()

        self.prob_risk = [(self.adultsperpoint[i] - min(self.adultsperpoint.values()))/float(max(self.adultsperpoint.values()) - min(self.adultsperpoint.values())) if i in self.adultsperpoint.keys() else 0. for i in range(len(self.coords))]

        #vcolors = np.array(["green" if prob_risk[i] < 0.25 else "yellow" if 0.25<= prob_risk[i] < 0.5 else "red" for i in range(len(prob_risk))])
        vcolors = np.array(["lightgray" if self.prob_risk[i]==0 else "red" for i in range(len(self.prob_risk))])

        plot_.plot_gmap(coords=self.coords, vcolors=vcolors, title="Day "+str(n+1), output_path=output_path)
    
            #print(whereadults)
            
        return self.eggperpoint, self.larvaeperpoint, self.pupaeperpoint, self.adultsperpoint, self.prob_risk, self.edges