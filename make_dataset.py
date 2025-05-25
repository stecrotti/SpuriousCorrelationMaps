import pandas as pd
import geopandas as gpd
import numpy as np
import os


def check_format(df, full_df):
    "Check that new dataframe `df` is compatible in format with the master `full_df`"

    assert(df.columns.values[0] == 'Country') 

    return None

def fill_with_nans(df, full_df):
    countries_to_be_added = full_df['Country'][~full_df['Country'].isin(df['Country'])].to_frame()
    n = len(countries_to_be_added)
    for colname in df.columns[1:]:
        countries_to_be_added.insert(1, colname, np.nan * np.ones(n))
    df = pd.concat([df, countries_to_be_added])
    df.reset_index(drop=True, inplace=True)
    return df


def add_to_dataset(df, full_df):
    # check format
    check_format(df, full_df)

    # keep only rows with country names existing in `df_full`
    compatible_names = df['Country'].isin(full_df['Country'])
    df = df[compatible_names]

    # fill countries not in `df` with NaNs
    df = fill_with_nans(df, full_df)

    # add to big dataset
    full_df = full_df.merge(df, on=['Country'])

    return full_df

def make_and_save_dataset():
    filedir = os.path.dirname(os.path.realpath(__file__))

    # initialize dataset with geometry info to plot countries
    full_df = gpd.read_file(filedir + '/plotting/gpd_plot.geojson')

    # scan subfolders of `/data/` to look for datasets
    for subdir in os.walk(filedir + '/data'):
        dirpath, dirnames, filenames = subdir
        for filename in filenames:
            if filename.endswith('_SCMdataset.csv'):
                # load dataset to add
                df = pd.read_csv(dirpath + '/' + filename)
                # add dataset
                full_df = add_to_dataset(df, full_df)

    # save
    full_df_path = filedir + '/full_dataset.geojson'
    full_df.to_file(full_df_path)



