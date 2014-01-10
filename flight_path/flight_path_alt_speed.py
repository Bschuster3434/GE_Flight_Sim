def flight_path_alt_speed(skeleton, c_speed, c_alt, d_dis, d_speed, d_alt):


	flight_distance, dis_skel = find_flight_distance(skeleton) # returns the total flight distance and appends markers to points
	### Skeleton is now [<point>, bound, mile_marker]
	
	descent_mile_marker = flight_distance - d_dis #Finds the descent point
	
	skel_with_descent = find_descent_point(dis_skel, descent_mile_marker)
	#### Skeleton is now [<point>, bound, mile_marker, descent_binary]
	
	destination_pack = skel_with_descent[-1]
	
	flight_alt_speed = find_ordinal_alt_speed(skel_with_descent, destination_pack, d_dis, c_speed, c_alt, d_speed, d_alt)
	
	return flight_alt_speed
	
	
	
def find_flight_distance(old_skeleton):
	skeleton = []
	for i in old_skeleton:
		skeleton.append(i)
		
	flight_turns = len(skeleton) - 1
	distance = 0
	
	skeleton[0].append(0)
	for i in range(0, flight_turns):
		###skeleton[i] is the [point, bound], [0] is point, [0][0] is x, [0][1] is y
		distance = distance + find_distance(skeleton[i][0][0], skeleton[i][0][1], skeleton[i + 1][0][0], skeleton[i + 1][0][1])
		skeleton[i + 1].append(distance) #Appends current distance to the skeleton
		
	return distance, skeleton

def find_descent_point(dis_skel, marker): #Adds 1 to the descent point
	
	marked_skel = []
	
	list_length = len(dis_skel)
	
	for i in range(0, list_length - 1): ## -1 because we don't want to check the final point
		curr_pack = dis_skel[i]
		next_pack = dis_skel[i+1]
		
		curr_dis = curr_pack[2]
		next_dis = next_pack[2]
		
		marked_skel.append([curr_pack[0], curr_pack[1], curr_pack[2], 0])
		
		if marker > curr_dis and marker < next_dis:
			distance_to_marker = marker - curr_dis
			angle = find_theta(curr_pack[0][0], curr_pack[0][1], next_pack[0][0], next_pack[0][1])
			descent_point = find_next_ne_angle(curr_pack[0][0], curr_pack[0][1], angle, distance_to_marker)
			
			marked_skel.append([descent_point, curr_pack[1], curr_pack[2], 1])
			
		elif marker < 0:
			
			marked_skel.append([curr_pack[0], curr_pack[1], curr_pack[2], 1])

	final_pack = dis_skel[-1]
	marked_skel.append([final_pack[0], final_pack[1], final_pack[2], 0])
			
	return marked_skel

	
def find_ordinal_alt_speed(skeleton, destination_pack, d_dis, c_speed, c_alt, d_speed, d_alt):
	ordinal_list = []
	
	dest_point = destination_pack[0]
	dest_mile_marker = destination_pack[2]
	
	
	in_descent = 0
	
	for ordinal in skeleton:
		point = ordinal[0]
		lower_bound = ordinal[1]
		mile_marker = ordinal[2]
		descent_binary = ordinal[3]
			
		if in_descent == 0 and c_alt > lower_bound:
			ordinal_list.append([point, c_alt, c_speed])
		elif in_descent == 0 and c_alt < lower_bound:
			ordinal_list.append([point, lower_bound + 500, c_speed])
		elif point != dest_point:
			current_distanct_to_dest = dest_mile_marker - mile_marker
			altitude_percent = current_distanct_to_dest / d_dis
			altitude_difference_cd = c_alt - d_alt
			current_altitude = (altitude_percent * altitude_difference_cd ) + d_alt
			ordinal_list.append([point, current_altitude, d_speed])
		elif point == dest_point:
			ordinal_list.append([point, d_alt, d_speed])
		else:
			raise Exception("Something Fucked Up")
			
			
		if descent_binary == 1:
			in_descent = 1
			
	return ordinal_list
			
		
def test_skeleton(choice):
	skel_0 = [[[877.597749, 886.747467], 0], [[940.2115511, 972.1340222], 0]]
	skel_1 = [[[795.440532, 731.693072], 0], [[948.305187486941, 826.765075099378], 0], [[940.2115511, 972.1340222], 0]]
	skel_2 = [[[-325.355417, 848.166215], 0], [[-461.565772, 919.3482914], 0]]
	skel_3 = [[[-893.849577, 824.797677], 0], [[-1079.2813676052604, 673.4267318563585], 0], [[-1081.352829, 618.2796063], 0]]
	skel_4 = [[[-1020.959393, 670.459519], 0], [[-840.6781118208097, 921.48486684559], 0], [[-801.4948792, 1010.875949], 0]]
	skel_5 = [[[-62.70846, 465.851781], 0], [[333.80062265024554, 325.20426877254835], 32000], [[339.477310268438, 323.1906654879663], 32000], [[661.0519947, 209.1234692], 0]]
	
	#basic points below
	
	skel_6 = [[[0.0, 0.0], 0], [[3.0, 0.0], 0], [[3.0, 10.0], 0]]
	skel_7 = [[[0.0, 0.0], 0], [[3.0, 0.0], 0], [[3.0, 9.0], 0], [[3.0, 10.0], 0]]
	
	
	if choice == 1:
		return [skel_6, skel_7]
		
	elif choice == 0:
		return [skel_0, skel_1, skel_2, skel_3, skel_4, skel_5]
	
	
	
	

	