# coding: utf-8
execfile('open_flight_csv.py')
execfile('open_rz_csv.py')
import csv
import numpy as np
import random
import os
import math
import shapely.geometry
import shapely.ops
import itertools


file = 'flights_20130910_1803.csv'
flights = open_flight_csv(file)
nofly_csv = 'restrictedZones.csv'
no_fly = open_rz_csv(nofly_csv)
