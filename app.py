import random
from datetime import datetime
from math import radians, cos, sin, asin, sqrt  
from data import database
from user_data import userdetails
from flask import Flask, render_template, redirect, url_for, request
# A more formal packaging needed... with __init__.py as the development grows.

app = Flask(__name__)
app.config['SECRET_KEY'] = "cross-path-alert"

database = database()           #change this with the userdata from sql
userdata = userdetails()        #and this with patients data from sql

######################################### temporary data for testing ################################
useremail="dddddd@china.com"  #email 
####################################################################################################



######################################### DISTANCE logic ###########################################
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

######################################################################################################



##################### ITERATE THOUGH PATIENT DATABASE AND CALCULATE PROXIMITY (HEART) ################
def calc_prox(val1,ulat,ulon):
	flag1=0 
	flag2=0 
	flag3=0
	for p in database:    #might need to change for sql
		pdate=p['date']                 
		ptime=p['time']                 
		checkyear,checkmonth,checkdate=pdate.split('-')
		checkhour,checkminutes=ptime.split('-')
		val2 = datetime(int(checkyear),int(checkmonth),int(checkdate),int(checkhour),int(checkminutes),00) # if the person has no account
		#print(val2)						
		plat=p['latitude']
		plon=p['longitude']
		plat=float(plat[0:len(plat)-1])
		plon=float(plon[0:len(plon)-1])

		difference = val1-val2

		time = difference.total_seconds()/60**2      #Time in Hours
		dist = distance(ulat,plat,ulon,plon)
		#print(dist)
		#print(time)

		if dist < 0.1 and time >= -2 and time <= 2:
			flag1=1
		elif dist < 0.25 and time >= -4 and time <= 4:
			flag2=2
		elif dist < 0.5 and time >= -7 and time <= 7:
			flag3=3

	if flag1 == 1:
		return('DANGER')
		p['flag']='3' #logic not working but you have to change the flag of corresponding entry in sql 
	elif flag2 == 2:
		#change the corresponding dict flag to 2
		return('ORANGE ALERT')
	elif flag3 == 3:
		#change the corresponding dict flag to 1
		return('YELLOW ALERT')
	else :
		return('GREEN BUT DONT GO OUT')		
#####################################################################################################



################################## FUNCTION FOR NON ACCOUNT USERS ####################################
def for_user_with_no_account(useryear,usermonth,userdate,usertimehour,usertimeminutes,userlatitude,userlongtitude):
	val1 = datetime(useryear,usermonth,userdate,usertimehour,usertimeminutes,00)
	ulat=userlatitude
	ulon=userlongtitude
	print(calc_prox(val1,ulat,ulon))
######################################################################################################



################################## FUNCTION FOR ACCOUNT USERS ########################################
def for_user_with_account(useremail):

	for z in userdata:                                                    
		if z['email'] == useremail:      
			udate=z['date']                 
			utime=z['time']                 
			checkyear,checkmonth,checkdate=udate.split('-')
			checkhour,checkminutes=utime.split('-')
			val1 = datetime(int(checkyear),int(checkmonth),int(checkdate),int(checkhour),int(checkminutes),00) 
					
			#thistime = datetime.now()              # TO POP DATA LARGER THAN 28 DAYS
			#checkdiff = thistime-val1
			#check = checkdiff.total_seconds()/60**2
			#if check >= 672:
			#	userdata.pop(z)                      poping will be diff in sql
			#	print(val1)
					
			ulat=z['latitude']
			ulon=z['longitude']
			ulat=float(ulat[0:len(ulat)-1])
			ulon=float(ulon[0:len(ulon)-1])
			print(calc_prox(val1,ulat,ulon))


#####################################################################################################

for_user_with_account(useremail)		 #call for users with account

#################################################### PHASE 2 ########################################
#for_user_with_no_account(useryear,usermonth,userdate,usertimehour,usertimeminutes,userlatitude,userlongtitude) # call for users with no account


