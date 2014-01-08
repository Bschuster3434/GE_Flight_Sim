def flight_path_skeleton(flight, no_fly):
	destination = flight[2]
	next_start = flight[1]
	
	weather_27000 = no_fly[0]
	weather_32000 = no_fly[1]
	weather_zones = [weather_27000, weather_32000]
	
	skeleton = [flight[1]]
	rz_notes = [] ## Test if flying over no_fly_zone. [[<ordinal_over_zone>,<Upper_Bound>]]
	
	ordinal = 1
	intersect_cross = .5 #
	no_fly_buffer = 3
	buffer = 3
	
	counter = 0
	
	while skeleton[-1] != destination:
		next_line = shapely.geometry.LineString([next_start, destination])
		intersect_test = test_intersect(no_fly, next_line)
		if intersect_test == False:
			skeleton.append(destination)
		elif intersect_test in weather_zones:
			bound = intersect_test[2]
			next_start = find_closests_intersect(next_start, destination, intersect_test, intersect_cross)
			skeleton.append(next_start)
			rz_notes.append([ordinal, bound])
		else:
			next_start = avoidance(next_start, destination, intersect_test, buffer)
			skeleton.append(next_start)
		
		ordinal = ordinal + 1
		counter = counter + 1
		
		if counter > 20:
			print flight
			break
		
	return skeleton, rz_notes ## List of ordinals that will accurately avoid no_fly zones
	

def test_intersect(no_fly, line):
	for zone in no_fly:
		if line.intersects(zone[0]) == True:
			return zone
	return False
	
def avoidance(curr_point, dest_point, zone, buffer): ##[restricted zone polygon, restricted zone points, restricted zone upper bound]
	polygon = zone[0]
	edge_points = zone[1][:-1] #takes the final duplicate point off
	
	visible_edges = find_visible_edges(curr_point, polygon, edge_points)
	next_start = find_furthest_point(curr_point, dest_point, visible_edges, buffer)
	
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
		
	next_start = find_next_ne_twopoints(curr_point[0], curr_point[1], dest_point[0], dest_point[1], go_distance)

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
	diminish_line = .98
		
	edge_angles = calculate_all_opposite_angles(edge_points)
	
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
	
def calculate_all_opposite_angles(edge_points):
	length = len(edge_points)
	
	edge_angles = []
	
	for i in range(0, length):
		previous = edge_points[i - 1]		
		current = edge_points[i]
		if i == length - 1:
			next = edge_points[0]
		else:
			next = edge_points[i + 1]
			
		opposite_angle = find_opposite_angle(previous, current, next)
		edge_angles.append([current, opposite_angle])
		
	return edge_angles

def find_opposite_angle(previous, current, next):
	
	angle_1 = find_theta(current[0], current[1], previous[0], previous[1]) % (2 * math.pi)
	angle_2 = find_theta(current[0], current[1], next[0], next[1]) % (2 * math.pi)

	angle_difference = (angle_1 + angle_2) / 2
	opposite_angle = (angle_difference + math.pi) % (2 * math.pi)
		
	return opposite_angle
		
def find_furthest_point(curr_point, dest_point, visible_edges, buffer):
	
	to_the_dest_angle = find_theta(curr_point[0], curr_point[1], dest_point[0], dest_point[1])
	right_angle = math.pi/2
	find_right_point_angle = to_the_dest_angle + right_angle
	find_left_point_angle = to_the_dest_angle - right_angle
	
	right_candidate, right_distance, right_ma = one_side_furthest(curr_point, dest_point, find_right_point_angle, visible_edges)
	left_candidate, left_distance, left_ma = one_side_furthest(curr_point, dest_point, find_left_point_angle, visible_edges)
	
	if right_distance > left_distance:
		f_point, m_angle = right_candidate, right_ma
	else:
		f_point, m_angle = left_candidate, left_ma
		
	furthest_point = find_next_ne_angle(f_point[0], f_point[1], m_angle, buffer)	
		
	return furthest_point
	
	

def one_side_furthest(curr_point, dest_point, angle, visible_edges):
	
	furthest_point = [0,0]
	distance = 0
	move_angle = 0
	
	for point, m_angle in visible_edges:
		test_point = find_next_ne_angle(point[0], point[1], angle, 500)
		##test_line = shapely.geometry.LineString([point[0], point[1], test_point[0], test_point[1]])
		result = intersect(curr_point, dest_point, point, test_point)
		if result == False:
			continue
		else:
			intersect_result = seg_intersect(array(tuple(curr_point)),array(tuple(dest_point)),array(tuple(point)),array(tuple(test_point)))
			intersect_result = list(intersect_result)
			new_distance = find_distance(point[0], point[1], intersect_result[0], intersect_result[1])
			if new_distance > distance:
				furthest_point, distance, move_angle = point, new_distance, m_angle
				
	return furthest_point, distance, move_angle
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	