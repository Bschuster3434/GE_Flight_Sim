def flight_path_skeleton(flight, no_fly):
	destination = flight[2]
	next_start = flight[1]
	
	skeleton = [flight[1]]	
	
	while skeleton[-1] != destination:
		next_line = shapely.geometry.LineString(no_fly, [next_start, destination])
		intersect_test = test_intersect(no_fly, next_line):
			if False:
				skeleton.append(destination)
			else:
				next_start = avoidance(next_start, destination, intersect_test)
		
		
	return skeleton ## List of ordinals that will accurately avoid no_fly zones
	

def test_intersect(no_fly, line):
	for zone in no_fly:
		if line.intersects(zone[0]) == True:
			return zone
	return False
	
def avoidance(curr_point, dest_point, zone):
	