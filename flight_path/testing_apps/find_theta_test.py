from math import atan2, pi, sin, cos
import shapely.geometry
import descartes
import matplotlib.pyplot as plt
import numpy as np

origin = [-579.128, 630.815]

rp1 = [-600, 650] # Upper Left
rp2 = [500, 630.815] #Directly Right
rp3 = [-400, 600] #Bottom Right
rp4 = [-550, 650] #Upper Right

### Need to find the angle theta, given two non-hypotenuse sides

def find_theta(oe, on, ne, nn): #Origin Easting and Northing, New Easting and Northing
	## find easting and northing distance
	delta_e = ne - oe #adjacent line
	delta_n = nn - on #opposite line
	
	## tan(theta) = opposite / adjacent (TOA), flip the tangent to the other side
	theta = atan2(delta_n,delta_e)
	
	return theta
	
def create_test_line(ox, oy, distance, angle):
	## find the amount of distance travel horizontally
	## cos(angle) = adjacent / hypotenuse, which would become cos(angle) * hypotenuse = adjacent
	delta_x = cos(angle) * distance
	
	## sin(angle) = opposite / hypotenuse, which would become sin(angle) * hypotenuse = opposite
	delta_y = sin(angle) * distance
	
	## now create the next x and y coordinates
	nx = ox + delta_x; ny = oy + delta_y
	
	### Use shapely to create a test line segment
	test_line = shapely.geometry.LineString([[ox, oy], [nx, ny]])
	
	return test_line
	
def create_original_line(ox, oy, nx, ny):
	line = shapely.geometry.LineString([[ox, oy], [nx,ny]])
	return line
	
line_1 = create_original_line(origin[0], origin[1], rp2[0], rp2[1])
angle = find_theta(origin[0], origin[1], rp2[0], rp2[1])
line_2 = create_test_line(origin[0], origin[1], 20, angle)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(*np.array(line_1).T, color='blue', linewidth=3, solid_capstyle='round')
ax.plot(*np.array(line_2).T, color='green', linewidth=3, solid_capstyle='round')
ax.axis('equal')

plt.show()
	

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
	