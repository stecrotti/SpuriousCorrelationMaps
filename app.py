import streamlit as st

from plotting import plotting
from make_dataset import make_and_save_dataset

import os
import geopandas as gpd
import random
import matplotlib

st.set_page_config(
        page_title = "Spurious Correlation Maps",
        page_icon = ":fried_shrimp:",
        layout="wide",
    )

st.title('Spurious Correlation Maps')

# make_and_save_dataset()

if st.button("Generate random pair of maps", type="primary"):
    filedir = os.path.dirname(os.path.realpath(__file__))
    df = gpd.read_file(filedir + '/full_dataset.geojson')

    valid_features = df.columns[~df.columns.isin(['Country', 'geometry'])].to_list()
    name1, name2 = random.sample(valid_features, 2)
    # matplotlib.rcParams.update({'font.size': 6})
    fig = plotting.plot_two_series(df, name1, name2)
    # fig.set_size_inches(3, 3)

    colsize = 0.4
    _side = (1 - colsize) / 2
    col1, col2, _ = st.columns([_side, colsize, _side])
    with col2:
        st.pyplot(fig)


st.markdown('''
            
            Click the button to plot a random pair of country-based data series, along with the corresponding [Pearson correlation coefficient](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient) R. 

            Visit the [source page](https://github.com/stecrotti/SpuriousCorrelationMaps) for more info.
            ''')

