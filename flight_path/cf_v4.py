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
execfile('flight_path_alt_speed.py')
execfile('create_ordinals_and_write_csv.py')

flights_csv = 'flights_20130910_1803.csv'
no_fly_csv = 'restrictedZones.csv'

flights = open_flight_csv(flights_csv)
no_fly = open_rz_csv(no_fly_csv)

all_ordinals = []

for flight in flights:
	skeleton = flight_path_skeleton_v2(flight, no_fly)
	ordinals = flight_path_alt_speed(skeleton, 600, 32001, 90, 250, 17790)
	all_ordinals.append(ordinals)

create_ordinals_and_write_csv(all_ordinals, flights)

