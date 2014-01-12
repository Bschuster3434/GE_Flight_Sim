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

all_ordinals = []

for flight in flights:
	skeleton = flight_path_skeleton_v2(flight, no_fly)
	o_obj = Flight_PAS(skeleton, c_speed = 500, d_speed = 500 )
	ordinals = o_obj.flight_path_alt_speed()
	all_ordinals.append(ordinals)

create_ordinals_and_write_csv(all_ordinals, flights)

