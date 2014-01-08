# coding: utf-8
import csv
import numpy as np
import random
import os
import math
import shapely.geometry
import shapely.ops
import itertools
import matplotlib.pyplot as plt
import descartes


### Files to Execute
execfile('open_rz_csv.py')

file = 'restrictedZones.csv'

list = open_rz_csv(file)

fig = plt.figure()
ax = fig.add_subplot(111)
for i in list:
	
#	if int(i[2]) == 27000:
#		ax.add_patch(descartes.PolygonPatch(i[0], fc='green', alpha=0.5))
#	elif int(i[2]) == 32000:
#		ax.add_patch(descartes.PolygonPatch(i[0], fc='blue', alpha=0.5))
#	else:
#		ax.add_patch(descartes.PolygonPatch(i[0], fc='red', alpha=0.5))
 
	ax.add_patch(descartes.PolygonPatch(i[0], fc='green', alpha=0.5))
 
trouble_point = shapely.geometry.Point(-1099.2670119390168, 699.021217857).buffer(5)
airport = shapely.geometry.Point(-1326.334844, 898.4162716).buffer(5)
start = shapely.geometry.Point(-158.536965, 489.825944).buffer(5)

ax.add_patch(descartes.PolygonPatch(trouble_point, fc='red', alpha=0.5))
ax.add_patch(descartes.PolygonPatch(airport, fc='orange', alpha=0.5))
ax.add_patch(descartes.PolygonPatch(start, fc='blue', alpha=0.5))


 
ax.axis('equal')
plt.grid()
plt.show()
