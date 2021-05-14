# -*- coding: utf-8 -*-
"""
Created on Tue May 11 20:01:34 2021

@author: Kinga
"""
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import shapely

gdf_w = gpd.read_file('PD_STAT_GRID_CELL_2011.shp')

gdf = gdf_w.to_crs("EPSG:4326")

xmin, ymin, xmax, ymax = [13, 48, 25, 56]

n_cells = 30
cell_size = (xmax-xmin)/n_cells

grid_cells = []
for x0 in np.arange(xmin, xmax+cell_size, cell_size):
    for y0 in np.arange(ymin, ymax+cell_size, cell_size):
        x1 = x0 - cell_size
        y1 = y0 + cell_size
        grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))

cell = gpd.GeoDataFrame(grid_cells, columns=['geometry'], crs = 'EPSG:4326')

merged = gpd.sjoin(gdf, cell, how='left', op='within')

dane_agreg = merged.dissolve(by = "index_right", aggfunc = "sum")

#demografia ogólnie
cell.loc[dane_agreg.index, 'TOT'] = dane_agreg.TOT.values

ax = cell.plot(column = 'TOT', figsize = (12,8), cmap = 'viridis', vmax = 700000, edgecolor = 'grey', legend = True)
plt.autoscale(False)
ax.set_axis_off()
plt.axis('equal')
plt.title('Liczba ludnosci w siatce')

#Zadanie pkt a
cell.loc[dane_agreg.index, 'TOT_0_14'] = dane_agreg.TOT_0_14.values
ax2 = cell.plot(column = 'TOT_0_14', figsize = (12,8), cmap = 'viridis', 
                vmax = 150000, edgecolor = 'grey', legend = True)
plt.autoscale(False)
ax2.set_axis_off()
plt.axis('equal')
plt.title('Liczba ludnosci w wieku 0-14 lat')

#Zadanie pkt b
cell.loc[dane_agreg.index, 'TOT_15_64'] = dane_agreg.TOT_15_64.values
ax3 = cell.plot(column = 'TOT_15_64', figsize = (12,8), cmap = 'viridis', 
                vmax = 150000, edgecolor = 'grey', legend = True)
plt.autoscale(False)
ax3.set_axis_off()
plt.axis('equal')
plt.title('Liczba ludnosci w wieku 15-64 lat')

#Zadanie pkt c
cell.loc[dane_agreg.index, 'TOT_65__'] = dane_agreg.TOT_65__.values
ax4 = cell.plot(column = 'TOT_65__', figsize = (12,8), cmap = 'viridis', 
                vmax = 150000, edgecolor = 'grey', legend = True)
plt.autoscale(False)
ax4.set_axis_off()
plt.axis('equal')
plt.title('Liczba ludnosci w wieku 65 lat i powyżej')

#Zadanie pkt d
cell.loc[dane_agreg.index, 'MALE_0_14'] = dane_agreg.MALE_0_14.values
ax5 = cell.plot(column = 'MALE_0_14', figsize = (12,8), cmap = 'viridis', 
                vmax = 150000, edgecolor = 'grey', legend = True)
plt.autoscale(False)
ax5.set_axis_off()
plt.axis('equal')
plt.title('Liczba ludnosci męskiej w wieku 0-14 lat')
          
cell.loc[dane_agreg.index, 'MALE_15_64'] = dane_agreg.MALE_15_64.values
ax5 = cell.plot(column = 'MALE_15_64', figsize = (12,8), cmap = 'viridis', 
                vmax = 150000, edgecolor = 'grey', legend = True)
plt.autoscale(False)
ax5.set_axis_off()
plt.axis('equal')
plt.title('Liczba ludnosci męskiej w wieku 15-64 lat')

cell.loc[dane_agreg.index, 'MALE_65__'] = dane_agreg.MALE_65__.values
ax5 = cell.plot(column = 'MALE_65__', figsize = (12,8), cmap = 'viridis', 
                vmax = 150000, edgecolor = 'grey', legend = True)
plt.autoscale(False)
ax5.set_axis_off()
plt.axis('equal')
plt.title('Liczba ludnosci męskiej w wieku 65 lat i powyżej')


#punkt e
cell.loc[dane_agreg.index, 'FEM_0_14'] = dane_agreg.FEM_0_14.values
ax6 = cell.plot(column='FEM_0_14', figsize=(12, 8), cmap='viridis', 
               vmax = 150000, edgecolor="grey", legend = True)
plt.autoscale(False)
ax6.set_axis_off()
plt.axis('equal')
plt.title('liczba kobiet w wieku do 14 lat w siatce')

cell.loc[dane_agreg.index, 'FEM_15_64'] = dane_agreg.FEM_15_64.values
ax7 = cell.plot(column='FEM_15_64', figsize=(12, 8), cmap='viridis', 
               vmax = 150000, edgecolor="grey", legend = True)
plt.autoscale(False)
ax7.set_axis_off()
plt.axis('equal')
plt.title('liczba kobiet w wieku 15-64 lat w siatce')

cell.loc[dane_agreg.index, 'FEM_65__'] = dane_agreg.FEM_65__.values
ax8 = cell.plot(column='FEM_65__', figsize=(12, 8), cmap='viridis', 
               vmax = 150000, edgecolor="grey", legend = True)
plt.autoscale(False)
ax8.set_axis_off()
plt.axis('equal')
plt.title('liczba kobiet w wieku do 14 lat w siatce')

# punkt f
dane_demograficzne = gdf_w[['TOT', 'geometry']]

wojew = gpd.read_file('Województwa.shp', encoding='utf-8')
wojew = wojew[['JPT_NAZWA_', 'geometry']]
merged = gpd.sjoin(dane_demograficzne, wojew, how='left', op='within')
dane_agreg = merged.dissolve(by = "index_right", aggfunc = "sum")

#liczba ludnosci w wojewodztwach
ax = dane_agreg.plot(column = 'TOT', cmap = 'viridis', edgecolor = 'grey', legend = True)
ax.set_axis_off()
plt.axis('equal')
plt.title('Liczba ludnosci w wojewodztwach')

#ratio w zależnoci od powierzchni
powierzch = wojew.area/1000000
ratio = dane_agreg.TOT.values/powierzch
dane_agreg['ratio'] = ratio
ax2 = dane_agreg.plot(column = 'ratio', cmap = 'viridis', edgecolor = 'grey', legend = True)
ax2.set_axis_off()
plt.axis('equal')
plt.title('Liczba ludnosci w wojewodztwach w odniesieniu do powierzchni')
