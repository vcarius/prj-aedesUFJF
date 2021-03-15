# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 16:02:40 2021

@author: viniciuscarius
"""

import os
import pandas as pd
import geopandas as gpd
import json
import time
import argparse
from aedesUFJF.Model import aedesmodel
from aedesUFJF.Forecast import forecast
from aedesUFJF.Clustering import clustering
from aedesUFJF.Plot import plot

plot_ = plot()
clustering_ = clustering()

def generate_output(data=None, eggperpoint=None, larvaeperpoint=None, pupaeperpoint=None, adultsperpoint=None, prob_risk=None, edges=None, output_path="./"):
    
    def x1 (a, b, c):
        try:
            a[b].extend([c])
        except:
            a[b]=[]
            a[b].extend([c])
        
    Dict = {}

    _ = [x1(Dict, str(edges[i][0]), str(edges[i][1])) for i in range(len(edges)) if edges[i][0] != edges[i][1]]
    
    graph ={}
    graph['graph']=[]
    graph['graph'].append(Dict)
    
    with open(output_path+'graph.json', 'w') as outfile:
        json.dump(graph, outfile)
    
    for i in range(len(data)):
        
        if i in eggperpoint.keys():
            data.at[data.index[i], "N egg"]    = eggperpoint[i]
        
        if i in larvaeperpoint.keys():
            data.at[data.index[i], "N larvae"] = larvaeperpoint[i]
        
        if i in pupaeperpoint.keys():
            data.at[data.index[i], "N pupae"]  = pupaeperpoint[i]
        
        if i in adultsperpoint.keys():
            data.at[data.index[i], "N adults"] = adultsperpoint[i]
    
    data.to_csv(output_path+"Data.csv", index=False, sep=";")

def read_file(File=None):
    
    try:
        
        _DATA = pd.read_csv(File, sep=";")
        return _DATA
    
    except:
        print("The "+str(File)+" file was not found.")
        return None

def main():
    parser = argparse.ArgumentParser(description='Aedes aegypti dispersion', \
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data_file1', required=True, type=str, help='', default=None)
    parser.add_argument('--data_file2', type=str, help='', default=None)
    parser.add_argument('--clustering', type=str, help='', default="Yes")
    parser.add_argument('--algorithm', type=str, help='', default="Meanshift")
    parser.add_argument('--PCA', type=str, help='', default="Yes")
    parser.add_argument('--nruns', type=int, help='', default=7)
    parser.add_argument('--country_bias', type=str, help='', default="Brazil")
    parser.add_argument('--pronvice_bias', type=str, help='', default="SE")
    parser.add_argument('--savedir', type=str, help='', default=None)
    
    args = parser.parse_args()
    
    print(args)
    
    file1_name = args.data_file1.split('/')[-1].split('.')[0]

    if args.savedir is None or os.path.exists(args.savedir)==True:
        _ = time.localtime()
        _ = str(_[0])+str(_[1])+str(_[2])+str(_[3])+str(_[4])+str(_[5])
        args.savedir = args.data_file1.split(file1_name)[0]+_+'/'
    
    os.mkdir(args.savedir)
    
    DATA1 = read_file(args.data_file1)
        
    if (hasattr(DATA1, 'Latitude') and hasattr(DATA1, 'Longitude')) is False:
        try:
            DATA1['Latitude']=None
            DATA1['Longitude']=None
            for i in xrange(len(DATA1)):
                end = gpd.tools.geocode(DATA1['Address'].iloc[i], timeout=None, provider = "nominatim", \
                user_agent="Intro Geocode", country_bias=args.country_bias)
                coord = str(end['geometry']).split("(")[1].split(")")[0].split(" ")  
                DATA1['Latitude'].iloc[i]= float(coord[1])
                DATA1['Longitude'].iloc[i]= float(coord[0])
        except:
            print("It isn't possible obtain coordinates")
    
    DATA2 = read_file(args.data_file2)    
    
    if DATA2 is None:
        forecast_ = forecast()
        temperature, humidity, precipitation, days = forecast_.getWeatherForecast()#RunOpenWeather(latitude=coords[:,0].mean(), longitude=coords[:,1].mean())
        if args.nruns>days:
            print("WARNING: the nruns value is greater than the number of days in the weather forecast.") 
            print("The value will be set to "+str(days)+".")
            args.nruns=days
    else:
        DATA2 = DATA2[['Temperature', 'Humidity','Precipitation']].to_numpy()
        temperature, humidity, precipitation = DATA2[:, 0], DATA2[:, 1], DATA2[:, 2]
        days = len(DATA2)
        if args.nruns>days:
            print("WARNING: the nruns value is greater than the number of days in the weather forecast.") 
            print("The value will be set to "+str(days)+".")
            args.nruns=days    
    
    
    
    model = aedesmodel()
    
    n_stages = DATA1[['N egg', 'N larvae', 'N pupae', 'N adults']].to_numpy()    
    
    model.create_aedespopulation(n_stages=n_stages)
    
    coords = DATA1[["Latitude", "Longitude"]].to_numpy()
    model.create_hotspot_connections(coords=coords)
    
    containers = DATA1[['A1', 'A2','B','C','D1', 'D2','E']].to_numpy()
    model.containers_distribution(containers=containers)
    
    model.define_local(country_bias=args.country_bias, pronvice_bias=args.pronvice_bias)    
    
    model.local_weatherForecast(temperature=temperature, humidity=humidity, precipitation=precipitation) 
    
    start = time.time()
    
    eggperpoint, larvaeperpoint, pupaeperpoint, adultsperpoint, prob_risk, edges = model.run_(nruns=args.nruns, output_path=args.savedir)
    
    generate_output(data=DATA1, eggperpoint=eggperpoint, larvaeperpoint=larvaeperpoint, \
    pupaeperpoint=pupaeperpoint, adultsperpoint=adultsperpoint, prob_risk=prob_risk, \
    edges=edges, output_path=args.savedir)
    

    if args.clustering == 'Yes':
        clustering_.ClusteringHotSpot(data=containers, algorithm=args.algorithm, pca=args.PCA)
        clustering_.plot_gmap(coords=coords, title=args.algorithm+"_clustering", output_path=args.savedir)
        clustering_.plot_shapefile(coords=coords, title=args.algorithm+"_clustering", output_path=args.savedir, country_bias=args.country_bias, pronvice_bias=args.pronvice_bias)
    
    print("Time: "+str(time.time() - start))

#if __name__ == "__main__":
    
#    main()
    
#    exit()
