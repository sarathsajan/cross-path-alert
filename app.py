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

######################################### temporary data for testing ################################
useremail="dddddd@china.com"  #email from the login form 
password='pass'               #password from the login form 
userdate=1
useryear=2020                 #  if the user is having account first remember to add the searched travel  
usermonth=3                   #  data to his travel database and just call the function  
usertimehour=1                #  for_user_with_account by passing username and password if user has 
usertimeminutes=12            #  no account just call the function for_user_with_no_account by simply 
userlatitude=10.5279          #  passing all the values entered by the user and enjoyy
userlongtitude=76.2155
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
	for p in database:                                  #might need to change for sql                       
		for q in range (0,len(p['travel_history'])):    #might need to change for sql
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
			#print(dist)
			#print(time)

			if dist < .05 and time >= -2 and time <= 2:
				flag1=1
				break                                  #This is the extreme case so no need to check furthur
			elif dist < .1 and time >= -4 and time <= 4:
				flag2=2
			elif dist < .25 and time >= -7 and time <= 7:
				flag3=3

	if flag1 == 1:
		return('DANGER')
	elif flag2 == 2:
		return('ORANGE ALERT')
	elif flag3 == 3:
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
def for_user_with_account(useremail,password):

	for y in userdata :                                                     #might need to chane for sql
		if y['user_email'] == useremail and y['password'] == password :     #might need to chane for sql
			for z in range (0,len(y['travel_history'])):

				udate=y['travel_history'][z]['date']                 
				utime=y['travel_history'][z]['time']                 
				checkyear,checkmonth,checkdate=udate.split('-')
				checkhour,checkminutes=utime.split('-')
				val1 = datetime(int(checkyear),int(checkmonth),int(checkdate),int(checkhour),int(checkminutes),00) # if the person has no account
					
				#thistime = datetime.now()              # TO POP DATA LARGER THAN 28 DAYS
				#checkdiff = thistime-val1
				#check = checkdiff.total_seconds()/60**2
				#if check >= 672:
				#	userdata.pop(y['travel_history'][z])
				#print(val1)
					
				ulat,ulon=(y['travel_history'][z]['location']).split(',')
				ulat=float(ulat[0:len(ulat)-1])
				ulon=float(ulon[0:len(ulon)-1])
				print(calc_prox(val1,ulat,ulon))


#####################################################################################################

#for_user_with_account(useremail,password)		 #call for users with account
for_user_with_no_account(useryear,usermonth,userdate,usertimehour,usertimeminutes,userlatitude,userlongtitude) # call for users with no account

# if atleast once danger is coming, it should be flagged

