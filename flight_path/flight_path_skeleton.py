def flight_path_skeleton(flight, no_fly):
	destination = flight[2]
	next_start = flight[1]
	
	weather_27000 = no_fly[0]
	weather_32000 = no_fly[1]
	weather_zones = [weather_27000, weather_32000]
	
	skeleton = [flight[1]]
	rz_notes = [] ## Test if flying over no_fly_zone. [[<ordinal_over_zone>,<Upper_Bound>]]
	
	ordinal = 0
	prev_line = 0 
	buffer = .5
	
	while skeleton[-1] != destination:
		next_line = shapely.geometry.LineString(no_fly, [next_start, destination])
		intersect_test = test_intersect(no_fly, next_line)
		if False:
			skeleton.append(destination)
		elif intersect_test in weather_zones:
			bound = intersect_test[2]
			next_start, prev_line = find_closests_intersect(next_start, destination, intersect_test, prev_line, buffer)
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
	
def find_closests_intersect(curr_point, dest_point, intersect_test, prev_line, buffer): # Finds the closest intersect of a polygon
	points = intersect_test[1]
	line_polygon = create_lines(points)
	
	base_line_1 = array( tuple(curr_point) )
	base_line_2 = array( tuple(dest_point) )
	
	intersects = []
	
	for line in line_polygon:
		test_line_1 = array( tuple(line[0]) )
		test_line_2 = array( tuple(line[1]) )
		result = seg_intersect(base_line_1, base_line_2, test_line_1, test_line_2)
		result_list = list(result)
		if math.isnan(result_list[0]) == False:
			base_x = curr_point[0]
			base_y = curr_point[1]
			to_x = result_list[0]
			to_y = result_list[1]
			
			distance = find_distance(base_x, base_y, to_x, to_y)
			intersects.append([result_list, distance, result_line])

	shortest_point, distance, intersect_line = check_shortest_distance(intersects, prev_line)
	
	if prev_line == 0:
		go_distance = distance - buffer
		next_prev_line = intersect_line
	else:
		go_distance = distance + buffer
		next_prev_line = 0
		
	next_start = find_next_ne_twopoints(curr_point[0], curr_point[1], dest_point[0], dest_point[1], go_distance)

	return next_start, next_prev_line
	

def create_lines(points): #Create the exterior lines of the polygon
	lines = []
	length = len(points)
	
	p1 = points[0]
	points.append(p1)
	
	for i in range(0, length - 1):
		line = [points[i], points[i+1]]
		lines.append(line)	
	
	return lines
	
def check_shortest_distance(intersects, prev_line):
	if prev_line != 0:
		intersects = filter(lambda a : a != prev_line, intersects)	
		
	point_dis =[0, 100000, [0,0]]
	
	for i in intersects:
		if i[1] < point_dis[1]:
			point_dis == i
	
	
	return point_dis[0], point_dis[1], point_dis[2]
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	