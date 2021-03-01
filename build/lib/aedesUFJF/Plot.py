# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 11:58:45 2021

@author: viniciuscarius
"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import gmplot
from gmplot import *
import numpy as np
import sys

APIgoogle=[]
PATH=[]
paths = ["."]
paths.extend(sys.path)

for path in paths:
    try:
        with open(path+'/aedesUFJF/keys/APIgoogle.txt', 'r') as infile:
            PATH=path            
            line = infile.readline()
            APIgoogle = line.rstrip("\n")
            
            break
    except:
         pass


class plot(object):
    def __init__(self):
        #super(plot, self).__init__
        #with open('./keys/APIgoogle.txt', 'r') as infile:
        #    line = infile.readline()            
        self.__APIgoogle = APIgoogle#line.rstrip("\n")
        self.__PATH=PATH
        
    def plot_shapefile(self, coords=None, edges=None, points=None, title="None", output_path="./", country_bias="Brazil", pronvice_bias="SE"):  
        
        try:
                
            myshp = (self.__PATH+"/aedesUFJF/shapes/ShapefileMap/"+country_bias+"/"+pronvice_bias+"/"+pronvice_bias)#('./ShapefileMap/SE_Municipios_2019')
    
        
            # create new figure, axes instances.
            fig=plt.figure(figsize=(16, 12))
            ax=fig.add_axes([0.1,0.1,0.8,0.8])
            # setup mercator map projection.
            m = Basemap(llcrnrlon= min(coords[:, 1])-0.05,\
                        llcrnrlat= min(coords[:, 0])-0.05,\
                        urcrnrlon= max(coords[:, 1])+0.05,\
                        urcrnrlat=max(coords[:, 0])+0.05,\
                        rsphere=(6378137.00,6356752.3142),\
                        resolution='h',projection='merc',                #area_thresh=.#,\
                        lat_0=np.mean(coords[:, 0]),lon_0=np.mean(coords[:, 1])
                       )
        
        
            m.readshapefile(myshp, 'Watersheds')
        
            #m.readshapefile("./ShapefileMap/loc_area_edificada_a", 'Watersheds')
            #m.readshapefile("./ShapefileMap/loc_aglomerado_rural_isolado_p", 'Watersheds')
        
            #m.drawcoastlines()
            #m.drawcountries()
            m.drawstates()
            m.drawmapboundary(fill_color= "aqua")#'#46bcec')
            m.fillcontinents(color = 'white',lake_color='#46bcec')
            #m.drawgreatcircle(0.09, 52.56, nylon,nylat, linewidth=2,color='r')
            #m.drawcoastlines()
            #m.fillcontinents()
            m.drawcountries(zorder=0, color='gray')
            #m.drawmapboundary(fill_color='aqua')
            m.drawcoastlines(linewidth=0.72, color='gray')
            
            _points = []
            if edges != None:
                for i in edges:
                    # draw great circle route between NY and London
                    m.drawgreatcircle(coords[:, 1][i[0]], coords[:, 0][i[0]], coords[:, 1][i[1]], coords[:, 0][i[1]], linewidth=1,color='black')
                    _points.extend([i[0], i[1]])
            # draw parallels
            #m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
            # draw meridians
            #m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
            ax.set_title(title)
            if points == None:
                points = _points
                
            for i in set(points):
                lons, lats = m([coords[:, 1][i]], [coords[:, 0][i]])
                m.scatter(lons, lats , marker = 'o', color='r', zorder=1.25)
            
            plt.savefig(output_path+title+".jpg")
        
        except:
             print("NOTICE: It is not possible to plot shapefile. Check country_bias and pronvince_bias arguments.")
    
    def plot_shapefile_clusters(self, coords=None, vcolors=None, labels=None, title="None", output_path="./", country_bias="Brazil", pronvice_bias="SE"):  
        
        try:
                
            myshp = (self.__PATH+"/aedesUFJF/shapes/ShapefileMap/"+country_bias+"/"+pronvice_bias+"/"+pronvice_bias)
        
            # create new figure, axes instances.
            fig=plt.figure(figsize=(16, 12))
            ax=fig.add_axes([0.1,0.1,0.8,0.8])
            # setup mercator map projection.
            m = Basemap(llcrnrlon= min(coords[:, 1])-0.05,\
                        llcrnrlat= min(coords[:, 0])-0.05,\
                        urcrnrlon= max(coords[:, 1])+0.05,\
                        urcrnrlat=max(coords[:, 0])+0.05,\
                        rsphere=(6378137.00,6356752.3142),\
                        resolution='h',projection='merc',                #area_thresh=.#,\
                        lat_0=np.mean(coords[:, 0]),lon_0=np.mean(coords[:, 1])
                       )
        
        
            m.readshapefile(myshp, 'Watersheds')
        
            #m.readshapefile("./ShapefileMap/loc_area_edificada_a", 'Watersheds')
            #m.readshapefile("./ShapefileMap/loc_aglomerado_rural_isolado_p", 'Watersheds')
        
            #m.drawcoastlines()
            #m.drawcountries()
            m.drawstates()
            m.drawmapboundary(fill_color= "aqua")#'#46bcec')
            m.fillcontinents(color = 'white',lake_color='#46bcec')
            #m.drawgreatcircle(0.09, 52.56, nylon,nylat, linewidth=2,color='r')
            #m.drawcoastlines()
            #m.fillcontinents()
            m.drawcountries(zorder=0, color='gray')
            #m.drawmapboundary(fill_color='aqua')
            m.drawcoastlines(linewidth=0.72, color='gray')
            
            ax.set_title(title)
            
            for l in set(labels):
                aux = np.where(labels == l)[0]
                for i in aux:
                    lons, lats = m([coords[:, 1][i]], [coords[:, 0][i]])
                    m.scatter(lons, lats , marker = 'o', color=vcolors[l], zorder=1.25)
            
            plt.savefig(output_path+title+".jpg")

        except:
            print("NOTICE: It is not possible to plot shapefile. Check country_bias and pronvince_bias arguments.")
        

    def plot_gmap(self, coords=None, vcolors=None, title="None", output_path="./"):
        
        try:
            gmap = gmplot.GoogleMapPlotter(coords[:,0].mean(), coords[:,1].mean(), 16.5, precision=5, apikey=self.__APIgoogle)
        
            for c in set(vcolors):
        
                aux = np.where(vcolors == c)[0]
        
                coord_hotspot=[]
        
                for i in aux:
                    coord_hotspot.append((coords[i][0], coords[i][1]))
        
                attractions_lats, attractions_lngs = zip(*coord_hotspot)
        
                gmap.scatter(attractions_lats, attractions_lngs, color=c, size=25, marker=False)
        
                # Outline the Golden Gate Park:
            coord_spots=[]
        
            for i in range(len(coords)):
                    coord_spots.append((coords[i][0], coords[i][1]))
        
            #spots = zip(*coord_spots)
            #gmap.polygon(*spots, color='cornflowerblue', edge_width=5)
        
            # Draw the map to an HTML file:
            gmap.draw(output_path+title+'.html')

        except:
            print("NOTICE: It is not possible to plot google-map. Check your Google API key.")
        
    def plot_gmap_clusters(self, coords=None, labels=None, vcolors=None, title="None", output_path="./"):
        
        try:                
            gmap = gmplot.GoogleMapPlotter(coords[:,0].mean(), coords[:,1].mean(), 16.5, precision=5, apikey=self.__APIgoogle)
        
            #reduced, labels, n_clusters_, colors = ClusteringHotSpot(data=data, algorithm=algorithm, pca=pca)
            #print ("Number of clusters is: "+str(n_clusters_))
            labels=np.array(labels)
            vcolors=np.array(vcolors)
        
            for l in set(labels):
                aux = np.where(labels == l)[0]
                coord_hotspot=[]
                for i in aux:
                    coord_hotspot.append((coords[i][0], coords[i][1]))
        
                # Mark a hidden gem:
                #gmap.marker(-21.7832, -43.3658, color='cornflowerblue')
        
                # Highlight some attractions in red:
        
                attractions_lats, attractions_lngs = zip(*coord_hotspot)
                gmap.scatter(attractions_lats, attractions_lngs, color=vcolors[l], size=25, marker=False)
        
            #spots = zip(*coord_spots)
            #gmap.polygon(*spots, color='cornflowerblue', edge_width=5)
        
            # Draw the map to an HTML file:
            gmap.draw(output_path+title+'.html')
        
        except:
            print("NOTICE: It is not possible to plot google-map. Check your Google API key.")