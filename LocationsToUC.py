#Andrew Amavizca ME-021
#Project 1        2019
#Iterates through provided text file and converts lattitude and longitude cordinates
#into distances and aranges them by their temperatures in summer and winter. 
#The code then sorts them top five closest to Uc merced. 

import math as m
import os


##FUNCTIONS AND CONVERSIONS#
############################

#This is the haversine formula for distance

def formula(lat2,lon2,lat1,lon1):
    begining = 2*6360 #2R
    deltaLat = (lat2 - lat1)/2
    deltaLon = (lon2 - lon1)/2
    a = m.sin(deltaLat)**2
    b = m.cos(lat1)*m.cos(lat2)
    c = m.sin(deltaLon)**2
    d = a + b*c
    e = m.sqrt(d)
    dist = begining*(m.asin(e))
    dist = dist
    return dist

#converts DMS to a tuple where the first element is in radians
#The second element is in degrees.

def dmsConvert(D,M,direction):
    degrees = D + (M/60)  
    rads = m.radians(degrees)*direction
    return rads, degrees



######### INPUT DATA ##########
###############################

#Taking in our user inputs

user_file = input('\nWhat file do you want to work with? ')

user_file_check = os.path.isfile(user_file)

#checks if the file the user inputs exists
#terminates code if it does not
if user_file_check == False:
    print('File not found!')
    quit()

season = input('\nWhen are you planning to take your holiday? summer or winter: ')
Temp = input('\nWould you like to go to a cold or warm destination? ' )

#ensures no capitalization errors occur

season = season.lower().capitalize() 
Temp = Temp.lower().capitalize() 

#home coorinates lon is negative because its east

homelat_rad = dmsConvert(37,22,1)[0]
homelon_rad = dmsConvert(120,42,-1)[0]

#empty list to fill later with places that match criteria

cities = []






####### ERROR HANDELING ########
################################

#creating error message blanks

error_message1 = ''
error_message2 = ''

#Handling any errors: if user inputs something odd the validation is set to 0.
#This ensures that the main portion of the program will not run.

if season == "Summer":
    validation1 = 1
elif season == "Winter":
    validation1 = 1
else:
    validation1 = 0
    error_message1 = ('Invalid Entry: "{}", please enter summer or winter.'.format(season))
     
if Temp == "Warm":
    validation2 = 1
elif Temp == "Cold":
    validation2 = 1
else:
    validation2 = 0
    error_message2 = ('Invalid Entry: "{}", please enter warm or cold.'.format(Temp))




####### Main Portion  ##########
################################


#Simply opening our text file and reading it

f = open(user_file, 'r')


#This skips the header line to avoid any issues with index ranges

next(f)

#if we did not enounter ANY errors in the input before, our validation will be = 1
#which will run this portion of the code.


if validation1 == 1 and validation2 == 1:

    for lines in f:                             

        #for the current line in the file the empty spaces are stripped.
        #And the lines are split into lists according to their coloumns. 
        
        city_info = lines.strip().split('\t')   
        
        #The name of the city,state,country are elements in city_info
        #and are ordered respectively after lat and lon.

        city = city_info[2]
        state_provice = city_info[3]
        country = city_info[4]

        #This takes the first element in city_info which in this case lattitude.
        #I replace North with 1 as it is positive with repect to the equator, and South with -1.
        #Then i replace the degree symbol with a space and split the Degrees from the minutes along
        #with the direction of its position being -1, or 1.

        latDMS = city_info[0].replace('N', ' 1').replace('S', ' -1').replace('°',' ').split() #output: ex ['20','10','-1'] DM(north or south)
        latDeg = int(latDMS[0])
        latMin = int(latDMS[1])
        latDirection = int(latDMS[2])
        
        # Simillarly as with the lattitude, the longitude respectfully.
        lonDMS = city_info[1].replace('E', ' 1').replace('W', ' -1').replace('°',' ').split()
        lonDeg = int(lonDMS[0])
        lonMin = int(lonDMS[1])
        lonDirection = int(lonDMS[2])

        #since our function dmsConvert can have 2 outputs in RAD or DEG
        #I choose to leave these two as tuples of the dmsConvert output
        latRad = dmsConvert(latDeg,latMin,latDirection)
        lonRad = dmsConvert(lonDeg,lonMin,lonDirection)

        #here: Using the haversine formula with 'latRad', and 'lonRad' using the RAD output
        distance = formula(latRad[0],lonRad[0],homelat_rad,homelon_rad)

        
        #This is used to determine the temp 
        #in summer or winter according to the lat
        #the variables tempsummer and tempWinter get stored
        #accordingly

        if latRad[1] > 66:
            tempSummer = 'Cold'
            tempWinter = 'Cold'
        elif latRad[1] < 66 and latRad[1] > 35:
            tempSummer = 'Warm'
            tempWinter = 'Cold'
        elif latRad[1] < 35 and latRad[1] > -35:
            tempSummer = 'Warm'
            tempWinter = 'Warm'
        elif latRad[1] < -35 and latRad[1] > -66:
            tempSummer = 'Cold'
            tempWinter = 'Warm'
        elif latRad[1] < -66:
            tempSummer = 'Cold'
            tempWinter = 'Cold'

        #once all the data is computed, it is placed in  a list of two elements
        #[float, dictionary]

        place = [distance,{
                'city': city, 
                'state': state_provice,
                'country':country,
                'Summer': tempSummer,
                'Winter': tempWinter
                }]
        
        #referencing the 2nd element in the list place which is a dictionary.
        #if the key referencing the users input ex('Summer') is equal to the 
        #temp the user selected ex('Cold') the list 'place' is appended to the list 'cities'.
    
        if place[1][season] == Temp:
            cities.append(place)
    
        #now that we have all locations in our list 'cities' that suit the users criteria for the vacation.
        #we can sort least to greatest in terms of distance. because the elements are made of lists [float, dictionary].
        #so cities is sorted by the magnitude of the float.
    
        cities = sorted(cities)

        #This is simply just formating to make the output look more organized.
    
        output1 = '\nThe top 5 closest travel desinations to UC Merced that are {} in the {}:'.format(Temp,season)
        output2 = '********************************************************************************\n'
    
    f.close()
    
    print(output1)
    print(output2)


#Since we only want the TOP 5 closest destinations that fit the criteria, we can use the already
#sorted list cities and only output the first 5 elements
#the organization of place in cities ex: cities = [ [0,{'city':etc,'summer':etc}], [0,{'city':etc,'summer':etc}] ++++++] 

    for i in range(0,5):

        #references the first list in cities and the first element in that list
        distance_ = cities[i][0]

        #here i added the conversion for miles.
        d_miles = distance_*0.621371

        #ct references the dictionary for every element. 
        #This allowed me to organize them much better in the output
        cT = cities[i][1]

        output = "{}: {}, {}, {}, distance: {:.2f}km or {:.2f} miles\n".format(i+1,cT['city'],cT['state'],cT['country'], distance_, d_miles)
        print(output)
        

#IF VALIDATION IS EQUAL TO 0 meaning the error handling caught an error it outputs 
#the formated strings created earlier

elif validation1 == 0 or validation2 == 0:
    print(error_message1)
    print(error_message2)

