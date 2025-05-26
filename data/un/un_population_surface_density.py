import os
import urllib.request
import pandas as pd
from functools import reduce

from utils import *

filedir = os.path.dirname(os.path.realpath(__file__))

urllib.request.urlretrieve("https://data.un.org/_Docs/SYB/CSV/SYB67_1_202411_Population,%20Surface%20Area%20and%20Density.csv", 
    filedir + '/data.csv')

df_in = pd.read_csv(filedir + '/data.csv', 
    skiprows = [0] + list(range(2, 885))
    )

df_in.rename(columns={'Unnamed: 1': 'Country'}, inplace=True)

df_in = correct_country_names(df_in)

dfs_un = []

df = get_feature_dataset(
    df_in, 
    'Population mid-year estimates (millions)',
    newname = 'Population (millions)',
    transform = string_with_commas_to_float
    )
if df is not None:
    dfs_un.append(df)

df = get_feature_dataset(
    df_in, 
    'Sex ratio (males per 100 females)',
    newname = 'Sex ratio (males to females)',
    transform = percentage_str_to_prop_float
    )
if df is not None:
    dfs_un.append(df)

df = get_feature_dataset(
    df_in, 
    'Population aged 0 to 14 years old (percentage)',
    newname = 'Population aged 0 to 14 years old (proportion)',
    transform = percentage_str_to_prop_float
    )
if df is not None:
    dfs_un.append(df)

df = get_feature_dataset(
    df_in, 
    'Population aged 60+ years old (percentage)',
    newname = 'Population aged 60+ years old (proportion)',
    transform = percentage_str_to_prop_float
    )
if df is not None:
    dfs_un.append(df)

df_pop_density = get_feature_dataset(
    df_in, 
    'Population density',
    newname = 'Population density (per km2)',
    transform = string_with_commas_to_float
    )
if df is not None:
    dfs_un.append(df)

df_un = reduce(lambda  left,right: pd.merge(left,right,on=['Country'],
                                            how='inner'), dfs_un)

df_un.to_csv(filedir + '/' + os.path.basename(__file__)[:-3] + '_SCMdataset.csv', index = False)

os.remove(filedir + '/data.csv') 