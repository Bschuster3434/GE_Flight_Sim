# coding: utf-8
import csv
import numpy as np
import random
import os
import math
import shapely.geometry
import shapely.ops
import itertools


### Files to Execute
execfile('open_rz_csv.py')
execfile('flight_path.skeleton.py')
execfile('open_rz_csv.py')

file = 'restrictedZones.csv'

list = open_rz_csv(file)

fig = plt.figure()
ax = fig.add_subplot(111)
for i in list:
    ax.add_patch(descartes.PolygonPatch(i[0], fc='green', alpha=0.5))
    
ax.axis('equal')
plt.grid()
plt.show()
