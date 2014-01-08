### Modules to Import
import csv
import numpy as np
import random
import os
import math
import shapely.geometry
import shapely.ops
import itertools


### Files to Execute
execfile('lambert.py')
execfile('open_flight_csv.py')
execfile('open_rz_csv.py')
##execfile('flight_path_skeleton.py')
execfile('find_theta.py')
execfile('seg_intersect.py')

def find_visible_edges(curr_point, polygon, edge_points):
	visible = []
	diminish_line = .95
	
	### This is the best place to find the opposite angle
	
	edge_angles = calculate_all_opposite_angles(edge_points)
	
	for edge, angle in edge_points:
		distance = find_distance(curr_point[0], curr_point[1], edge[0], edge[1])
		angle = find_theta(curr_point[0], curr_point[1], edge[0], edge[1])
		test_dis = distance * diminish_line
		test_point = find_next_ne_angle(curr_point[0], curr_point[1], angle, test_dis)
		test_line = shapely.geometry.LineString([[curr_point[0], curr_point[1]], [test_point[0], test_point[1]]])
		result = test_line.intersects(polygon)
		if result == False:
			visible.append(edge)
			
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
		
		
		
		
		
		
			