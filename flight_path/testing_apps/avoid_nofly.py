import shapely.geometry
import pandas as pd

rz = pd.read_csv('restrictedZones.csv')
latlong = list(rz['LatLongVertices']) #Vertices in a list, with each string being a set of points

# The functions above capture all zones as if they are not altitude dependent
# Some of the zones are actually well below the flight zone, and might get in the way of an optimal solution

def create_ver_list(latlong): #Takes a list of strings with vertices and transforms them into a list of list or list, with each sublist being a vertice.
	delimit = " " #A space divides each vertice.
	lol_verts = []
	for verts in latlong:
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
		

def create_nofly_polygons():
	nofly_shapes = []
	lol_verts = create_ver_list(latlong)
	for i in lol_verts:
		next_shape = shapely.geometry.Polygon(i)
		nofly_shapes.append(next_shape)
		
	return nofly_shapes

## Example Geometry as a reference
#no_fly_1 = shapely.geometry.Polygon([[1,5], [3,5], [3,7], [1,7]])
#no_fly_2 = shapely.geometry.Polygon([[5,1], [8,1], [8,3], [5,3]])
#no_fly = [no_fly_1, no_fly_2]

#line1 = shapely.geometry.LineString([[0,0], [10,10]])
#line2 = shapely.geometry.LineString([[0,0], [8,3]])

#def intersects(line):
	#intersects = False
	#for zone in no_fly:
	#	if line.intersects(zone) == True:
	#		intersects = True
	#		break
	#return intersects

#print "line1 intersects: " + str(intersects(line1))
#print "line2 intersects: " + str(intersects(line2))