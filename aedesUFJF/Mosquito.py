# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 11:49:53 2021

@author: viniciuscarius
"""

class mosquito (object):
    def __init__(self, point, egg, larvae, pupae, adult):
        self.point=point
        self.egg=egg                                  
        self.larvae=larvae           
        self.pupae=pupae
        self.adult=adult
    
    def alter_stage(self, egg, larvae, pupae, adult):
        self.egg=egg
        self.larvae=larvae
        self.pupae=pupae
        self.adult=adult
        
        return True
    
    def alter_point(self, point):
        self.point=point
        
        return True