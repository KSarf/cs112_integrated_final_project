
import pandas as pd
import numpy as np
 
utilities = pd.read_csv('utilities.csv')
substations = pd.read_csv('substations.csv')
lines = pd.read_csv('lines.csv')

valid_ids = set(substations['Substation ID'])
bad_rows = lines[~lines['Source Substation ID'].isin(valid_ids)]

duplicates = utilities[utilities.duplicated()]
utilities = utilities.drop_duplicates()

bad_coords = substations[
    (substations['Latitude'] < 4) | (substations['Latitude'] > 15) |
    (substations['Longitude'] < -17) | (substations['Longitude'] > 15)
]

