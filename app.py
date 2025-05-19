import streamlit as st

from plotting import plotting
from make_dataset import make_and_save_dataset

import os
import geopandas as gpd
import random

st.title('Spurious Correlation Maps')

# make_and_save_dataset()

if st.button("Generate random pair of maps", type="primary"):
    filedir = os.path.dirname(os.path.realpath(__file__))
    df = gpd.read_file(filedir + '/full_dataset.geojson')

    valid_features = df.columns[~df.columns.isin(['Country', 'geometry'])].to_list()
    name1, name2 = random.sample(valid_features, 2)
    fig = plotting.plot_two_series(df, name1, name2)
    st.write(fig)

