# coding: utf-8
import shapely.geometry
flight = [1, [0,0], [-8,-8]]
block1 = shapely.geometry.LineString([[-2, -2], [-4, -2], [-4,-4], [-2,-4]])
block2 = shapely.geometry.LineString([[-2, -4], [-2, -8], [-3,-8], [-3,-4]])
points1 = [[-2,-2],[-4,-2],[-4,-4],[-2,-4]]
points2 = [[-2,-4],[-2,-8],[-3,-8],[-3,-4]]
no_fly = [[block1, points1], [block2, points2]]
