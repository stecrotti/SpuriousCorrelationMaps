"Donwload and save in a .geojson file the GeoDataFrame necessary for plotting"

import geopandas as gpd
import os

url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
gpd_countries = gpd.read_file(url)
gpd_countries.rename(columns={'NAME': 'Country'}, inplace=True)
gpd_countries = gpd_countries[['Country', 'geometry']]

gpd_countries.to_file(os.path.dirname(os.path.realpath(__file__)) + '/gpd_plot.geojson')