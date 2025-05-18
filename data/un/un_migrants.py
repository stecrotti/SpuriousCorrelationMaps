import os
import urllib.request
import pandas as pd

from utils import *

filedir = os.path.dirname(os.path.realpath(__file__))

urllib.request.urlretrieve("https://data.un.org/_Docs/SYB/CSV/SYB67_327_202411_International%20Migrants%20and%20Refugees.csv", 
    filedir + '/data.csv')

df_in = pd.read_csv(filedir + '/data.csv', 
    skiprows = [0] + list(range(2, 552))
    )

df_in.rename(columns={'Unnamed: 1': 'Country'}, inplace=True)

df_in = correct_country_names(df_in)

df_migrants = get_feature_dataset(
    df_in, 
    'International migrant stock: Both sexes (number)',
    newname = 'Number of international migrants',
    transform = string_with_commas_to_int
    )
df_un = df_migrants

df_migrants_proportion = get_feature_dataset(
    df_in, 
    'International migrant stock: Both sexes (% total population)',
    newname = 'International migrants in proportion to population',
    transform = percentage_str_to_prop_float
    )
df_un = pd.merge(df_un, df_migrants_proportion)

# df_refugees = get_feature_dataset(
#     df_in, 
#     'Total refugees and people in refugee-like situations (number)',
#     newname = 'Number of refugees and people in refugee-like situations',
#     transform = string_with_commas_to_int
#     )
# df_un = pd.merge(df_un, df_refugees)

# df_asylum = get_feature_dataset(
#     df_in, 
#     'Asylum seekers, including pending cases (number)',
#     newname = 'Number of asylum seekers, including pending cases (number)',
#     transform = string_with_commas_to_int
#     )
# df_un = pd.merge(df_un, df_asylum)

df_un.to_csv(filedir + '/' + os.path.basename(__file__)[:-3] + '_SCMdataset.csv', index = False)

os.remove(filedir + '/data.csv') 