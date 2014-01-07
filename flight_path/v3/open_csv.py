import csv

def get_airport_coordinates(file):
	airports_ne = {} ##Airports Northing Easting Dictionary
	with open(file, 'rb') as csv_airports:
		reader = csv.reader(csv_airports, delimiter=',')
		next(reader, None)
		for row in reader: #skips the first row
			airports_ne[row[0]] = [float(row[1]), float(row[2])] #Easting, Northing
	return airports_ne

def get_flight_info(file):
	flight_list = [] ##[flightid, arrival airport, [easting, northing], altitude]
	with open(file, 'rb') as csv_flights:
		reader = csv.reader(csv_flights, delimiter=',')
		next(reader, None) # skips the headers
		check_test = file.find('TestFlights.csv')
		if check_test == -1:
			for row in reader:
				flight_list.append([row[0], row[5], [float(row[1]), float(row[2])], float(row[3])])
		else: 
			for row in reader:
				lon = float(row[5]); lat = float(row[4]) 
				e_n_con = tolambert(lat, lon) #Need to covert X,Y into Easting Northing
				flight_list.append([row[0], row[2], e_n_con, row[6]])
				
	return flight_list
	
def create_coordinate_pairing(a_file, f_file):
	current_dest_pairings = [] ##[FlightId, [current easting, current northing], [dest easting, dest northing]]
	
	airports = get_airport_coordinates(a_file)
	flights = get_flight_info(f_file)
	
	for i in flights:
		current_dest_pairings.append([i[0], [float(i[2][0]), float(i[2][1])], airports[i[1]], i[3]])
	
	return current_dest_pairings
		
def get_extra_flight_details(flights_file):
	extra_details = []
	with open(flights_file) as csv_flights:
		reader = csv.reader(csv_flights, delimiter=',')
		next(reader, None)
		check_test = file.find('TestFlights.csv')
		if check_test == -1:
			for row in reader:
				flight_list.append([row[0], row[5], [float(row[1]), float(row[2])], float(row[3])])
		else: 
			for row in reader:
				lon = float(row[5]); lat = float(row[4]) 
				e_n_con = tolambert(lat, lon) #Need to covert X,Y into Easting Northing
				flight_list.append([row[0], row[2], e_n_con, row[6]])
				
	return flight_list
		