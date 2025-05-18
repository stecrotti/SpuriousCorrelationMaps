import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import os

filedir = os.path.dirname(os.path.realpath(__file__))

df_in = gpd.read_file(filedir + '/../full_dataset.geojson')

df_plot = df_in[['Country', 'International migrants', 'Sex ratio (males to females)', 'geometry']]

fig, axes = plt.subplots(2, 1)
cmaps = ['Reds', 'Greens']

cor = df_plot[df_plot.columns[1]].corr(df_plot[df_plot.columns[2]])

for i in range(2):
    feature = df_plot.columns[i+1]
    df_plot.plot(
        ax = axes[i],
        column = df_plot[feature],
        missing_kwds = {'color': 'lightgrey'},
        cmap = cmaps[i],
        legend = True
    )

    axes[i].set_xticks([])
    axes[i].set_yticks([])

    axes[i].title.set_text(feature)

fig.suptitle(f'R={cor}')
plt.show()
