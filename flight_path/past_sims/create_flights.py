execfile("lambert.py") #Converts lambert and x,y values
execfile("haversine.py") #Finds miles between two points
import csv
import math

airports_file = 'Airports.csv'
flights_file = 'TestFlights.csv'

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
with open(flights_file, 'rb') as csv_todays_flights:
	flights_rows = csv.reader(csv_todays_flights, delimiter=',')
	first_row = 0 #Used to skip the first row
	for row in flights_rows:
		if first_row == 0:
			first_row = 1
		else:
			flights.append([row[0], row[2], row[4], row[5]])

#Creates the flight plane to be converted
flight_plan = [["FlightId","Ordinal","Latitude","Longitude","Altitude","Airspeed"]] #Flight Header for export file

#Goes through flights and finds the airport to convert to X,Y, then creates the logs
for i in flights:
	lat_lon_dest = airports_xy[i[1]]
	flight_plan.append([i[0],0,lat_lon_dest[0],lat_lon_dest[1],3000,250])

#Writes flight_plan to CSV file
with open('todays_flights.csv', 'wb') as write_file:
	flight_writer = csv.writer(write_file, delimiter=',')
	for i in flight_plan:
		flight_writer.writerow(i)

