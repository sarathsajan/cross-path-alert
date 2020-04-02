import random
from math import radians, cos, sin, asin, sqrt  
from data import database
from flask import Flask, render_template, redirect, url_for, request
# A more formal packaging needed... with __init__.py as the development grows.

app = Flask(__name__)
app.config['SECRET_KEY'] = "cross-path-alert"

database = database()
traveldatabase = []

def distance(lat1, lat2, lon1, lon2): 
      
    lon1 = radians(lon1)       #converting radians
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
        
    dlon = lon2 - lon1         # Haversine formula 
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))  
      
    r = 6371                     #Radius of earth
        
    return(c * r)                #final output





print(distance(10.5276,10.5221,76.2144,76.2237))

#for x in database:
#	print(x['travel_history'])
