# coding: utf-8
file = 'flights_20130910_1803.csv'
flights = open_flight_csv(file)
nofly_csv = 'restrictedZones.csv'
no_fly = open_rz_csv(nofly_csv)
