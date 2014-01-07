# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry
import descartes
import csv
import itertools

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
