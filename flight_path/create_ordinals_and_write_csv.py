def create_ordinals_and_write_csv(ordinals, flights):
	## Output is csv with the following: [flightid, ordianl, latitude, longitude, altitude, airspeed]
	
	all_ordinals = [['FlightId','Ordinal','Latitude','Longitude','Altitude','Airspeed']]
	
	num_of_flights = len(flights)
	
	for i in range(0, num_of_flights):
		f = flights[i]
		o = ordinals[i]
		
		id = f[0]
		ordinal = 1
		
		### all points need to be converted using this :fromlambert(easting, northing) - output [x, y]
		
		for point_pack in o[1:]:
			ne_point = point_pack[0]
			altitude = point_pack[1]
			speed = point_pack[2]
			
			xy_point = fromlambert(ne_point[0], ne_point[1])
			
			next_ordianl = [id, ordinal, xy_point[0], xy_point[1], altitude, speed]
			
			ordinal = ordinal + 1
			all_ordinals.append(next_ordianl)
			
	with open('todays_flights.csv', 'wb') as write_file:
		flight_writer = csv.writer(write_file, delimiter=',')
		for i in all_ordinals:
			flight_writer.writerow(i)
	
	
			
			
		
		
	
	
	
	
	
def test_ords():
	one = [[[877.597749, 886.747467], 34000, 425], [[881.077030314761, 891.4921692233964], 34000, 425], [[940.2115511, 972.1340222], 17990, 250]]
	two = [[[795.440532, 731.693072], 34000, 425], [[948.305187486941, 826.765075099378], 34000, 425], [[945.7705931170071, 872.2886564995673], 34000, 425], [[940.2115511, 972.1340222], 17990, 250]]
	three = [[[-893.849577, 824.797677], 34000, 425], [[-1044.5655349154156, 701.7658229504897], 34000, 425], [[-1079.2813676052604,673.4267318563585], 26825.281230481356, 250], [[-1081.352829, 618.2796063], 17990, 250]]
	four = [[[-1020.959393, 670.459519], 34000, 425], [[-842.0771150579299, 919.5368816086417], 34000, 425], [[-840.6781118208097,921.48486684559], 33616.031714365105, 250], [[-801.4948792, 1010.875949], 17990, 250]]
	five = [[[-62.70846, 465.851781], 34000, 425], [[333.80062265024554, 325.20426877254835], 34000, 425], [[339.477310268438, 323.1906654879663], 34000, 425], [[566.8055307376619, 242.55405445655393], 34000, 425], [[661.0519947, 209.1234692], 17990,250]]
	
	
	ordinals = [one, two, three, four, five]
	
	f_1 = ['308567953', [-239.001069, 381.916596], [-14.60777576, 279.2220579], 37000.0, 14758.8]
	f_2 = ['308567955', [251.819514, 686.545241], [842.6588783, 900.6587461], 31000.0, 19988.0]
	f_3 = ['308567956', [-354.180154, 454.629724], [-17.80256177, 299.6569477], 35000.0, 16133.8]
	f_4 = ['308567975', [-880.438361, 641.350407], [-1174.85114, 640.8135838], 38000.0, 15258.800000000001]
	f_5 = ['308567978', [-157.386281, 772.765061], [13.73253826, 867.8475026], 41000.0, 13050.4]
	
	flights = [f_1, f_2, f_3, f_4, f_5]
	
	return ordinals, flights