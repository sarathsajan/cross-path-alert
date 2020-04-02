import random
from datetime import datetime
from math import radians, cos, sin, asin, sqrt  
from data import database
from user_data import userdetails
from flask import Flask, render_template, redirect, url_for, request
# A more formal packaging needed... with __init__.py as the development grows.

app = Flask(__name__)
app.config['SECRET_KEY'] = "cross-path-alert"


############################################################   matching logic


database = database()
userdata = userdetails()
useremail="dddddd@china.com"  #email from the login form (useremail)
password='pass'
userdate=3
useryear=2020
usermonth=3
usertimehour=17
usertimeminutes=30 
userlatitude=10.5276
userlongtitude=76.2144
acctype='account' #or acctype='noaccount' for no acoount users


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




#print(distance(10.193910,10.306233,76.386473,76.334464))
###### HEART #######
def match(useremail,password,useryear,usermonth,userdate,usertimehour,usertimeminutes,userlatitude,userlongtitude,acctype):
	flag1=0
	for y in userdata :
		if y['user_email'] == useremail and y['password'] == password or acctype == 'noaccount':
			for z in range (0,len(y['travel_history'])):
				if acctype == 'account':
					udate=y['travel_history'][z]['date']                 
					utime=y['travel_history'][z]['time']                 
					checkyear,checkmonth,checkdate=udate.split('-')
					checkhour,checkminutes=utime.split('-')
					val1 = datetime(int(checkyear),int(checkmonth),int(checkdate),int(checkhour),int(checkminutes),00) # if the person has no account
					#print(val1)
					ulat,ulon=(y['travel_history'][z]['location']).split(',')
					ulat=float(ulat[0:len(ulat)-1])
					ulon=float(ulon[0:len(ulon)-1])

				elif acctype == 'noaccount':
					val1 = datetime(useryear,usermonth,userdate,usertimehour,usertimeminutes,00)
					ulat=userlatitude
					ulon=userlongtitude
					flag1=1
					#print(val1)
				######################### FOR USER LAT AND LONG IN DATABASE
				#print(val2)
				#print(diff.total_seconds()/60**2)
				print(ulat)
				print(ulon)

				for p in database:                              #all p is for patient
					for q in range (0,len(p['travel_history'])):
						pdate=p['travel_history'][q]['date']                 
						ptime=p['travel_history'][q]['time']                 
						checkyear,checkmonth,checkdate=pdate.split('-')
						checkhour,checkminutes=ptime.split('-')
						val2 = datetime(int(checkyear),int(checkmonth),int(checkdate),int(checkhour),int(checkminutes),00) # if the person has no account
						#print(val2)						

						plat,plon=(p['travel_history'][q]['location']).split(',')
						plat=float(plat[0:len(plat)-1])
						plon=float(plon[0:len(plon)-1])
						print(plat)
						print(plon)
						print(val1)
						print(val2)
						difference = val1-val2
						print(difference.total_seconds())
						time = difference.total_seconds()/60**2      #Time in Hours
						dist = distance(ulat,plat,ulon,plon)
						print(dist)
						print(time)
						#print(dist)
						if dist < 50 and time >= -2 and time <= 2:
							return('DANGER')
							break
						elif dist < 100 and time >= -4 and time <= 4:
							return('ORANGE ALERT')
							break
						elif dist < 250 and time >= -7 and time <= 7:
							return('BE CAREFUL')
							break
						else :
							return('YOUR SAFE BUT DONT GO OUT')	


			if flag1 == 1:                                 #to avoid itteration for noaccount users
				break


print(match(useremail,password,useryear,usermonth,userdate,usertimehour,usertimeminutes,userlatitude,userlongtitude,acctype))		 


