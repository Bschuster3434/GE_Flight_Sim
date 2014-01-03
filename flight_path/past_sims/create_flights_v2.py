##### My goal with this script is to write a two-ordinal output file
##### that takes the plane from 35000 feet and 500 mph to 17000 and 250mph

execfile("lambert.py") #Converts lambert and x,y values
execfile("haversine.py") 
import csv
import math

airports_file = 'Airports.csv'
flights_file = 'flights_20130910_1803.csv'


#Opens Airport Files and Converts them to X,Y
airports_xy = {} #Dictionary of XY airport coordinates
with open(airports_file, 'rb') as csv_airports:
	airports_lam = csv.reader(csv_airports, delimiter=',')
	first_row = 0 #Used to skip the first row
	for row in airports_lam:
		if first_row == 0:
			first_row = 1
		else:
			airports_xy[row[0]] = fromlambert(float(row[1]), float(row[2]))
			
#	Reads the flights for today and returns their Id and Airport Destination		
flights = [] #List for flight numbers and Airport Destination

if flights_file == 'TestFlights.csv': #This is the test case used for the final submission
	with open(flights_file, 'rb') as csv_todays_flights:
		flights_rows = csv.reader(csv_todays_flights, delimiter=',')
		first_row = 0 #Used to skip the first row
		for row in flights_rows:
			if first_row == 0:
				first_row = 1
			else:
				current = [row[4], row[5]]
				flights.append([row[0], float(current[0]), float(current[1]), row[2]])
				##['flight id', 'current latitude', 'current longitude', 'destination airport'] 

else:
	with open(flights_file, 'rb') as csv_todays_flights:
		flights_rows = csv.reader(csv_todays_flights, delimiter=',')
		first_row = 0 #Used to skip the first row
		for row in flights_rows:
			if first_row == 0:
				first_row = 1
			else:
				current = fromlambert(float(row[1]), float(row[2]))
				flights.append([row[0], current[0], current[1], row[5]])
				##['flight id', 'current latitude', 'current longitude', 'destination airport']	

				
def find_theta(current, destination):
	adjacent_len = destination[1] - current[1]  #Longitude
	opposite_len = destination[0] - current[0] #Latitude
	
	theta = math.atan2(opposite_len, adjacent_len)
	
	return theta
	

#########################################
# MAIN PROGRAM TO SCRIPT FLIGHTS
#########################################

#Creates the flight plane to be converted
flight_plan = [["FlightId","Ordinal","Latitude","Longitude","Altitude","Airspeed"]] #Flight Header for export file

descent_distance = 100 ##Given in Miles

for flight_info in flights: ####TESTING ONLY
	###Find the X,Y coordinates between the airports and current
	dest_airport = flight_info[3]
	dest_coor = airports_xy[dest_airport]
	curr_coor = [flight_info[1], flight_info[2]]
	
	###Find distance between airplane and airport
	
	distance = haversine(dest_coor[0], dest_coor[1], curr_coor[0], curr_coor[1])
	
	### Find theta of the angle between the airport and the current point
	
	theta = find_theta(curr_coor, dest_coor)
	
	descent_point = find_next_point(dest_coor[0], dest_coor[1], descent_distance, theta)
	
	###If Greater than 150 miles out, set path to X miles out at 38000 and speed of 450
	###Else, set path to destination airport at 10000 and speed of 250
	if distance > descent_distance:
		flight_plan.append([flight_info[0],1,descent_point[0], descent_point[1],28000, 500])
		flight_plan.append([flight_info[0],2,dest_coor[0],dest_coor[1],17000,250])
	else:
		flight_plan.append([flight_info[0],1,dest_coor[0],dest_coor[1],17000,250])
		
	
			
		
			
####Writes flight_plan to CSV file
with open('todays_flights.csv', 'wb') as write_file:
	flight_writer = csv.writer(write_file, delimiter=',')
	for i in flight_plan:
		flight_writer.writerow(i)
		
		
		
		
		
		