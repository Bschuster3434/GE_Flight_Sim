import numpy as np
import math
import csv
import shapely.geometry
import pandas as pd


def find_theta(oe, on, ne, nn): #Origin Easting and Northing, New Easting and Northing
	## find easting and northing distance
	delta_e = ne - oe #adjacent line
	delta_n = nn - on #opposite line
	
	## tan(theta) = opposite / adjacent (TOA), flip the tangent to the other side
	theta = math.atan2(delta_n,delta_e)
	
	return theta
	
def find_next_ne(ox, oy, distance, angle):
	## find the amount of distance travel horizontally
	## cos(angle) = adjacent / hypotenuse, which would become cos(angle) * hypotenuse = adjacent
	delta_x = math.cos(angle) * distance
	
	## sin(angle) = opposite / hypotenuse, which would become sin(angle) * hypotenuse = opposite
	delta_y = math.sin(angle) * distance
	
	## now create the next x and y coordinates
	nx = ox + delta_x; ny = oy + delta_y
	
	return [nx, ny]

def find_distance(oe, on, ne, nn):
	delta_e = ne - oe
	delta_n = nn - on
	
	distance = math.sqrt(delta_e**2 + delta_n**2)
	return distance
	
def haversine(lat1, lon1, lat2, lon2):
	lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
	
	
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
	c = 2 * math.asin(sqrt(a))
	
	miles = c * 3963.1676
	return miles
	
reflat = 25.0
reflon = 265.0
stanpar = 25.0
earthrad = 3440.189697153

def radianstodegrees(radians):
    return (radians * 180.0 / np.pi)

def degreestoradians(degrees):
    return (degrees * np.pi / 180.0)

def boundangle(angle):
    multiple = math.floor((angle + 180.0) / 360.0)
    result = angle - multiple * 360.0
    return result

def adjustangle(angle):
    quarterpi = 0.25 * np.pi 
    return (0.5 * angle + quarterpi)

def inverseadjustangle(adjustedangle):
    return ((adjustedangle - 0.25 * np.pi) * 2.0)

def toeastingnorthing(n, rho, rho0, reflon, lon):
    theta = n * (degreestoradians(boundangle(lon)) - degreestoradians(boundangle(reflon)))
    easting = rho * math.sin(theta) * earthrad
    northing = (rho0 - rho * math.cos(theta)) * earthrad
    return (easting, northing)

def calculaten():
    sp1 = degreestoradians(stanpar)
    result = math.sin(sp1)
    return result

def calculaterho(n, lat):
    sp1 = degreestoradians(stanpar)
    angle = degreestoradians(lat)
    result = ((math.tan(adjustangle(sp1)) / math.tan(adjustangle(angle)))**n) * math.cos(sp1) / n
    return result

def inverserho(n, rho):
    sp1 = degreestoradians(stanpar)
    tanangle = math.tan(adjustangle(sp1)) / ((rho * n / math.cos(sp1))**(1.0 / n))
    result = radianstodegrees(inverseadjustangle(math.atan(tanangle))) 
    return result

def tolambert(lat, lon):
    n = calculaten()
    rho = calculaterho(n, lat)
    rho0 = calculaterho(n, reflat)
    result = toeastingnorthing(n, rho, rho0, reflon, lon)
    return result
    
def fromlambert(easting, northing):
    n = calculaten()
    rho0 = calculaterho(n, reflat)
    conorthing = rho0 - northing / earthrad
    scaledeasting = easting / earthrad
    theta = math.atan(scaledeasting / conorthing)
    if n < 0:
        signofn = -1.0 
    elif n == 0:  
        signofn = 0.0 
    else:
        signofn = 1.0 
        
    rho = math.sqrt(scaledeasting * scaledeasting + conorthing*conorthing) * signofn
    lat = inverserho(n, rho)
    lon = reflon + radianstodegrees(theta / n)
    if lon > 180:
        lon = lon - 360

    return [lat, lon]

def get_airport_coordinates(file):
	airports_ne = {} ##Airports Northing Easting Dictionary
	with open(file, 'rb') as csv_airports:
		reader = csv.reader(csv_airports, delimiter=',')
		next(reader, None)
		for row in reader: #skips the first row
			airports_ne[row[0]] = [float(row[1]), float(row[2])] #Easting, Northing
	return airports_ne

def get_flight_info(file):
	flight_list = [] ##[flightid, arrival airport, [easting, northing]]
	with open(file, 'rb') as csv_flights:
		reader = csv.reader(csv_flights, delimiter=',')
		next(reader, None) # skips the headers
		check_testflight = file.find('TestFlights.csv') #Checks file to see if it's the TestFlight File
		if check_testflight == -1:
			for row in reader:
				flight_list.append([row[0], row[5], [float(row[1]), float(row[2])]])
		else: 
			for row in reader:
				lon = float(row[5]); lat = float(row[4]) 
				e_n_con = tolambert(lat, lon) #Need to covert X,Y into Easting Northing
				flight_list.append([row[0], row[2], e_n_con])
				
	return flight_list
	
def create_coordinate_pairing(a_file, f_file):
	current_dest_pairings = [] ##[FlightId, [current easting, current northing], [dest easting, dest northing]]
	
	airports = get_airport_coordinates(a_file)
	flights = get_flight_info(f_file)
	
	for i in flights:
		current_dest_pairings.append([i[0], i[2], airports[i[1]]])
	
	return current_dest_pairings

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
		

def create_nofly_polygons(verts):
	nofly_shapes = []
	lol_verts = create_ver_list(verts)
	for i in lol_verts:
		next_shape = shapely.geometry.Polygon(i)
		nofly_shapes.append(next_shape)
		
	return nofly_shapes
	
def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return 
def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot( dap, db)
    num = dot( dap, dp )
    return (num / denom)*db + b1
