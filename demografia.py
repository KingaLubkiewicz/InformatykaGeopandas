# -*- coding: utf-8 -*-
"""
Created on Tue May 11 20:01:34 2021

@author: Kinga
"""
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

gdf_w = gpd.read_file('PD_STAT_GRID_CELL_2011.shp')

gdf = gdf_w.to_crs("EPSG:4326")

wojew = gpd.read_file('Województwa.shp')

wojew['centroid']=wojew.centroid

#wojew.plot("TOT", legend=True)

import shapely

xmin, ymin, xmax, ymax = [13, 48, 25, 56]

n_cells = 30
cell_size = (xmax-xmin)/n_cells

grid_cells = []
for x0 in np.arange(xmin, xmax+cell_size, cell_size):
    for y0 in np.arange(ymin, ymax+cell_size, cell_size):
        x1 = x0 - cell_size
        y1 = y0 + cell_size
        grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))

cell = gpd.GeoDataFrame(grid_cells, columns=['geometry'])

# ax = gdf.plot(markersize = .1, figsize = (12,8), column = 'TOT', cmap='jet')

# plt.autoscale(False)
# cell.plot(ax=ax, facecolor="none", edgecolor='grey')
# ax.axis('off')

merged = gpd.sjoin(gdf, cell, how='left', op='within')

dane_agreg = merged.dissolve(by = "index_right", aggfunc = "sum")

cell.loc[dane_agreg.index, 'TOT'] = dane_agreg.TOT.values

ax = cell.plot(column = 'TOT', figsize = (12,8), cmap = 'viridis', vmax = 700000, edgecolor = 'grey', legend = True)
plt.autoscale(False)
ax.set_axis_off()
plt.axis('equal')
plt.title('Liczba ludnosci w siatce')

cell.loc[dane_agreg.index, 'MALE_0_14'] = dane_agreg.MALE_0_14.values

ax2 = cell.plot(column = 'MALE_0_14', figsize = (12,8), cmap = 'viridis', vmax = 100000, edgecolor = 'grey', legend = True)
plt.autoscale(False)
ax2.set_axis_off()
plt.axis('equal')
plt.title('Liczba ludnosci w wieku 1-14 lat w siatce')




