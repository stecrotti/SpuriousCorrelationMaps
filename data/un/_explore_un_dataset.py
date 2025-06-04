import os
import urllib.request
import pandas as pd

from un_utils import *

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))
from utils import *

filedir = os.path.dirname(os.path.realpath(__file__))

urllib.request.urlretrieve("https://data.un.org/_Docs/SYB/CSV/SYB67_246_202411_Population%20Growth,%20Fertility%20and%20Mortality%20Indicators.csv", 
    filedir + '/data.csv')

df = pd.read_csv(filedir + '/data.csv', 
    skiprows = [0]
    )

df.rename(columns={'Unnamed: 1': 'Country'}, inplace=True)

df = correct_country_names(df)

features = df['Series'].unique()

first_valid_row = df[df['Country'] == 'Afghanistan'].iloc[0]
x = df.drop(index=range(first_valid_row.name))
print(f'Lines to skip: {first_valid_row.name}\n')

dfs = [make_feature_dataset(x, feat) for feat in features]
for df in dfs:
    if df is not None:
        print(df.columns.values[1])

os.remove(filedir + '/data.csv') 