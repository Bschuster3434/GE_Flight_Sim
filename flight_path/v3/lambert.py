import numpy as np
import random
import os
import math

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

