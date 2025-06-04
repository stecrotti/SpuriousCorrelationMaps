from make_dataset import make_and_save_dataset
from plotting import plotting

import geopandas as gpd
import os
import random

make_and_save_dataset()

filedir = os.path.dirname(os.path.realpath(__file__))
df = gpd.read_file(filedir + '/full_dataset.geojson')

valid_features = df.columns[~df.columns.isin(['Country', 'geometry'])].to_list()
name1, name2 = random.sample(valid_features, 2)

plotting.plot_two_series(df, name1, name2)