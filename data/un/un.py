import os
import urllib.request
import pandas as pd

cwd = os.path.dirname(os.path.realpath(__file__))

urllib.request.urlretrieve("https://data.un.org/_Docs/SYB/CSV/SYB67_1_202411_Population,%20Surface%20Area%20and%20Density.csv", 
    cwd + '/data.csv')

df_in = pd.read_csv(cwd + '/data.csv', 
    skiprows = [0] + list(range(2, 885))
    )

df_in.rename(columns={'Unnamed: 1': 'Country'}, inplace=True)

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

df_in = correct_country_names(df_in)

ncountries = df_in['Country'].nunique()

feature = 'Population mid-year estimates (millions)'

def get_feature_dataset(df_in, feature_name, ncountries, newname = None, transform = None):
    if newname is None:
        newname = feature_name
    if transform is None:
        transform = lambda x : x
    is_required_feature = df_in['Series'] == feature_name
    df = df_in[is_required_feature]
    all_countries_covered = (df.groupby('Year').nunique()['Country'] == ncountries)
    covered_years =  all_countries_covered[all_countries_covered==True]
    if covered_years.empty:
        error("Feature not available for all countries")
    year = int(covered_years.index[-1])
    df = df[df['Year'] == year]
    assert(len(df) == ncountries)
    df.reset_index(inplace = True)
    df = df[['Country', 'Value']]
    df.rename(columns={'Value': newname}, inplace=True)
    df[newname] = transform(df[newname])
    return df

def string_with_commas_to_float(s):
    ss = ''.join(s.split(','))
    return float(ss)

df_pop = get_feature_dataset(
    df_in, 
    'Population mid-year estimates (millions)',
    ncountries,
    newname = 'Population (millions)',
    transform = lambda x : [string_with_commas_to_float(xx) for xx in x]
    )

df_sex_ratio = get_feature_dataset(
    df_in, 
    'Sex ratio (males per 100 females)',
    ncountries,
    newname = 'Sex ratio (males to females)',
    transform = lambda x : [float(xx)/100 for xx in x]
    )
df_un = pd.merge(df_pop, df_sex_ratio)

df_pop_young = get_feature_dataset(
    df_in, 
    'Population aged 0 to 14 years old (percentage)',
    ncountries,
    newname = 'Population aged 0 to 14 years old (proportion)',
    transform = lambda x : [float(xx)/100 for xx in x]
    )
df_un = pd.merge(df_un, df_pop_young)

df_pop_old = get_feature_dataset(
    df_in, 
    'Population aged 60+ years old (percentage)',
    ncountries,
    newname = 'Population aged 60+ years old (proportion)',
    transform = lambda x : [float(xx)/100 for xx in x]
    )
df_un = pd.merge(df_un, df_pop_old)

df_un.to_csv(cwd + '/un_clean.csv', index = False)

os.remove(cwd + '/data.csv') 