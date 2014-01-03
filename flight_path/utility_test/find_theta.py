from math import atan2, pi, sin, cos

def find_theta(oe, on, ne, nn): #Origin Easting and Northing, New Easting and Northing
	## find easting and northing distance
	delta_e = ne - oe #adjacent line
	delta_n = nn - on #opposite line
	
	## tan(theta) = opposite / adjacent (TOA), flip the tangent to the other side
	theta = atan2(delta_n,delta_e)
	
	return theta
	
def find_next_ne(ox, oy, distance, angle):
	## find the amount of distance travel horizontally
	## cos(angle) = adjacent / hypotenuse, which would become cos(angle) * hypotenuse = adjacent
	delta_x = cos(angle) * distance
	
	## sin(angle) = opposite / hypotenuse, which would become sin(angle) * hypotenuse = opposite
	delta_y = sin(angle) * distance
	
	## now create the next x and y coordinates
	nx = ox + delta_x; ny = oy + delta_y
	
	return [nx, ny]