import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import os

cwd = os.path.dirname(os.path.realpath(__file__))

df_un = pd.read_csv(cwd + '/../data/un/un_clean.csv')

df = df_un[['Country', 'Population (millions)', 'Sex ratio (males to females)']]
df = df_un[['Country', 'Population aged 0 to 14 years old (proportion)', 'Population aged 60+ years old (proportion)']]

assert(len(df.columns) == 3)

gpd_countries = gpd.read_file(cwd + '/gpd_countries.geojson')
gpd_countries.reset_index(drop=True, inplace=True)
print(type(gpd_countries))

compatible_names = df['Country'].isin(gpd_countries['Country'])
df = df[compatible_names]

# fill with NaNs when countries in the map are not present in dataset
countries_to_be_added = gpd_countries['Country'][~gpd_countries['Country'].isin(df['Country'])].to_frame()
n = len(countries_to_be_added)
countries_to_be_added.insert(1, df.columns.tolist()[1], np.nan * np.ones(n))
countries_to_be_added.insert(1, df.columns.tolist()[2], np.nan * np.ones(n))

df = pd.concat([df, countries_to_be_added])
df.reset_index(drop=True, inplace=True)

df_plot = gpd_countries.merge(df, on='Country')

fig, axes = plt.subplots(2, 1)
cmaps = ['Reds', 'Greens']

cor = df_plot[df_plot.columns[2]].corr(df_plot[df_plot.columns[3]])

for i in range(2):
    feature = df_plot.columns[i+2]
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
