### Modules to Import
import csv
import numpy as np
import random
import os
import math
import shapely.geometry
import shapely.ops
import itertools
from operator import itemgetter


### Files to Execute
execfile('lambert.py')
execfile('open_flight_csv.py')
execfile('open_rz_csv.py')
execfile('flight_path_skeleton_v2.py')
execfile('find_theta.py')
execfile('seg_intersect.py')
execfile('flight_path_alt_speed_v2.py')
execfile('create_ordinals_and_write_csv.py')

flights_csv = 'TestFlights.csv'
no_fly_csv = 'restrictedZones.csv'

flights = open_flight_csv(flights_csv)
no_fly = open_rz_csv(no_fly_csv)

for i in flights:
	if i[0] == '309708962':
		p_flight = [i]
		break

for i in p_flight:
	id = i[0]
	curr = i[1]
	dest = i[2]
	
	line = shapely.geometry.LineString([curr, dest])
	
	zone = test_intersect(no_fly, line, curr, dest)
	
	ve = find_visible_edges(curr, zone[0], zone[1])
	
	skeleton = flight_path_skeleton_v2(i, no_fly)
	

	



