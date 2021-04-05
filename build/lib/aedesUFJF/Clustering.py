# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 15:58:37 2021

@author: viniciuscarius
"""

from sklearn import cluster
from sklearn.decomposition import PCA
from aedesUFJF.Plot import plot
from random import randint
plot_ = plot()

class clustering(object):
    def __init__(self):
        
        self.data = None        
        self.labels = []
        self.n_clusters_ = []
        self.__colors = []
        self.cluster_centers_ = []        
        
    def __ColorPalett(self, n_clusters_):
    
        for i in range(n_clusters_):
            self.__colors.append('#%06X' % randint(0, 0xFFFFFF))
        
        #return self.__colors
    
    def ClusteringHotSpot(self, data=None, algorithm='Meanshift', pca=None):
    
        self.data = data.copy()
        if pca is not None:
            pca = PCA(n_components=2, copy=False)
            self.data = pca.fit_transform(data)
        
        if (algorithm=='Affinity'):
            cl = cluster.AffinityPropagation(damping=.75).fit(self.data)
            for lb in set(cl.labels_):
                self.cluster_centers_.append(self.data[cl.labels_==lb].mean(axis=0))
        
        #elif (algorithm=='Meanshift'):
        else:
            if (algorithm=='Meanshift'):
                # Estimate bandwith
                bandwidth = cluster.estimate_bandwidth(self.data, quantile=.2, n_samples=len(self.data))
                # Fit Mean Shift with Scikit
                cl = cluster.MeanShift(bandwidth = bandwidth).fit(self.data)        
                for lb in set(cl.labels_):
                    self.cluster_centers_.append(self.data[cl.labels_==lb].mean(axis=0))
        
            else:
                print("The "+algorithm+" is not implemented.")
        self.labels = cl.labels_
        self.n_clusters_ = len(set(self.labels))
        
        self.__ColorPalett(self.n_clusters_)
        
        #return self.labels, self.n_clusters_, self.colors
        
    
    def plot_shapefile(self, coords=None, title="None", output_path="./", country_bias="Brazil", pronvice_bias="SE"):
        plot_.plot_shapefile_clusters(coords=coords, vcolors=self.__colors, labels=self.labels, title=title, output_path=output_path, country_bias=country_bias, pronvice_bias=pronvice_bias)
    
    
    def plot_gmap(self, coords=None, title="None", output_path="./"):
        plot_.plot_gmap_clusters(coords=coords, vcolors=self.__colors, labels=self.labels, title=title, output_path=output_path)
