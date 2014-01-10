def open_rz_csv(file):
	restricted_zones = [] ##[restricted zone polygon, restricted zone points, restricted zone upper bound]
	
	r_verts = []
	with open(file) as csv_rz:
		reader = csv.reader(csv_rz, delimiter=',')
		next(reader, None)
		for row in reader:
			ne_vert_string = row[4]
			upper_bound = row[2]
			vert_list = seperate_verts(ne_vert_string)
			r_verts.append([vert_list, upper_bound])
			
	matched_zones = match_zones(r_verts)
	
	polygon_array = create_polygon_array(matched_zones)
	
	return polygon_array
	
			
def seperate_verts(string):
	delimit = " "
	list_of_verts = []
	next_start = 0
	while next_start >= 0:
		next_end = string[next_start:].find(delimit)
		if next_end == -1:
			vertice = string[next_start:]
		else:
			vertice = string[next_start:next_start + next_end]
		list_of_verts.append(vertice)
		if next_end == -1:
			next_start = next_end
		else:
			next_start = next_start + next_end + 1
	return list_of_verts
	
def match_zones(list):
	potential = [] 
	
	number_of_zones = len(list) - 1
	
	matched = 0
	for row in range(0, number_of_zones):
		if matched == 1:
			matched = 0
			continue
		else:
			current_row = list[row]
			next_row = list[row + 1]
			
			current_upper = current_row[1]
			next_row_upper = next_row[1]
			
			if current_upper != next_row_upper:
				potential.append([[current_row[0]], current_row[1]])
			else:
				test_lines = check_line_match(current_row[0], next_row[0])
				if test_lines == True:
					matched = 1
					potential.append([[current_row[0], next_row[0]], current_upper])
				else:
					potential.append([[current_row[0]], current_row[1]])
					
	return potential
	
	
def check_line_match(current_row, next_row):
	points_list = [current_row, next_row]
	coor_list = list(itertools.product(*points_list))
	for e in coor_list:
		i = list(e)
		line_1 = i[0]
		line_2 = i[1]
		if line_1 == line_2:
			return True
		
	return False
	
def create_polygon_array(zoz):
	result = []
	
	for matched_zones in zoz:
		zones = matched_zones[0]
		bound = matched_zones[1]

		if len(zones) == 1:
			zones = seperate_points(zones[0])
			polygon = create_shape(zones)
		else:
			zones_1 = seperate_points(zones[0])
			zones_2 = seperate_points(zones[1])
			polygon_1 = create_shape(zones_1)
			polygon_2 = create_shape(zones_2)
			poly_list = [polygon_1 , polygon_2]
			polygon = shapely.ops.cascaded_union(poly_list)
			zones = extract_points(polygon)
		
		result.append([polygon, zones, bound])
	return result
		
def create_shape(zones):
	trans_zones = []
	for i in zones:
		trans_zones.append(i)
	shape = shapely.geometry.Polygon(trans_zones)
	return shape
		
def seperate_points(list):
	points = []
	delimit = ":"	
	for string in list:

		delimit_point = string.find(delimit)
		x_coor = float(string[0:delimit_point])
		y_coor = float(string[delimit_point + 1:])
		points.append([x_coor, y_coor])
		
	return points

def extract_points(polygon):
	new_points = []
	
	x_points, y_points = polygon.exterior.coords.xy
	x_list = list(x_points)
	y_list = list(y_points)
	
	length = len(x_list)
	
	for i in range(0, length):
		new_points.append([x_list[i], y_list[i]])
	
	return new_points
	
		
	
	
	
	
	
	
	
	
	
	