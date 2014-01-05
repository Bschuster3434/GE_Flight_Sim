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
flights_file = csv_path + "flights_20130910_1803.csv"

### BelowFormat = [FlightId, [current easting, current northing], [destination easting, destination northing]]
dest_pair = create_coordinate_pairing(airports_file, flights_file)

###################################################################################
### Step 2 to get the destination pairs into the correct ordinals
#Utilizes 'find_theta.py', 'create_no_fly_zones.py' and 'seg_intersect.py'

miles_to_degrees = 1.1234 #miles to one degree movement in lambert, on average
descent_miles = 100

degree_distance = descent_miles/miles_to_degrees


def avoidance_agent(dest_pair):
	rz = pd.read_csv(csv_path + 'restrictedZones.csv') ##Opens the no fly zone csv file and grabs the Lambert vertices
	en_verts = list(rz['XYLambertVertices'])
	no_fly = create_nofly_polygons(en_verts) ## returns [<Polygon>, Points that make up the polygon]
	
	flight_ordinals = []
	
	for flight in dest_pair:
		cur_point = flight[1]
		dest_point = flight[2]
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
			pivot_distance = find_distance(dest_point[0], dest_point[1], pivot_point[0], pivot_point[1])
			if pivot_distance > degree_distance:
				descent_point = find_next_ne(dest_point[0], dest_point[1], pivot_point[0], pivot_point[1], degree_distance)
				flight_ordinals.append([flight[0], flight[1], pivot_point, descent_point, flight[2]])
			else:
				flight_ordinals.append([flight[0], flight[1], pivot_point, flight[2]])
				
	return flight_ordinals		
	
	


##Finishing Step: Writes the ordinals to the csv		
def write_list_to_csv(ordinals):
	with open('todays_flights.csv', 'wb') as write_file:
		flight_writer = csv.writer(write_file, delimiter=',')
		for i in ordinals:
			flight_writer.writerow(i)

			
		
		