execfile('find_theta.py')
execfile('seg_intersect.py')
execfile('create_no_fly_zones.py')
import shapely.geometry
from math import pi, isnan

def avoid_nofly(flight, intersect_result, no_fly):
	zone_points = intersect_result[1] ##List of List of points that makeup the problem zone
	curr_point = flight[1]
	dest_point = flight[2]
	
	o_p1 = ( curr_point ) 
	o_p2 = ( dest_point )
	
	angle = find_theta(curr_point[0], curr_point[1], dest_point[0], dest_point[1])
	
	right_angle = math.pi/2
	
	right_point_angle = angle - right_angle
	right_avoidance_point = find_furthest_point(zone_points, right_point_angle, o_p1, o_p2)
	right_movement_angle = right_point_angle + math.pi
	right_ordinal_canidate = find_ordinal_point(right_avoidance_point, right_movement_angle, curr_point, dest_point, no_fly)
	
	
	left_point_angle = angle + right_angle
	left_avoidance_point = find_furthest_point(zone_points, left_point_angle, o_p1, o_p2)
	left_movement_angle = left_point_angle - math.pi
	left_ordinal_canidate = find_ordinal_point(left_avoidance_point, left_movement_angle, curr_point, dest_point, no_fly)

	if right_ordinal_canidate == 0 and left_ordinal_canidate == 0:
		return 0
	elif right_ordinal_canidate == 0:
		return left_ordinal_canidate
	elif left_ordinal_canidate ==0:
		return right_ordinal_canidate
	else:
		right_dist = multiline_distance(right_ordinal_canidate, curr_point, dest_point)
		left_dist = multiline_distance(left_ordinal_canidate, curr_point, dest_point)
		if right_dist > left_dist:
			return left_ordinal_canidate
		else:
			return right_ordinal_canidate
		

def find_furthest_point(zone_points, angle, o_p1, o_p2):
	avoidance_point = [[], 0]
	
	for i in zone_points:
		test_line_point = find_next_ne_angle(i[0], i[1], angle, 500)
		test_line_start = array( i )
		test_line_end = array(test_line_point)
		intersect_point = seg_intersect(array(o_p1),array(o_p2), array(test_line_start), array(test_line_end)).tolist()
		if math.isnan(intersect_point[0]) == False:
			distance = find_distance(i[0], i[1], intersect_point[0], intersect_point[1])
			if distance > avoidance_point[1]:
				avoidance_point = [intersect_point, distance]
				
	return avoidance_point[0]
	
def find_ordinal_point(avoidance_point, movement_angle, curr_point, dest_point, no_fly):
	end_test_distance = 100
	steps = 5
	distance_range = range(5, end_test_distance + 1, steps)
	
	for next_dis in distance_range:
		next_avoid_point = find_next_ne_angle(avoidance_point[0], avoidance_point[1], movement_angle, next_dis)
		test_line = shapely.geometry.LineString([curr_point, next_avoid_point, dest_point])
		intersection = test_intersect(no_fly, test_line, 100000)
		if intersection == False:
			return next_avoid_point
			
	return 0
	
def multiline_distance(candidate, curr_point, dest_point):
	distance = find_distance(candidate[0], candidate[1], dest_point[0], dest_point[1])
	distance = distance + find_distance(candidate[0], candidate[1], curr_point[0], curr_point[1])
	return distance


def find_new_points(curr_point, dest_point):
	curr_e = curr_point[0]
	curr_n = curr_point[1]
	dest_e = dest_point[0]
	dest_n = dest_point[1]
	
	distances = range(25, 500, 25) ##Amount choosen to move
	
	final_move_distance = math.pi #Final Movement Either Left or right, compared to straight to destination
	num_of_moves = 25
	move_distance = final_move_distance/num_of_moves
	
	dest_angle = find_theta(curr_e, curr_n, dest_e, dest_n)
	
	angle_movement_list = []
	for i in range(1, int(num_of_moves) +1):
		right = dest_angle + (i * move_distance); angle_movement_list.append(right)
		left = dest_angle - (i * move_distance); angle_movement_list.append(left)
	
	new_curr_points = []
	for angle in angle_movement_list:
		for distance in distances:
			next_point = find_next_ne_angle(curr_e, curr_n, angle, distance)
			new_curr_points.append(next_point)
	
	return new_curr_points	
		