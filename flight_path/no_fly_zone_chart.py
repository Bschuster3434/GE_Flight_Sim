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

execfile('lambert.py')
execfile('open_flight_csv.py')
execfile('open_rz_csv.py')
execfile('flight_path_skeleton.py')
execfile('find_theta.py')
execfile('seg_intersect.py')

### Files to Execute
def nfzc(curr, dest, tp, zone):

	execfile('open_rz_csv.py')

	file = 'restrictedZones.csv'

	#list = open_rz_csv(file)
	list = zone
	
	buffer = 5
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	for i in list:
	
#		if int(i[2]) == 27000:
#			ax.add_patch(descartes.PolygonPatch(i[0], fc='green', alpha=0.5))
#		elif int(i[2]) == 32000:
#			ax.add_patch(descartes.PolygonPatch(i[0], fc='blue', alpha=0.5))
#		else:
#			ax.add_patch(descartes.PolygonPatch(i[0], fc='red', alpha=0.5))
 
		ax.add_patch(descartes.PolygonPatch(i[0], fc='blue', alpha=0.5))
 
	trouble_point = shapely.geometry.Point(tp[0], tp[1]).buffer(buffer)
	airport = shapely.geometry.Point(dest[0], dest[1]).buffer(buffer)
	start = shapely.geometry.Point(curr[0], curr[1]).buffer(buffer)

	ax.add_patch(descartes.PolygonPatch(trouble_point, fc='red', alpha=0.5))
	ax.add_patch(descartes.PolygonPatch(airport, fc='black', alpha=0.5))
	ax.add_patch(descartes.PolygonPatch(start, fc='green', alpha=0.5))
	


 
	ax.axis('equal')
	plt.grid()
	plt.show()
