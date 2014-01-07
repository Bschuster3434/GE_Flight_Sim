airport_file = 'Airports.csv'

def open_flight_csv(file):
	flight_info = [] ##[Flightid, [current easting, current northing], [destination easting, destination northing], altitude, fuel remaining]
	airport_dict = get_airport_coordinates(airport_file)
	with open(file) as csv_flights:
		reader = csv.reader(csv_flights, delimiter=',')
		next(reader, None)
		check_test = file.find('TestFlights.csv')
		

		for row in reader:
			flightId = row[0]		
			if check_test == -1:
				current_coor = [float(row[1]), float(row[2])]
				dest_coor = airport_dict[row[5]]			
				altitude = float(row[3])
				fuel_remaining = float(row[8]) - float(row[9])
			
			else:
				current_coor = tolambert(float([4]), float([5]))
				dest_coor = airport_dict[row[2]]
				altitude = float(row[6])
				fuel_remaining = float([10])
			
			to_append = [flightId, current_coor, dest_coor, altitude, fuel_remaining]
		
			flight_info.append(to_append)
			
	return flight_info
			

def get_airport_coordinates(file):
	airports_ne = {} ##Airports Northing Easting Dictionary
	with open(file, 'rb') as csv_airports:
		reader = csv.reader(csv_airports, delimiter=',')
		next(reader, None)
		for row in reader: 
			airports_ne[row[0]] = [float(row[1]), float(row[2])] #Easting, Northing
	return airports_ne
	