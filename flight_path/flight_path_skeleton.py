def flight_path_skeleton(flight, no_fly):
	destination = [flight[2], 0]
	print destination
	
	test_start_point = find_next_ne_angle(flight[1][0], flight[1][1], 0, .01)
	next_line = shapely.geometry.LineString([flight[1], test_start_point])
	intersect_test = test_intersect(no_fly, next_line, flight[1], destination[0][0] )	
	
	if intersect_test == False:
		next_start = [flight[1], 0]
	else:
		next_start = [flight[1], intersect_test[2]]
	
	weather_27000 = no_fly[0]
	weather_32000 = no_fly[1]
	weather_zones = [weather_27000, weather_32000]
	
	skeleton = [next_start]
	rz_notes = [] ## Test if flying over no_fly_zone. [[<ordinal_over_zone>,<Upper_Bound>]]
	
	ordinal = 1
	intersect_cross = .5 
	buffer = 10
	
	counter = 0
	
	while skeleton[-1] != destination:
		next_line = shapely.geometry.LineString([next_start[0], destination[0]])
		intersect_test = test_intersect(no_fly, next_line, next_start[0], destination[0])
		bound = 0
		if intersect_test == False:
			skeleton.append(destination)
		elif intersect_test in weather_zones:
			bound = intersect_test[2]
			next_point = find_closests_intersect(next_start[0], destination[0], intersect_test, intersect_cross)
			skeleton.append([next_point, bound])
			next_start = [next_point, bound]
		else:
			next_point = avoidance(next_start[0], destination[0], intersect_test, buffer, no_fly)
			skeleton.append([next_point, bound])
			next_start = [next_point, bound]
		
		ordinal = ordinal + 1
		counter = counter + 1
		
		if counter > 20:
			skeleton.append(destination)
			for i in skeleton:
				print i
			break
		
	return skeleton ## List of ordinals that will accurately avoid no_fly zones
	

def test_intersect(no_fly, line, next_start, destination):
	
	sub_no_fly_zone = []
	
	for zone in no_fly:
		if line.intersects(zone[0]) == True:
			sub_no_fly_zone.append(zone)
	
	if len(sub_no_fly_zone) == 0:
		return False
	elif len(sub_no_fly_zone) == 1:
		return sub_no_fly_zone[0]
	else:
		line_distance = find_distance(next_start[0], next_start[1], destination[0], destination[1])
		angle = find_theta(next_start[0], next_start[1], destination[0], destination[1])
		breaks = 100
		for i in range(1, breaks + 1):
			next_distance = line_distance * float(i) / breaks
			next_test_point = find_next_ne_angle(next_start[0], next_start[1], angle, next_distance)
			next_line = shapely.geometry.LineString([next_start, next_test_point])
			next_intersect_test = test_intersect(sub_no_fly_zone, next_line, [0,0],[0,0])
			if next_intersect_test != False:
				return next_intersect_test
	
	
	
	
def avoidance(curr_point, dest_point, zone, buffer, no_fly): ##[restricted zone polygon, restricted zone points, restricted zone upper bound]
	polygon = zone[0]
	edge_points = zone[1]
	
	visible_edges = find_visible_edges(curr_point, polygon, edge_points)
	next_start = find_furthest_point(curr_point, dest_point, visible_edges, buffer, no_fly)
	
	return next_start
	
def find_closests_intersect(curr_point, dest_point, intersect_test, intersect_cross): # Finds the closest intersect of a polygon
	points = intersect_test[1]
	line_polygon = create_lines(points)

	base_line_1 = array( tuple(curr_point) )
	base_line_2 = array( tuple(dest_point) )
	
	intersects = []
	
	for line in line_polygon:
	## Need to find a suitable script to calculate if two line segments intersect

		test_line_1 = array( tuple(line[0]) )
		test_line_2 = array( tuple(line[1]) )
		result = intersect(base_line_1, base_line_2, test_line_1, test_line_2)
		if result == True:
			intersect_point = seg_intersect(base_line_1, base_line_2, test_line_1,test_line_2)
			distance = find_distance(curr_point[0], curr_point[1], intersect_point[0], intersect_point[1])
			intersects.append([list(intersect_point), distance, line])
	
	shortest_point, distance, intersect_line = check_shortest_distance(intersects)

	go_distance = distance + intersect_cross
		
	next_start = find_next_ne_twopoints(curr_point[0], curr_point[1], shortest_point[0], shortest_point[1], go_distance)
	
	return next_start
	

def create_lines(points): #Create the exterior lines of the polygon
	lines = []
	length = len(points)
	
	for i in range(0, length - 1):
		line = [points[i], points[i + 1]]
		lines.append(line)	
	
	return lines
	
def check_shortest_distance(intersects):
	ints = []
		
	point_dis =[0, 100000, [0,0]]
	
	for i in intersects:
		if i[1] < point_dis[1]:
			point_dis = i
	
	
	return point_dis[0], point_dis[1], point_dis[2]
	
def find_visible_edges(curr_point, polygon, edge_points):
	visible = []
	diminish_line = .99999
		
	edge_angles = calculate_all_opposite_angles(edge_points, polygon)
	
	for edge, edge_angle in edge_angles:
		distance = find_distance(curr_point[0], curr_point[1], edge[0], edge[1])
		angle = find_theta(curr_point[0], curr_point[1], edge[0], edge[1])
		test_dis = distance * diminish_line
		test_point = find_next_ne_angle(curr_point[0], curr_point[1], angle, test_dis)
		test_line = shapely.geometry.LineString([[curr_point[0], curr_point[1]], [test_point[0], test_point[1]]])
		result = test_line.intersects(polygon)
		if result == False:
			visible.append([edge, edge_angle])
			
	return visible
	
def calculate_all_opposite_angles(edge_points, polygon):
	length = len(edge_points)

	
	edge_angles = []
	
	for i in range(0, length):
		if i == 0:
			previous = edge_points[length - 2]
		else:
			previous = edge_points[i - 1]		
		current = edge_points[i]
		if i == length - 1:
			next = edge_points[1]
		else:
			next = edge_points[i + 1]
			
		opposite_angle = find_opposite_angle(previous, current, next, polygon)
		edge_angles.append([current, opposite_angle])
		
	return edge_angles
	

def find_polygon_center(edge_points):
	num_of_points = len(edge_points)
	
	x,y = 0, 0
	
	for i in range(0, num_of_points):
		x , y = x + edge_points[i][0], y + edge_points[i][1]
	
	new_x = x / num_of_points
	new_y = y / num_of_points
	
	return [new_x, new_y]
	
	

def find_opposite_angle(previous, current, next, polygon):
	
	angle_1 = (find_theta(current[0], current[1], previous[0], previous[1])) % ( 2 * math.pi )
	angle_2 = find_theta(current[0], current[1], next[0], next[1]) % ( 2 * math.pi )
	
	angle_difference = ((angle_1 + angle_2) / 2) 
	
	point_test = find_next_ne_angle(current[0], current[1], angle_difference, 2); new_point = find_next_ne_angle(point_test[0], point_test[1], 0, .01)
	line = shapely.geometry.LineString([point_test, new_point])
	
	spot_point_test = line.intersects(polygon)
	
	if spot_point_test == True:
		opposite = (angle_difference + math.pi) % ( 2 * math.pi )
	else:
		opposite = angle_difference
	
	return opposite
		
def test_positive_or_negative(number):
	if number > 0:
		return True
	else:
		return False
		
def find_furthest_point(curr_point, dest_point, visible_edges, buffer, no_fly):
	
	to_the_dest_angle = find_theta(curr_point[0], curr_point[1], dest_point[0], dest_point[1])
	right_angle = math.pi/2
	find_right_point_angle = to_the_dest_angle + right_angle
	find_left_point_angle = to_the_dest_angle - right_angle
	
	right_candidate, right_distance, right_ma = one_side_furthest(curr_point, dest_point, find_right_point_angle, visible_edges)
	left_candidate, left_distance, left_ma = one_side_furthest(curr_point, dest_point, find_left_point_angle, visible_edges)
	
	r_line = shapely.geometry.LineString([curr_point, right_candidate])
	r_inf = test_intersect(no_fly, r_line, curr_point, right_candidate)
	
	if right_distance > 0 and r_inf != False:
		f_point, m_angle = right_candidate, right_ma
	else:
		f_point, m_angle = left_candidate, left_ma
		
		
		
	furthest_point = find_next_ne_angle(f_point[0], f_point[1], m_angle, buffer)	
		
	return furthest_point

def one_side_furthest(curr_point, dest_point, angle, visible_edges):
	
	furthest_point = [0,0]
	distance = 0
	move_angle = 0
	
	curr_dest_angle = find_theta(curr_point[0], curr_point[1], dest_point[0], dest_point[1])
	seg_point_1 = find_next_ne_angle(curr_point[0], curr_point[1], (curr_dest_angle + math.pi), 10000)
	seg_point_2 = find_next_ne_angle(curr_point[0], curr_point[1], curr_dest_angle, 10000)
	
	for point, m_angle in visible_edges:
		test_point = find_next_ne_angle(point[0], point[1], angle, 500)
		##test_line = shapely.geometry.LineString([point[0], point[1], test_point[0], test_point[1]])
		result = intersect(seg_point_1, seg_point_2, point, test_point)
		if result == False:
			continue
		else:
			intersect_result = seg_intersect(array(tuple(curr_point)),array(tuple(dest_point)),array(tuple(point)),array(tuple(test_point)))
			intersect_result = list(intersect_result)
			new_distance = find_distance(point[0], point[1], intersect_result[0], intersect_result[1])
			if new_distance > distance:
				furthest_point, distance, move_angle = point, new_distance, m_angle
	
	
	return furthest_point, distance, move_angle
	
	
	
	
	
	