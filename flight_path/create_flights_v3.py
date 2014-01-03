execfile('utility.py')

csv_path = "csv_files/"

airports_file = csv_path + "Airports.csv"
flights_file = csv_path + "flights_20130910_1803.csv"
rz = pd.read_csv(csv_path + 'restrictedZones.csv') ##Opens the no fly zone csv file and grabs the Lambert vertices
en_verts = list(rz['XYLambertVertices'])

### BelowFormat = [FlightId, [current easting, current northing], [destination easting, destination northing]]
dest_pair = create_coordinate_pairing(airports_file, flights_file)

##Creates the no fly zone polygons
no_fly_zones = create_nofly_polygons(en_verts)

def agent_one_ordinal(flight_pairs):
	ordinal_list = [['FlightId', 'Ordinal', 'Latitude', 'Longitude', 'Altitude', 'AirSpeed']]
	for flight in flight_pairs:
		easting = flight[1][0]; northing = flight[1][1]
		current_xy_convert =  fromlambert(easting, northing) ##returns [lat, lon]
		latitude = current_xy_convert[0]; longitude = current_xy_convert[1]
		ordinal_list.append([flight[0], 1, latitude, longitude, 17000, 250])
	return ordinal_list
		
def agent_two_ordinal(flight_pairs):
	ordinal_list = [['FlightId', 'Ordinal', 'Latitude', 'Longitude', 'Altitude', 'AirSpeed']]
	for flight in flight_pairs:
		oe = flight[2][0]; on = flight[2][1]
		ce = flight[1][0]; cn = flight[1][1]
		
		angle_to_plane = find_theta(oe, on, ce, cn)
		
		miles_to_LambertDegrees = 1.1234 ##On Average, the number of miles per 1 degree lambert movement
		descent_distance = 100 / miles_to_LambertDegrees
		
		current_distance = find_distance(oe, on, ce, cn)
		
		##Start Descent Point
		dest_xy = fromlambert(flight[2][0], flight[2][1]) #[lat, long]
		
		##Else, send the plane to the descent distance, then send to the airport
		if current_distance > descent_distance:
			descent_ne = find_next_ne(oe, on, descent_distance, angle_to_plane) #[easting, northing]
			descent_xy = fromlambert(descent_ne[0], descent_ne[1]) #[lat, long]
			ordinal_list.append([flight[0], 1, descent_xy[0], descent_xy[1], 35000, 500])
			ordinal_list.append([flight[0], 2, dest_xy[0], dest_xy[1], 17000, 250])
		else:
			ordinal_list.append([flight[0], 1, dest_xy[0], dest_xy[1], 17000, 250])
		
	return ordinal_list
			
		##If the plane is within the descent distance, send to airport	
		
def write_list_to_csv(ordinals):
	with open('todays_flights.csv', 'wb') as write_file:
		flight_writer = csv.writer(write_file, delimiter=',')
		for i in ordinals:
			flight_writer.writerow(i)
			
ordinals = agent_two_ordinal(dest_pair)
write_list_to_csv(ordinals)
			
		
		