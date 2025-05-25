import os
import urllib.request
import pandas as pd
from functools import reduce

from utils import *

filedir = os.path.dirname(os.path.realpath(__file__))

urllib.request.urlretrieve("https://data.un.org/_Docs/SYB/CSV/SYB67_246_202411_Population%20Growth,%20Fertility%20and%20Mortality%20Indicators.csv", 
    filedir + '/data.csv')

df_in = pd.read_csv(filedir + '/data.csv', 
    skiprows = [0] #+ list(range(2, 837))
    )

df_in.rename(columns={'Unnamed: 1': 'Country'}, inplace=True)

df_in = correct_country_names(df_in)

first_valid_row = df_in[df_in['Country'] == 'Afghanistan'].iloc[0]
df_in = df_in.drop(index=range(first_valid_row.name))

dfs_un = []

df = get_feature_dataset(
    df_in, 
    'Total fertility rate (children per women)',
    transform = string_with_commas_to_float
    )
dfs_un.append(df)
    
df = get_feature_dataset(
    df_in, 
    'Under five mortality rate for both sexes (per 1,000 live births)',
    newname = 'Under five mortality rate for both sexes (proportion to live births)',
    transform = perthousand_str_to_prop_float
    )
dfs_un.append(df)

df = get_feature_dataset(
    df_in, 
    'Life expectancy at birth for both sexes (years)',
    newname = 'Life expectancy at birth (years)',
    transform = string_with_commas_to_float
    )
dfs_un.append(df)

df = get_feature_dataset(
    df_in, 
    'Population annual rate of increase (percent)',
    newname = 'Population annual rate of increase (proportion)',
    transform = percentage_str_to_prop_float
    )
dfs_un.append(df)

dfs_notnone = [df for df in dfs_un if df is not None]

df_un = reduce(lambda  left,right: pd.merge(left,right,on=['Country'],
                                            how='outer'), dfs_un)

df_un.to_csv(filedir + '/' + os.path.basename(__file__)[:-3] + '_SCMdataset.csv', index = False)

os.remove(filedir + '/data.csv') 