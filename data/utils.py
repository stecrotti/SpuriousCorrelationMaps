def correct_country_names(df):
    "Transform country names to the standard accepted by map"
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
        'Western Sahara': 'W. Sahara',
        'United States': 'United States of America'
    }
    return df.replace(d)