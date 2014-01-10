def flight_path_skeleton_v2(flight, no_fly):
	destination = [flight[2], 0.0]

	test_start_point = find_next_ne_angle(flight[1][0], flight[1][1], 0, .01)
	next_line = shapely.geometry.LineString([flight[1], test_start_point])
	intersect_test = test_intersect(no_fly, next_line, flight[1], destination[0][0])	
	
	if intersect_test == False:
		next_start = [flight[1], 0.0]
	else:
		next_start = [flight[1], float(intersect_test[2])]
	
	weather_27000 = no_fly[0]
	weather_32000 = no_fly[1]
	weather_zones = [weather_27000, weather_32000]
	
	skeleton = [next_start]
	rz_notes = [] ## Test if flying over no_fly_zone. [[<ordinal_over_zone>,<Upper_Bound>]]
	
	intersect_cross = .5 
	
	counter = 0
	
	while skeleton[-1] != destination:
		next_line = shapely.geometry.LineString([next_start[0], destination[0]])
		intersect_test = test_intersect(no_fly, next_line, next_start[0], destination[0])
		bound = 0.0
		if intersect_test == False:
			skeleton.append(destination)
		elif intersect_test in weather_zones:
			bound = float(intersect_test[2])
			next_point = find_closests_intersect(next_start[0], destination[0], intersect_test, intersect_cross)
			skeleton.append([next_point, bound])
			next_start = [next_point, bound]
		else:
			next_point = avoidance(next_start[0], destination[0], intersect_test, no_fly)
			skeleton.append([next_point, bound])
			next_start = [next_point, bound]
			
		counter = counter + 1
		
		if counter > 20:
			print "overflow error: " + flight[0]
			skeleton.append(destination)
			break
		
	return skeleton ## List of ordinals that will accurately avoid no_fly zones
	

def test_intersect(no_fly, line, curr, dest):
	
	sub_no_fly_zone = []
	
	for zone in no_fly:
		if line.intersects(zone[0]) == True:
			sub_no_fly_zone.append(zone)
	
	if len(sub_no_fly_zone) == 0:
		return False
	elif len(sub_no_fly_zone) == 1:
		return sub_no_fly_zone[0]
	else:
	
		distance = find_distance(curr[0], curr[1], dest[0], dest[1])
		
		distance_divider = 100
		
		angle = find_theta(curr[0], curr[1], dest[0], dest[1])
		
		for i in range(1, distance_divider + 1):
			next_distance = distance * (i/distance_divider)
			test_point = find_next_ne_angle(curr[0], curr[1], angle, next_distance)
			
			test_line = shapely.geometry.LineString([curr, test_point])
			
			result = test_intersect_brief(sub_no_fly_zone, test_line)
			
			if result != False:
				return result
		
		
def test_intersect_brief(no_fly, line):
	
	sub_no_fly_zone = []
	
	for zone in no_fly:
		if line.intersects(zone[0]) == True:
			sub_no_fly_zone.append(zone)
	
	if len(sub_no_fly_zone) == 0:
		return False
	else:
		return sub_no_fly_zone[0]
			
def intersection_point(line, zone, curr_point, dest_point, d_or_p ): #if 1, d, if 0, p
	zone_polygon = zone[0]
	line = shapely.geometry.LineString([curr_point, dest_point])
	intersect_seg = line.intersection(zone_polygon)
	try:
		intersect_point = list(intersect_seg.coords[0])
	except NotImplementedError:
		intersect_point = list(intersect_seg[0].coords[0])
	dist_to_intersect = find_distance(curr_point[0], curr_point[1], intersect_point[0], intersect_point[1])
	
	if d_or_p == 1:
		return dist_to_intersect
	elif d_or_p == 0:
		return intersect_point
	
	
	
def avoidance(curr_point, dest_point, zone, no_fly): ##[restricted zone polygon, restricted zone points, restricted zone upper bound]
	polygon = zone[0]
	edge_points = zone[1]
	
	visible_edges = find_visible_edges(curr_point, polygon, edge_points)
	next_start = decide_furthest_point(curr_point, dest_point, visible_edges, zone, no_fly)
	
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
	
	for edge in edge_points:
		distance = find_distance(curr_point[0], curr_point[1], edge[0], edge[1])
		angle = find_theta(curr_point[0], curr_point[1], edge[0], edge[1])
		test_dis = distance * diminish_line
		test_point = find_next_ne_angle(curr_point[0], curr_point[1], angle, test_dis)
		test_line = shapely.geometry.LineString([[curr_point[0], curr_point[1]], [test_point[0], test_point[1]]])
		result = test_line.intersects(polygon)
		if result == False:
			visible.append(edge)
			
	return visible
		

def decide_furthest_point(curr, dest, ve, zone, no_fly):

	dest_angle = find_theta(curr[0], curr[1], dest[0], dest[1]) + (2 * math.pi)
	
	ve_point_radials = []
	
	for i in ve:
		ve_angle = find_theta(curr[0], curr[1], i[0], i[1]) + (2 * math.pi)
		ve_difference = dest_angle - ve_angle
		ve_point_radials.append([i, ve_difference])
		## Angles to the right will be positive, Angles to the left will be negatve
		
	sorted_ve_points = sorted(ve_point_radials, key = itemgetter(1))
	
	left_pivot = sorted_ve_points[0][0]
	left_point = find_pivot_point(curr, left_pivot, 1); to_left_point = shapely.geometry.LineString([curr, left_point])
	dest_to_left_through_nofly = test_intersect_brief(no_fly, to_left_point)
	
	right_pivot = sorted_ve_points[-1][0]
	right_point = find_pivot_point(curr, right_pivot, 0); to_right_point = shapely.geometry.LineString([curr, right_point])
	dest_to_right_through_nofly = test_intersect_brief(no_fly, to_right_point)
	
	if dest_to_right_through_nofly != False and dest_to_left_through_nofly != False:
		line_to_dest = shapely.geometry.LineString([curr, dest])
		intersect_distance = intersection_point(line_to_dest, zone, curr, dest, 1)
		half_i_dist = intersect_distance /2
		
		next_point = find_next_ne_twopoints(curr[0], curr[1], dest[0], dest[1], half_i_dist)
		
		return next_point
		
	
	elif dest_to_right_through_nofly != False:
		return left_point
		
	elif dest_to_left_through_nofly !=False:
		return right_point
		
	else:
		right_to_dest = shapely.geometry.LineString([curr, right_point, dest]); 
		left_to_dest = shapely.geometry.LineString([curr, left_point, dest]); 
		
		if right_to_dest.length > left_to_dest.length:
			return right_point
		else:
			return left_point
		

def find_pivot_point(curr, point, l_or_r): #left is one, right is zero
	
	angle_to_point = find_theta(curr[0], curr[1], point[0], point[1])
	
	if l_or_r == 1:
		pivot_angle = + (math.pi)/2
	elif l_or_r == 0:
		pivot_angle = (math.pi)/2
		
	new_angle = angle_to_point + pivot_angle
	
	buffer = 7
	
	new_point = find_next_ne_angle(point[0], point[1], new_angle, buffer)
	
	point, new_point
	
	return new_point
	
	
		
	
	
	
	
	
	
	
	