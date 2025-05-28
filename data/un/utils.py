import urllib.request
import pandas as pd

# select only valid country names
def correct_country_names(df):
    d = {
        'The Bahamas': 'Bahamas',
        'Bolivia (Plurin. State of)' : 'Bolivia',
        'Bosnia and Herzegovina': 'Bosnia and Herz.',
        'Central African Republic': 'Central African Rep.',
        'Brunei Darussalam' : 'Brunei',
        'Republic of the Congo': 'Congo',
        'Côte d’Ivoire': "Côte d'Ivoire",
        "Dem. People's Rep. Korea": 'North Korea',
        'Republic of Korea': 'South Korea',
        'Dem. Rep. of the Congo': 'Dem. Rep. Congo',
        'Dominican Republic': 'Dominican Rep.',
        'Eswatini': 'eSwatini',
        'Equatorial Guinea': 'Eq. Guinea',
        'Falkland Islands (Malvinas)': 'Falkland Is.',
        'Iran (Islamic Republic of)': 'Iran',
        "Lao People's Dem. Rep.": 'Laos',
        'Netherlands (Kingdom of the)': 'Netherlands',
        'Republic of Moldova': 'Moldova',
        'Russian Federation': 'Russia',
        'Republic of Serbia': 'Serbia',
        'South Sudan': 'S. Sudan',
        'Syrian Arab Republic': 'Syria',
        'Türkiye': 'Turkey',
        'United Rep. of Tanzania': 'Tanzania',
        'Venezuela (Boliv. Rep. of)':'Venezuela',
        'Viet Nam': 'Vietnam',
        'Western Sahara': 'W. Sahara'
    }
    return df.replace(d)

def prepare_un_dataset(filedir, url):
    # download dataset
    urllib.request.urlretrieve(url, filedir + '/tmp_data.csv')

    # read starting from relevant row and set column name to Country
    df_in = pd.read_csv(filedir + '/tmp_data.csv', skiprows = [0], encoding = 'latin-1')
    df_in.rename(columns={'Unnamed: 1': 'Country'}, inplace=True)
    df_in = correct_country_names(df_in)
    starts_with_afghanistan = df_in[df_in['Country'] == 'Afghanistan']
    if starts_with_afghanistan.empty:
        raise(Exception('DataFrame does not contain entry for the first country in alphabetical order: Afghanistan'))
    else:
        first_valid_row = starts_with_afghanistan.iloc[0]
        df_in = df_in.drop(index=range(first_valid_row.name))
        return df_in
    

def dataset_from_names_and_transforms(df_in, names_transforms):
    dfs = []
    # iterate over feature names to find matches
    for _, row in names_transforms.iterrows():
        if row['name'] in df_in['Series'].values:
            # append data to dfs
            df = make_feature_dataset(
                df_in, 
                row['name'], newname = row['newname'], transform = row['transform']
            )
            dfs.append(df)

    return dfs

def make_names_transforms_df(names_transforms_array):
    # fill dataframe with names and transforms
    names_transforms = pd.DataFrame(columns=['name', 'newname', 'transform'])
    for nt in names_transforms_array:
        names_transforms.loc[len(names_transforms)] = nt

    return names_transforms

def make_feature_dataset(df_in, feature_name, newname = None, transform = None):
    if newname is None:
        newname = feature_name
    if transform is None:
        transform = lambda x : x
    is_required_feature = df_in['Series'] == feature_name
    df = df_in[is_required_feature]
    ncountries = df_in['Country'].nunique()
    countries_covered_by_year = (df.groupby('Year').nunique()['Country'])
    covered_years = countries_covered_by_year[countries_covered_by_year == ncountries]
    if covered_years.empty:
        # print(f'Warning: Feature `{feature_name}` not available for all {ncountries} countries for all years:\n{countries_covered_by_year}\n')
        return None
    year = int(covered_years.index[-1])
    df = df[df['Year'] == year]
    assert(len(df) == ncountries)
    df.reset_index(inplace = True)
    df = df[['Country', 'Value']]
    df.rename(columns={'Value': newname}, inplace=True)
    df[newname] = df[newname].apply(transform)
    return df

def string_with_commas_to_float(s):
    ss = ''.join(s.split(','))
    return float(ss)

def string_with_commas_to_int(s):
    ss = ''.join(s.split(','))
    return int(ss)

def percentage_str_to_prop_float(s):
    return float(s) / 100

def perthousand_str_to_prop_float(s):
    return float(s) / 1000

def str_mult_times_thousand(s):
    return float(s) * 1000