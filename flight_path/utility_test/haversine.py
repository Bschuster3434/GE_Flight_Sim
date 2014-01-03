from math import radians, degrees, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
	lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
	
	
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	
	miles = c * 3963.1676
	return miles
	