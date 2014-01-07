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
	
	if int(i[2]) == 27000:
		ax.add_patch(descartes.PolygonPatch(i[0], fc='green', alpha=0.5))
	elif int(i[2]) == 32000:
		ax.add_patch(descartes.PolygonPatch(i[0], fc='blue', alpha=0.5))
	else:
		ax.add_patch(descartes.PolygonPatch(i[0], fc='red', alpha=0.5))
    
ax.axis('equal')
plt.grid()
plt.show()
