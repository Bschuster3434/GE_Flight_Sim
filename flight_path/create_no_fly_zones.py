import shapely.geometry
import pandas as pd

def create_ver_list(en): #Takes a list of strings with vertices and transforms them into a list of list or list, with each sublist being a vertice.
	delimit = " " #A space divides each vertice.
	lol_verts = []
	for verts in en:
		ind_vert = []
		next_start = 0
		while next_start >= 0: #the find function used here will return a '-1' when delimiter is not found
			next_end = verts[next_start:].find(delimit)
			if next_end == -1:
				string_vertice = verts[next_start:]
			else:
				string_vertice = verts[next_start:next_start + next_end]
			list_vertice = create_vert_point_list(string_vertice)
			ind_vert.append(list_vertice)
			if next_end == -1:
				next_start = next_end
			else:
				next_start = next_start + next_end + 1
		lol_verts.append(ind_vert) #append individual polygon of verts to the 'List of Lists' vertice list
	return lol_verts
				
			
def create_vert_point_list(str_vert):
	delimit = ":"
	delimit_point = str_vert.find(delimit)
	x_coor = float(str_vert[0:delimit_point])
	y_coor = float(str_vert[delimit_point + 1:])
	return [x_coor, y_coor]
		

def create_nofly_polygons(en_verts):
	nofly_shapes = []
	lol_verts = create_ver_list(en_verts)
	for i in lol_verts:
		next_shape = shapely.geometry.Polygon(i)
		nofly_shapes.append([next_shape, i])
		
	return nofly_shapes
	
def test_intersect(no_flys, line, altitude):
	for zone in no_flys:
		if line.intersects(zone[0]) == True and zone[2] > altitude:
			return zone
	return False