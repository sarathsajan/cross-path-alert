import random
from datetime import datetime
from math import radians, cos, sin, asin, sqrt  
from data import database
from user_data import userdetails
from flask import Flask, render_template, redirect, url_for, request
# A more formal packaging needed... with __init__.py as the development grows.

app = Flask(__name__)
app.config['SECRET_KEY'] = "cross-path-alert"
database = database()
userdata = userdetails()

################################ DISTANCE logic ################################

useremail="dddddd@china.com"  #email from the login form (useremail) (char)
password='pass'               #(char)
userdate=0
useryear=0                    #if the user is having account first remember to add the  travel data to his 
usermonth=0                   #travel database and just call the function by passing username, password and
usertimehour=0                #accounttype='account' and rest all can be 0
usertimeminutes=0             #if user has no account just call the function by simply passing all the 
userlatitude=0                #values enteres by the user and enjoyy
userlongtitude=0
acctype='account' #or acctype='noaccount' for no acoount users (char)


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

##########################################################################################


############################################### HEART #####################################
def match(useremail,password,useryear,usermonth,userdate,usertimehour,usertimeminutes,userlatitude,userlongtitude,acctype):
	flag=0
	for y in userdata :
		if y['user_email'] == useremail and y['password'] == password or acctype == 'noaccount':
			for z in range (0,len(y['travel_history'])):
				flag1=0 
				flag2=0 
				flag3=0 
				flag4=0
				if acctype == 'account':
					udate=y['travel_history'][z]['date']                 
					utime=y['travel_history'][z]['time']                 
					checkyear,checkmonth,checkdate=udate.split('-')
					checkhour,checkminutes=utime.split('-')
					val1 = datetime(int(checkyear),int(checkmonth),int(checkdate),int(checkhour),int(checkminutes),00) # if the person has no account
					
					#thistime = datetime.now()              # TO POP DATA LARGER THAN 14 DAYS
					#checkdiff = thistime-val1
					#check = checkdiff.total_seconds()/60**2
					#if check >= 336:
					#	userdata.pop(y['travel_history'][z])
					#print(val1)
					
					ulat,ulon=(y['travel_history'][z]['location']).split(',')
					ulat=float(ulat[0:len(ulat)-1])
					ulon=float(ulon[0:len(ulon)-1])

				elif acctype == 'noaccount':
					val1 = datetime(useryear,usermonth,userdate,usertimehour,usertimeminutes,00)
					ulat=userlatitude
					ulon=userlongtitude
					flag=1
					#print(val1)
				######################### FOR USER LAT AND LONG IN DATABASE

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

						difference = val1-val2

						time = difference.total_seconds()/60**2      #Time in Hours
						dist = distance(ulat,plat,ulon,plon)

						if dist < 50 and time >= -2 and time <= 2:
							flag1=1
							print(dist)
							print(time)
							break
						elif dist < 100 and time >= -4 and time <= 4:
							flag2=2
							break
						elif dist < 250 and time >= -7 and time <= 7:
							flag3=3
							break
						else :
							flag4=4
				if flag1 == 1:
					return('DANGER')
				elif flag2 == 2:
					return('ORANGE ALERT')
				elif flag3 == 3:
					return('YELLOW ALERT')
				elif flag4 == 4:
					return('GREEN BUT DONT GO OUT')				


			if flag == 1:                                 #To avoid itteration for noaccount users
				break
##################################################################################


print(match(useremail,password,useryear,usermonth,userdate,usertimehour,usertimeminutes,userlatitude,userlongtitude,acctype))		 


