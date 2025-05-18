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

def get_feature_dataset(df_in, feature_name, newname = None, transform = None):
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
        raise Exception(f"Feature not available for all countries for all years:\n{countries_covered_by_year}")
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