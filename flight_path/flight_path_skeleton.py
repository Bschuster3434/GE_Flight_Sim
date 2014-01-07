def flight_path_skeleton(flight, no_fly):
	destination = flight[2]
	next_start = flight[1]
	
	weather_27000 = no_fly[0]
	weather_32000 = no_fly[1]
	weather_zones = [weather_27000, weather_32000]
	
	skeleton = [flight[1]]
	rz_notes = [] ## Test if flying over no_fly_zone. [[<ordinal_over_zone>,<Upper_Bound>]]
	
	ordinal = 0
	
	while skeleton[-1] != destination:
		next_line = shapely.geometry.LineString(no_fly, [next_start, destination])
		intersect_test = test_intersect(no_fly, next_line)
		if False:
			skeleton.append(destination)
		elif intersect_test in weather_zones:
			bound = intersect_test[2]
			next_start = find_closests_intersect(next_start, destination, intersect_test)
			skeleton.append(next_start)
			rz_notes.append([ordinal, bound])
		else:
			next_start = avoidance(next_start, destination, intersect_test)
			skeleton.append(next_start)
		
		ordinal = ordianl + 1
		
	return skeleton ## List of ordinals that will accurately avoid no_fly zones
	

def test_intersect(no_fly, line):
	for zone in no_fly:
		if line.intersects(zone[0]) == True:
			return zone
	return False
	
def avoidance(curr_point, dest_point, zone): ##[restricted zone polygon, restricted zone points, restricted zone upper bound]
	polygon = zone[0]
	edge_points = zone[1]
	
	return avoidance_point
	
def find_closests_intersect(curr_point, dest_point, intersect_test): # Finds the closest intersect of a polygon
	points = intersect_test[1]
	line_polygon = create_lines(points)
	
	

def create_lines(points): #Create the exterior lines of the polygon
	lines = []
	length = len(points)
	
	p1 = points[0]
	points.append(p1)
	
	for i in range(0, length - 1):
		line = [points[i], points[i+1]]
		lines.append(line)	
	
	return lines
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	