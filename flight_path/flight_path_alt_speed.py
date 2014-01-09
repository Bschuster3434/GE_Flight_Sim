def flight_path_alt_speed(skeleton, cruise_speed, cruise_alt, descent_dis, descent_speed, descent_alt):

	flight_distance, dis_skel = find_flight_distance(skeleton) # returns the total flight distance and appends markers to points
	
	descent_mile_marker = flight_distance - flight_dis #Finds the descent point
	
	flight_alt_speed = find_ordinal_alt_speeds
	
	
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
		
		
def test_skeleton(choice):
	skel_0 = [[[877.597749, 886.747467], 0], [[940.2115511, 972.1340222], 0]]
	skel_1 = [[[795.440532, 731.693072], 0], [[948.305187486941, 826.765075099378], 0], [[940.2115511, 972.1340222], 0]]
	skel_2 = [[[-325.355417, 848.166215], 0], [[-461.565772, 919.3482914], 0]]
	skel_3 = [[[-893.849577, 824.797677], 0], [[-1079.2813676052604, 673.4267318563585], 0], [[-1081.352829, 618.2796063], 0]]
	skel_4 = [[[-1020.959393, 670.459519], 0], [[-840.6781118208097, 921.48486684559], 0], [[-801.4948792, 1010.875949], 0]]
	skel_5 = [[[-62.70846, 465.851781], 0], [[333.80062265024554, 325.20426877254835], 32000], [[339.477310268438, 323.1906654879663], 32000], [[661.0519947, 209.1234692], 0]]
	
	#basic points below
	
	skel_6 = [[[0, 0], 0], [[3, 0], 0], [[3, 10], 0]]
	skel_7 = [[[0, 0], 0], [[3, 0], 0], [[3,9], 0], [[3, 10], 0]]
	
	
	if choice == 1:
		return [skel_6, skel_7]
		
	else:
		return [skel_0, skel_1, skel_2, skel_3, skel_4, skel_5]
	
	
	
	

	