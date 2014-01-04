import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry
import descartes
import math
import itertools
from datetime import datetime

startTime = datetime.now()

no_fly1 = shapely.geometry.Polygon([[2,2], [3,2], [3,4], [2,4]])
no_fly2 = shapely.geometry.Polygon([[3,2], [4,2], [4,4], [3,4]])

no_fly_list = [no_fly1, no_fly2]

start = [0, 0]
end = [3000,1500]
flight_id = 1

def create_ordinals(start, end):
	line_segment = shapely.geometry.LineString([start, end])
	int_test = test_intersect(no_fly_list, line_segment)
	if int_test == False:
		return[end]
	else:
		avoid_point = find_short_avoidance(start, end)
		return [avoid_point, end]	
		
def test_intersect(no_fly_list, line):
	for zone in no_fly_list:
		if line.intersects(zone) == True:
			return True
	return False
	
def find_short_avoidance(start, end):
	x_zone = end[0] - start[0]
	y_zone = end[1] - start[1]
	
	x_list = list(range(start[0], start[0] + x_zone + 1))
	y_list = list(range(start[1], start[1] + y_zone +1))
	
	process_list = [x_list, y_list]
	tuple_list = list(itertools.product(*process_list))
	
	min_avoidance = [[0,0], 10000]
	for i in tuple_list:
		i = list(i)
		if i == start or i == end:
			continue
		else:
			test_line = shapely.geometry.LineString([start, i, end])
			if test_intersect(no_fly_list, test_line) == True:
				continue
			else:
				dist = distance(end, i)
				dist = dist + distance(start, i)
				if dist < min_avoidance[1]:
					min_avoidance = [i, dist]
					
	return min_avoidance[0]

def distance(end_point, test_point):
	x = math.fabs(end_point[0] - test_point[0])
	y = math.fabs(end_point[1] - test_point[1])
	distance = math.sqrt(x**2 + y**2)
	return distance
	
print create_ordinals(start, end)
print(datetime.now()-startTime)
	

					
		
	
	