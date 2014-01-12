import csv
import itertools
from operator import itemgetter
from copy import deepcopy

class Variable_Testing:
	
	def __init__(self, start_file, start_altitude = [32000], cruise_speed = [475], cruise_altitude = [32000], descent_distance = [100], descent_speed = [475], descent_altitude = [17990]):
		self.s_f = start_file
		self.s_a = start_altitude
		self.c_s = cruise_speed
		self.c_a = cruise_altitude
		self.d_d = descent_distance
		self.d_s = descent_speed
		self.d_a = descent_altitude
		
		self.variation_list = [ self.s_a, self.c_s, self.c_a, self.d_d, self.d_s, self.d_a]
		
	def create_testing_flights_file(self):
	
		total_variations = self.count_variations( self.variation_list )
		
		flight_base = []
		
		with open(self.s_f) as csv_flights:
			reader = csv.reader(csv_flights, delimiter=',')
			flights_header = next(reader, None)
			for i in reader:
				flight_base.append(i)
		
		for x in flight_base:
			del x[3]
			
		total_flight_variations = self.extend_flight_base(flight_base, total_variations, self.s_a)
		
		#return total_flight_variations
		return flight_base
		
	def extend_flight_base(self, base, variations_count, start_alt):
		
		i_b = base * len(start_alt)
		i_b = sorted(i_b, key=itemgetter(3))
		
		iter_base = []
		
		for i in i_b:
			copy = deepcopy(i)
			iter_base.append(copy)
		
		base_list = []
		
		base_list = base_list * (variations_count / len(start_alt))
		base_list = sorted(base_list, key=itemgetter(3))
		
		return iter_base
	
	
	def count_variations( self, list_or_string ):
		
		variations = 1
		for i in list_or_string:
			variations = variations * len(i)
				
		return variations
	
			
		