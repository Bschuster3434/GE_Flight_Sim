execfile('open_csv.py')
execfile('find_theta.py')
execfile('lambert.py')
execfile('create_no_fly_zones.py')
execfile('seg_intersect.py')
execfile('avoid_nofly.py')
###################################################################################
##Step 1 to open the CSV file and get the correct information in the right way
##Utilizes 'open_csv.py'

csv_path = "csv_files/"

airports_file = csv_path + "Airports.csv"
flights_file = csv_path + "test_flight.csv"

### BelowFormat = [FlightId, [current easting, current northing], [destination easting, destination northing]]
dest_pair = create_coordinate_pairing(airports_file, flights_file)

###################################################################################
### Step 2 to get the destination pairs into the correct ordinals
#Utilizes 'find_theta.py', 'create_no_fly_zones.py' and 'seg_intersect.py'

miles_to_degrees = 1.1234 #miles to one degree movement in lambert, on average
descent_miles = 120

degree_distance = descent_miles/miles_to_degrees


def avoidance_agent(dest_pair):
	rz = pd.read_csv(csv_path + 'restrictedZones.csv') ##Opens the no fly zone csv file and grabs the Lambert vertices
	en_verts = list(rz['XYLambertVertices'])
	UpperBound = list(rz['UpperBound'])
	no_fly_list = create_nofly_polygons(en_verts) ## returns [<Polygon>, Points that make up the polygon]
	list_length = len(UpperBound)
	no_fly = []
	for i in range(0, list_length):
		no_fly_list[i].append(int(UpperBound[i]))
		if no_fly_list[i][2] > 33000:
			no_fly.append(no_fly_list[i])

	flight_ordinals = []
	
	count = 0
	
	for flight in dest_pair:
		cur_point = flight[1]
		dest_point = flight[2]
		cur_altitude = flight[3]
		path = shapely.geometry.LineString([cur_point, dest_point])
		intersect_result = test_intersect(no_fly, path)
		if intersect_result == False:
			current_distance = find_distance(dest_point[0], dest_point[1], cur_point[0], cur_point[1])
			if current_distance > degree_distance:
				descent_point = find_next_ne(dest_point[0], dest_point[1], cur_point[0], cur_point[1], degree_distance)
				flight_ordinals.append([flight[0], flight[1], descent_point, flight[2]])
			else:
				flight_ordinals.append([flight[0], flight[1], flight[2]])
		else:
			pivot_point = avoid_nofly(flight, intersect_result, no_fly)
			if pivot_point == 0: ### Tests the scenario if one pivot point fails
				#### Now we need to look for a 2nd ordinal
				new_radials = find_new_points(cur_point, dest_point) ## Returns a list of Easting, Northing Points
				#for i in new_radials:
				#	print i
				second_point = []
				for point in new_radials: ##Tests the Line String between Current Point and New Point to confirm it's not in a no fly zone
					new_line = shapely.geometry.LineString([cur_point, point])
					result = test_intersect(no_fly, new_line)
					if result == False:
						second_point.append(point)
				
				#### This is the 'I've given up on you' part of the code
				#### For flights that just won't find the right id
				
				distance_check = []
				for point in second_point: ##Tests the new point to see if it can pass the avoid_nofly test
					next_line = shapely.geometry.LineString([cur_point, point, dest_point])
					result = test_intersect(no_fly, next_line)
					if result == False:
						distance = multiline_distance(point, cur_point, dest_point)
						distance_check.append([distance, [point]])
					else:
						new_flight = [flight[0], point, flight[2]] #Replacing current point with the new test point
						second_avoid_point = avoid_nofly(new_flight, intersect_result, no_fly)
						if second_avoid_point == 0:
							continue
						distance_one = multiline_distance(point, cur_point, second_avoid_point)
						distance_two = find_distance(second_avoid_point[0], second_avoid_point[1], dest_point[0], dest_point[1])
						distance = distance_one + distance_two
						distance_check.append([distance, [point, second_avoid_point]])
								
				next_ords = [100000,[]]
				for points in distance_check:
					if points[0] < next_ords[0]:
						next_ords = points
						
				if next_ords[0] == 100000:
					descent_point = find_next_ne(dest_point[0], dest_point[1], cur_point[0], cur_point[1], degree_distance)
					flight_ordinals.append([flight[0], flight[1], descent_point, flight[2]])
					continue						
						
				if len(next_ords[1]) == 1:
					pivot_point = next_ords[1][0]
					pivot_distance = find_distance(dest_point[0], dest_point[1], pivot_point[0], pivot_point[1])
					if pivot_distance > degree_distance:
						descent_point = find_next_ne(dest_point[0], dest_point[1], pivot_point[0], pivot_point[1], degree_distance)
						flight_ordinals.append([flight[0], flight[1], pivot_point, descent_point, flight[2]])
					else:
						flight_ordinals.append([flight[0], flight[1], pivot_point, flight[2]])
				else:
					prev_point = next_ords[1][0]
					pivot_point = next_ords[1][1]
					pivot_distance = find_distance(dest_point[0], dest_point[1], pivot_point[0], pivot_point[1])
					if pivot_distance > degree_distance:
						descent_point = find_next_ne(dest_point[0], dest_point[1], pivot_point[0], pivot_point[1], degree_distance)
						flight_ordinals.append([flight[0], flight[1], prev_point, pivot_point, descent_point, flight[2]])
					else:
						flight_ordinals.append([flight[0], flight[1], prev_point, pivot_point, flight[2]])						
				
				
				
			else:
				pivot_distance = find_distance(dest_point[0], dest_point[1], pivot_point[0], pivot_point[1])
				if pivot_distance > degree_distance:
					descent_point = find_next_ne(dest_point[0], dest_point[1], pivot_point[0], pivot_point[1], degree_distance)
					flight_ordinals.append([flight[0], flight[1], pivot_point, descent_point, flight[2]])
				else:
					flight_ordinals.append([flight[0], flight[1], pivot_point, flight[2]])
	
	flight_ords = create_ordinals(flight_ordinals)
	
	return flight_ords		
	
def create_ordinals(flight_ordinals):
	##Final Format is [Flight Id, Ordinal, Latitude, Longitude, Altitude, Airspeed]
	ordinals = [['FlightId', 'Ordinal', 'Latitude', 'Longitude', 'Altitude', 'Airspeed']]
	for flight in flight_ordinals:
		order = []
		flightid = flight[0]
		ordered_list = flight[2:]
		list_length = len(ordered_list)
		ordinal_number = 1
		for i in ordered_list:
			xy_coor = fromlambert(i[0], i[1])
			if i != ordered_list[list_length - 1]:
				order_info = [flightid, ordinal_number, xy_coor[0], xy_coor[1], 32000, 600]
				ordinal_number = ordinal_number + 1
			else:
				order_info = [flightid, ordinal_number, xy_coor[0], xy_coor[1], 17990, 250]
			ordinals.append(order_info)
	
	return ordinals	

	


##Finishing Step: Writes the ordinals to the csv		
def write_list_to_csv(ordinals):
	with open('todays_flights.csv', 'wb') as write_file:
		flight_writer = csv.writer(write_file, delimiter=',')
		for i in ordinals:
			flight_writer.writerow(i)

write_to_list = avoidance_agent(dest_pair)
write_list_to_csv(write_to_list)
			
		
		